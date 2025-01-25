import os
from subprocess import check_output
import cv2
import math
import numpy as np
from conversion.core.eft_helper import US_CHAR
from conversion.core.fd258_ocr import OCR_LOCATIONS

class Finger:
    def __init__(self, str):
        """
        Center (sx,sy)
        Dimensions (sw,sh)
        Angle (t)

        self.start
        self.end
        """
        self.orgID = "15" # Vendor ID for NFIQv1
        self.algID = "14205" # Algorithm ID for NFIQv1
        self.str = str
        self.readString()
        self.computeBox()
        self.segmentQuality()

    def readString(self):
        vals = self.str.split(' ')
        #[FILE, lfour_10.raw, ->, e, 3, sw, 168, sh, 280, sx, 120, sy, 256, th, -28.3]
        self.name = vals[1]
        print(vals)
        print(self.name, self.name.split('_'))
        self.n = str(int(self.name.split('_')[2].split('.')[0]))
        self.sw = int(vals[6])
        self.sh = int(vals[8])
        self.sx = int(vals[10])
        self.sy = int(vals[12])
        self.t = float(vals[14])

    def computeBox(self):
        self.x1 = str(abs(int((self.sw / 2) * math.cos(self.t) - (self.sh / 2)))) # Left
        self.y1 = str(abs(int((self.sh / 2) * math.cos(self.t) - (self.sw / 2)))) # Top
        self.x2 = str(abs(int((self.sw / 2) * math.cos(self.t) + (self.sh / 2)))) # Top
        self.y2 = str(abs(int((self.sh / 2) * math.cos(self.t) - (self.sw / 2)))) # Bottom

    def segmentQuality(self):
        # Four fields in each finger

        # finger number (1-10)
        # estimated correctends (254)
        # Vendor quality id
        # numeric product code 
        x = "nfiq {}".format(self.name)
        self.score = check_output(x, shell=True, text=True).strip()

    def getScoreString(self):
        if int(self.n) == 11:
            a = "1"
        elif int(self.n) == 12:
            a="6"
        else:
            a=self.n
        x = a + chr(US_CHAR) + self.score + chr(US_CHAR) + self.orgID + chr(US_CHAR) + self.algID
        return x

    def getPosString(self):
        x = self.n + chr(US_CHAR) + self.x1 + chr(US_CHAR) + self.x2 + chr(US_CHAR) + self.y1 + chr(US_CHAR) + self.y2
        return x

class Fingerprint:
    """
        self.tmpdir # The temporary directory files are stored in
        self.name # The file name (without encoding)
        self.encoding # The base encoding
        self.converted # The compressed fingerprint file
        self.src # The CV2 image used to extract fingerprint
        self.img # The CV2 image of the extracted fingerprint
        self.ppi # Pixel density
        self.hll # HORIZONTAL LINE LENGTH
        self.vll # VERTICAL LINE LENGTH
        self.hps # HORIZONTAL PIXEL SCALE
        self.vps # VERTICAL PIXEL SCALE
        self.slc # SCALE UNITS
        self.cga # COMPRESSION ALGORITHM (JP2 default)
        self.bpx # BITS PER PIXEL
        self.fgp # Fingerprint position
    """
    def __init__(self, loc, src_img, tmpdir):
        self.tmpdir = tmpdir
        self.name = loc.id
        self.fgp = loc.fp_number
        self.encoding = 'png'
        self.converted = ""
        self.src = src_img
        self.extract_fp(loc.bbox) # Sets self.img 
        self.fingers = []

    def get_settings(self):
        self.ppi = self.get_ppi()
        self.hll = self.img.shape[1]# HORIZONTAL LINE LENGTH
        self.vll = self.img.shape[0] # VERTICAL LINE LENGTH
        self.slc = "1" # SCALE UNITS
        self.bpx = 8 # BITS PER PIXEL, should be 8

    def get_ppi(self):
        # Image should be 8x8"
        x = self.src.shape[0] / 8
        y = self.src.shape[1] / 8
        # Real DPI
        # Now to convert image to correct DPI
        self.hps = round(x) # HORIZONTAL PIXEL SCALE
        self.vps = round(y) # VERTICAL PIXEL SCALE
        self.ppi = round((x+y)/2) 

    def extract_fp(self, bbox):
        """
        Extract the fingerprint from the bounding box, resize it, and process it further.
        """
        (x, y, w, h) = bbox
        self.img = self.src[y:y + h, x:x + w]
        print(f"Extracted image shape: {self.img.shape}")  # Debug log

        self.crop_image()  # Crop unnecessary whitespace
        self.resize_image(min_side=1400)  # Resize with proper scaling
        self.save_image()

    def segment(self):
        x=""
        if 'nt' in os.name:
            x += "wsl "
        x += "nfseg {} 1 1 1 0 {}".format(self.fgp, self.converted.replace('jp2','png'))
        a = check_output(x, shell=True, text=True).split('\n')
        for each in a:
            tmp = each.split('FILE')
            if len(tmp) > 1 and len(tmp[1])>1:
                tmp = tmp[1]
                self.fingers.append(Finger(tmp))
    def crop_image(self):
        print(f"Image shape before cropping: {self.img.shape}")
        """Crop the image to remove unnecessary white space."""
        # Ensure the image is at least 2D
        if len(self.img.shape) == 2:
            gray = self.img  # Image is already grayscale
        else:
            gray = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale if needed

        # Threshold and crop
        _, thresh = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
        x, y, w, h = cv2.boundingRect(thresh)
        self.img = self.img[y:y + h, x:x + w]
        print(f"Image shape before cropping: {self.img.shape}")

    def resize_image(self, min_side=1400):
        """
        Resize the image to ensure the smallest side is at least `min_side` while maintaining aspect ratio.
        """
        h, w = self.img.shape[:2]

        # Calculate scaling factor to make the smallest side equal to or greater than `min_side`
        scaling_factor = max(min_side / w, min_side / h)
        new_width = int(w * scaling_factor)
        new_height = int(h * scaling_factor)

        # Resize the image while maintaining aspect ratio
        self.img = cv2.resize(self.img, (new_width, new_height), interpolation=cv2.INTER_AREA)

        print(f"Image resized to: {self.img.shape}")  # Debug log

    def set_dpi(self, dpi):
        """
        Adjust the DPI metadata of the image. 
        OpenCV does not support this directly, so this requires using the PIL library.
        """
        from PIL import Image
        import tempfile

        # Save the current image temporarily
        temp_file = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        cv2.imwrite(temp_file.name, self.img)

        # Open the image with PIL and adjust DPI
        with Image.open(temp_file.name) as pil_img:
            pil_img.save(temp_file.name, dpi=(dpi, dpi))

        # Reload the adjusted image back into OpenCV format
        self.img = cv2.imread(temp_file.name)
        os.remove(temp_file.name)

    def save_image(self, encoding=None):
        """Save the processed image to disk, ensuring it is in 8-bit grayscale."""
        if encoding is None:
            f = os.path.join(self.tmpdir, self.name) + '.' + self.encoding
        else:
            f = os.path.join(self.tmpdir, self.name) + '.' + encoding

        # Convert to grayscale if the image has 3 channels
        if len(self.img.shape) == 3:
            gray_img = cv2.cvtColor(self.img, cv2.COLOR_BGR2GRAY)
        else:
            gray_img = self.img  # Already grayscale

        cv2.imwrite(f, gray_img)

    def convert(self, encoding='jp2', ratio=10):
        """
        Convert the image to the desired encoding and compression ratio.
        """
        self.get_settings()
        self.crop_image()  # Ensure the image is cropped
        self.resize_image(min_side=1400)  # Resize with proper scaling
        i = os.path.join(self.tmpdir, self.name)
        o = i + '.' + encoding
        i = i + '.' + self.encoding
        x = ""
        print("Encoding: {}".format(encoding))
        if 'nt' in os.name:
            x += "wsl "
        if encoding == 'jp2':
            self.cga = "JP2"  # COMPRESSION ALGORITHM
            x += "opj_compress -i {} -o {} -r {} -n 2".format(i, o, ratio)
        os.system(x)
        self.converted = o
        self.segment()  # Now segment the compressed file
