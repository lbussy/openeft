import os
import cv2
import time
import json
import threading

from django.http import JsonResponse, HttpResponse  # Import HttpResponse here
from urllib.parse import quote  # Depreciated urlquote
from django.shortcuts import render, redirect
from django.conf import settings
from django.views.decorators.http import require_http_methods

from conversion.core.core import generate_eft, section_fp, manual_section

CWD = os.getcwd()
TMP_DIR = settings.TMP_DIR
FILES = []  # List to hold generated files

# Create your views here.

def index(request):
    return render(request, "conversion/index.html")

def new(request):
    return render(request, "conversion/new.html")

def process_fp():
    os.chdir(TMP_DIR)
    for each in RESULTS:
        each.convert()

def resection(request):
    if request.method == "POST":
        data = request.POST.dict()
        fname = os.path.join(TMP_DIR, 'input.png')
        out = manual_section(fname=fname, data=data)
        return JsonResponse({'values': out}, safe=False)
    return JsonResponse({'message': 'Invalid request method'}, status=405)

def step1(request):
    global RESULTS
    if request.method == "POST":
        file = request.FILES.get("formFileLg")
        print(file)
        time.sleep(1)
        fname = os.path.join(TMP_DIR, 'input.png')
        with open(fname, 'wb+') as dest:
            for chunk in file.chunks():
                dest.write(chunk)
        try:
            out = section_fp(fname=fname)
        except Exception as e:
            print(e)
            out = False
        return JsonResponse({'values': out}, safe=False)
    return JsonResponse({'message': 'Invalid request method'}, status=405)

def step2(request):
    global FILES
    if request.method == "POST":
        print(dir(request))
        print(request.body)
        data = request.POST.dict()
        fname = generate_eft(data)
        FILES.append(fname)
    return render(request, "conversion/download.html", context={'files': FILES})

def download(request, filename):
    """
    Handle the download of files.
    """
    file_path = os.path.join(TMP_DIR, filename)
    
    # Check if the file exists
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/octet-stream")
            # Depreciated urlquote - using `quote` instead of `urlquote`
            response['Content-Disposition'] = f'attachment; filename={quote(filename)}'
            return response
    else:
        return JsonResponse({"message": "File not found"}, status=404)

@require_http_methods(["DELETE"])
def delete_file(request, filename):
    """
    Handles the deletion of files from the server
    """
    global FILES
    file_path = os.path.join(TMP_DIR, filename)

    # Check if the file exists and remove it
    if os.path.exists(file_path):
        os.remove(file_path)
        FILES = [f for f in FILES if f != filename]  # Remove the file from the FILES list
        return JsonResponse({"message": "File deleted successfully"}, status=200)
    else:
        return JsonResponse({"message": "File not found"}, status=404)
