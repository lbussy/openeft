# This is the 10-print version of this app. It is not stable and still a WIP. Use the Main branch!

#### Current Problems
- 10print scanning is not functioning correctly
  - Related file: conversion/core/fd258_ocr.py
  - When lines 26-37 are uncommented, it throws off OCR locations
  - When OCR does work correctly (which seems to be sporadic), it throws an error referencing NBIS 1 1 1 1 0 location, which means everything is attempting to be consolidated into the four slaps instead of individual fingers

# OpenEFT

<img src="docs/imgs/blurred.png" width="250" />

OpenEFT is an open-source project originally created by Noah Wood. Its purpose is to convert physical FD-258 fingerprint cards to EBTS-packaged, EFT-formatted files.

So, if you're here, you probably need to file a Form 1 or Form 4 and would like to file electronically.

The original software appears to be abandoned and had a few core issues, including links to moving codebases that are being maintained independently (such as NIST's NBIS). Because of this, 

## How To Use

1. Print an FD-258 card (use <a href=fd-258-110120.pdf>this file</a> for a fillable card)

2. Roll your prints on the card (you don't need to fill out the boxes)

3. Take a high-resolution **1:1** scan (at least 600 DPI) of the completed FD-258 card.

4. Run the python program from the command line like so:

   ```
      python3 openeft.py
   ```

5. Access the tool via HTTP://localhost:8080

6. Follow the instructions the program provides and respond to the prompts with your info.

7. Validate the file using <a href="https://www.netxsolutions.co.uk/NISTViewer.aspx" target="_blank">NIST Viewer</a>

8. Validate the file was packaged correctly to EBTS specifications by attempting to upload it to the Responsible Person train stop of eForms

9. Congratulations! You now have an EFT!

## Tips

#### How To Record Fingerprints

If you've never had your fingerprints taken, you definitely need to know how to do it. The first ten prints should be "rolled" on as the video demonstrates, then you need to take two "slap" impressions of the four fingers on each hand and two flat impressions of the thumbs.

[![Rolling Your Prints](http://img.youtube.com/vi/47YLGj_yLVA/0.jpg)](//www.youtube.com/watch?v=47YLGj_yLVA "Fingerprinting Technique")

#### Bad Fingerprints

If you mess up on a fingerprint, you can use a white address label within the blue or black bounding boxes to re-ink that specific finger so you don't need to waste multiple cards. Do not use white-out.

## Installing

1. Clone the repo:

   ```sh
   git clone --recurse-submodules https://github.com/Robbbbbbbbb/OpenEFT.git
   ```

2. Build & Install

   ```sh
   # If Windows
   wsl cd OpenEFT
   wsl ./build_windows.sh
   # If Linux
   cd OpenEFT
   ./build_linux.sh
   ```

5. Run the program!

   ```bash
   python3 openeft.py

6. Access the app in a web browser:

   HTTP://localhost:8080

   *NOTE* If you want to access this on other hosts on your network, you can open TCP/8080 on Windows Firewall.
   *NOTE* If placing behind a reverse proxy, do _not_ expose this to the internet unless you want the world to have your EFTs and be able to read the contents (eg: your SSN)

## Requirements

#### Operating Systems

* Linux (Ubuntu)
* Windows using WSL (https://learn.microsoft.com/en-us/windows/wsl/install)

#### External Libraries

* [OpenJPEG](https://github.com/uclouvain/openjpeg)
* [NBIS](https://www.nist.gov/services-resources/software/nist-biometric-image-software-nbis) (Currently a working build is forked to https://github.com/Robbbbbbbbb/NBIS.git and is called with the ./build_windows.sh script)

#### Python Modules

* [OpenCV-Python](https://github.com/opencv/opencv-python)
* [Imutils](https://github.com/PyImageSearch/imutils)
* [Pillow](https://python-pillow.org/)
* [NumPy](https:://numpy.org)
* django

## ScreenShots

![](docs/imgs/openeft_gui.png)

![Confirmation With ATF](docs/imgs/personal.png)

![](docs/imgs/eft_files.png)



![Confirmation With ATF](docs/imgs/ITWORKS.png)
