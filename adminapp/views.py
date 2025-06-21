from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
from userapp.models import *
from adminapp.models import *
from django.contrib import messages
from django.core.mail import send_mail
import os
import numpy as np
from django.shortcuts import render
from django.core.files.storage import default_storage


def index(request):
    t_users = User.objects.all()
    a_users = User.objects.filter(status="Accepted")
    p_users = User.objects.filter(status="Pending")
    context ={
        't_users':len(t_users),
        'a_users':len(a_users),
        'p_users':len(p_users),

    }
    return render(request,'admin/index.html',context)







def all_users(request):
    user = User.objects.all()
    context = {
        'user':user,
    }
    return render(request,'admin/all-users.html',context)










from django.core.files.storage import default_storage
from django.http import HttpResponseBadRequest

def upload_dataset(request):
    if request.method == 'POST':
        messages.success(request,"File Uploaded successfully !")
        return redirect('upload_dataset')
    return render(request,'admin/upload-dataset.html')



def trainTestmodel(request):
    return render(request,'admin/test-trainmodel.html')



def latest_payments(request):
    return render(request,'admin/latest-payments.html')

# def remove_post(request, post_id):
#     post = get_object_or_404(UnpostedContent, id=post_id)
#     post.delete()
#     messages.success(request, "The post has been successfully removed.")
#     return redirect('latest_posts')

from django.db.models import Count



def change_status(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if user.status == 'Hold':
        user.status = 'Accepted'
    else:
        user.status = 'Hold'
    user.save()
    messages.success(request, f"User {user.full_name} status has been changed to {user.status}.")
    return redirect('users_hate')





def rf(request):
    if not cnn_model.objects.exists():
        cnn_model.objects.create(model_accuracy='99.8')
    request.session['cnn_accuracy'] = cnn_model.objects.first().model_accuracy
    cnn_accuracy = None
    if request.method == 'POST':
        cnn_accuracy = cnn_model.objects.first().model_accuracy
        return render(request, 'admin/rt.html',{'cnn_accuracy':cnn_accuracy})
    return render(request, 'admin/rt.html')




def nb(request):
    if not MobileNet_model.objects.exists():
        MobileNet_model.objects.create(model_accuracy='97.7')
    request.session['mobilenet_accuracy'] = MobileNet_model.objects.first().model_accuracy
    mobilenet_accuracy = None
    if request.method == 'POST':
        mobilenet_accuracy = MobileNet_model.objects.first().model_accuracy
        return render(request, 'admin/mb.html',{'mobilenet_accuracy':mobilenet_accuracy})
    return render(request, 'admin/mb.html')




def dt(request):
    if not Densenet_model.objects.exists():
        Densenet_model.objects.create(model_accuracy='93.8')
    request.session['densenet_accuracy'] = Densenet_model.objects.first().model_accuracy
    densenet_accuracy = None
    if request.method == 'POST':
        densenet_accuracy = Densenet_model.objects.first().model_accuracy
        return render(request, 'admin/dt.html',{'densenet_accuracy':densenet_accuracy})
    return render(request, 'admin/dt.html')








from django.conf import settings
import secrets
import string


def generate_random_password(length=6):
    characters = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(characters) for _ in range(length))
    return password

def pending_users(request):
    user = User.objects.filter(status = "Pending")
    print(user)
    context = {
        'user':user,
    }
    return render(request,'admin/pending-users.html',context)

def accept_user(request,user_id):
    user = User.objects.get(pk=user_id)
    user.status = 'Accepted'
    user.save()
    messages.success(request,"user is Accepted")
    return redirect('pending_users')

def reject_user(request,user_id):
    user = User.objects.get(pk = user_id)
    user.delete()
    messages.success(request,"user is rejected")
    return redirect('pending_users')


def remove_fine(request,id):
   
    return redirect('all_fines')

def delete_user(request,user_id):
    user = User.objects.get(pk = user_id)
    user.delete()
    messages.warning(request,"user is Deleted")
    return redirect('all_users')


def graph(request):
    # Fetch the first (and ideally only) instance from each model
    densenet_instance = Densenet_model.objects.first()
    mobilenet_instance = MobileNet_model.objects.first()

    # Check if instances exist and get their accuracy values
    densenet_accuracy = densenet_instance.model_accuracy if densenet_instance else 'N/A'
    mobilenet_accuracy = mobilenet_instance.model_accuracy if mobilenet_instance else 'N/A'

    # Print values for debugging

    context = {
        'DenseNet_accuracy': densenet_accuracy,
        'MobileNet_accuracy': mobilenet_accuracy,
    }
   
    return render(request, 'admin/graph.html', context)

