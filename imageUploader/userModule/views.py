from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User
from pymongo import MongoClient
from imageUploader import mongo
import json
import os

import re
from django.http import JsonResponse


def saveImage(profile_image, imagepath):
    if not os.path.exists(imagepath):
        os.makedirs(imagepath)

    file_path = os.path.join(imagepath, profile_image.name)

    with open(file_path, 'wb') as destination:
        for chunk in profile_image.chunks():
            destination.write(chunk)


@api_view(['POST'])
@csrf_exempt
def create_user(request):
    # Get the user data from the request.
    print("here")
    user_name = request.POST.get('user_name')
    user_email = request.POST.get('user_email')
    user_phone = request.POST.get('user_phone')
    profile_image = request.FILES.get('profile_image')
    user = User(user_name=user_name, user_email=user_email,
                user_phone=user_phone)
    try:
        validateUser(user_name, user_email, user_phone, profile_image)
    except Exception as e:
        return Response(status=400, data={'message': str(e)})

    print(user_name)
    imageDirectoryPath = 'upload/user/image/'
    saveImage(profile_image, imageDirectoryPath)
    # Create a new user in the database.
    document = {
        'user_name': user_name,
        'user_email': user_email,
        'user_phone': user_phone,
        'profile_image': imageDirectoryPath+profile_image.name
    }
    print(document)
    my_client = mongo.MongoDbClient
    dbname = my_client['image-uploader-database']
    collection_name = dbname["user_data"]
    collection_name.insert_one(document)
    count = collection_name.count_documents({})
    # Return a success response.
    return Response({'user created successfully'})


@api_view(['GET'])
@csrf_exempt
def fetch_all(request):
    my_client = mongo.MongoDbClient
    dbname = my_client['image-uploader-database']
    collection_name = dbname["user_data"]
    users = collection_name.find({})
    print(users)
    user_list = []
    for user in users:
        print('userval', user)
        user_data = {
            'user_name': user['user_name'] if 'user_name' in user else '',
            'user_email': user['user_email'] if 'user_email' in user else '',
            'user_phone': user['user_phone'] if 'user_phone' in user else '',
            'profile_image': user['profile_image'] if 'profile_image' in user else ''
        }
        print(user_data)
        user_list.append(user_data)
    return JsonResponse(user_list, safe=False)


def validateUser(user_name, user_email, user_phone, profile_image):
    if (len(user_name) > 30 or len(user_name) < 10):
        raise Exception('Invalid User Name')
    if (is_valid_email(user_email) is False):
        raise Exception('Invalid Email Address')
    if (is_valid_mobile(user_phone) is False):
        raise Exception('Invalid Mobile Number')
    if (is_valid_profile_image(profile_image) is False):
        raise Exception('Invalid Image Size [50 kb to 100Kb allowed]')


def is_valid_email(email):
    if (email is None or email == ''):
        return False
    match = re.match(
        r'^[a-zA-Z0-9.!#$%&\'*+\/=?^_`{|}~-]+@[a-zA-Z0-9-]+\.[a-zA-Z]+$', email)
    return match is not None


def is_valid_mobile(mobile):
    if (mobile is None or mobile == ''):
        return False
    match = re.match(r'^\d{10}$', mobile)
    return match is not None


def is_valid_profile_image(profile_image):
    print('is valid profile image')
    if (profile_image is None):
        return False
    if profile_image is not None:
        # image = Image.open(profile_image)
        file_size = profile_image.size
        size_in_kb = file_size / 1024  # Convert to kilobytes
        size_in_kb = int(size_in_kb)
        print(size_in_kb)
        if (size_in_kb < 50 or size_in_kb > 100):
            return False
        print(file_size)
    return True
