from django.shortcuts import render, redirect
from .models import Search
from .forms import SearchForm
from django.http import JsonResponse
from .darkflow.darkflow.net.build import TFNet
import cv2
import os
import json
from django.conf import settings
import numpy as np

# Create your views here.
def index(request):
    return render(request, 'yolos/index.html')

def search(request):
    # search = Search.objects.all()
    # upimg = search[0].image
    # context = {
    #     'upimg': upimg
    # }
    return render(request, 'yolos/search.html')

def upload(request):
    _, files = request.FILES.popitem()
    files = files[0]
    search = Search()
    search.image = files
    search.save()
    img = Search.objects.all().last()
    # print(img.url)
    print(img.image.url)
    print(img.image.name)
    context = {
        'img_url': img.image.url,
        'img_name': img.image.name,
    }
    return JsonResponse(context)

def goflow(request):
    search = Search()
    img = Search.objects.all().last()
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, 'darkflow', 'cfg', 'my-tiny-yolo.cfg')
    print(module_dir)
    print(file_path)
    options = {
        "model": file_path,
        "load": -1,
        "threshold": 0.1
    }
    print('==')
    tfnet = TFNet(options)
    print('===')
    path = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, img.image.name)
    # print(path)
    imgcv = cv2.imread(path)
    # print(imgcv)
    result = tfnet.return_predict(imgcv)
    print(type(result))
    reimg = json.dumps(str(result[0]))
    print(reimg)
    print('-------------')
    b = imgcv.tolist()
    a = json.dumps(b)
    for r in result:
        r['confidence'] = str(r['confidence'])
    context = {
        'result': result,
        'img_url': img.image.url,
    }
    return JsonResponse(context)