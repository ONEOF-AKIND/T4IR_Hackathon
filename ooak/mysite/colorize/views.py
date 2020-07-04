from django.shortcuts import render, redirect
from .models import Search, Search2
from django.http import JsonResponse
import caffe
import numpy as np
import scipy as sp
import matplotlib.pyplot as plt
from data import colorize_image as CI
from skimage import color
from data import lab_gamut as lab

# Create your views here.
def index(request):
    return render(request, 'colorizes/search.html')

def upload(request):
    _, files = request.FILES.popitem()
    files = files[0]
    search = Search()
    search.image = files
    search.save()
    img = Search.objects.all().last()

    print(img.image.url)
    print(img.image.name)
    context = {
        'img_url':img.image.url,
        'img_name':img.image.name,
    }
    return JsonResponse(context)
def upload2(request):
    _, files = request.FILES.popitem()
    files = files[0]
    search2 = Search2()
    search2.image = files
    search2.save()
    img2 = Search2.objects.all().last()

    print(img2.image.url)
    print(img2.image.name)
    context = {
        'img_url2':img2.image.url,
        'img_name2':img2.image.name,
    }
    return JsonResponse(context)

def colorize(request):
    search = Search()
    img = Search.objects.all().last()
    
    

    search2 = Search2()
    img2 = Search2.objects.all().last()
    
    import os
    from django.conf import settings
    print(os.getenv('PYTHONPATH'))
    img_path = os.path.join(settings.MEDIA_ROOT, img.image.url)
    ref_path = os.path.join(settings.MEDIA_ROOT, img2.image.url)
    img_path = "."+img.image.url
    ref_path = "."+img2.image.url

    print("-------------------------------------"+img_path)
    print("-------------------------------------"+ref_path)

    # color histogram to use
    
    gpu_id = -1
    Xd = 256
    cid = CI.ColorizeImageCaffeGlobDist(Xd)
    cid.prep_net(gpu_id,prototxt_path='./models/global_model/deploy_nodist.prototxt',caffemodel_path='./models/global_model/global_model.caffemodel')
    gt_glob_net = caffe.Net('./models/global_model/global_stats.prototxt','./models/global_model/dummy.caffemodel', caffe.TEST)
    cid.load_image(img_path)
    
    input_ab = np.zeros((2,Xd,Xd))
    input_mask = np.zeros((1,Xd,Xd))
    img_pred = cid.net_forward(input_ab,input_mask)
    img_pred_auto_fullres = cid.get_img_fullres()
    img_gray_fullres = cid.get_img_gray_fullres()

    def get_global_histogram(ref_path):
        ref_img_fullres = caffe.io.load_image(ref_path)
        img_glob_dist = (255*caffe.io.resize_image(ref_img_fullres,(Xd,Xd))).astype('uint8') # load image
        gt_glob_net.blobs['img_bgr'].data[...] = img_glob_dist[:,:,::-1].transpose((2,0,1)) # put into 
        gt_glob_net.forward()
        glob_dist_in = gt_glob_net.blobs['gt_glob_ab_313_drop'].data[0,:-1,0,0].copy()
        return (glob_dist_in,ref_img_fullres)
    
    (glob_dist_ref,ref_img_fullres) = get_global_histogram(ref_path)
    img_pred = cid.net_forward(input_ab,input_mask,glob_dist_ref)
    img_pred_withref_fullres = cid.get_img_fullres()

    plt.figure(figsize=(10,4))
    # plt.imshow(np.concatenate((img_gray_fullres,img_pred_withref_fullres),axis=1))
    plt.imshow(img_pred_withref_fullres)
    plt.title('greisekkiya!')
    plt.axis('off')
    plt.savefig('./colorize/static/colorize/images/result.jpg')
    
   

    return redirect('colorizes:index')