from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User
from imageUploader import mongo
import json

from django.http import JsonResponse
from . import utils


@api_view(['POST'])
@csrf_exempt
def create_user(request):
    user_name = request.POST.get('user_name')
    user_email = request.POST.get('user_email')
    user_phone = request.POST.get('user_phone')
    profile_image = request.FILES.get('profile_image')
    try:
        utils.validateUser(user_name, user_email, user_phone, profile_image)
    except Exception as e:
        return Response(status=400, data={'message': str(e)})

    print(user_name)
    imageDirectoryPath = 'upload/user/image/'
    utils.saveImage(profile_image, imageDirectoryPath)
    # Create a new user in the database.
    document = {
        'user_name': user_name,
        'user_email': user_email,
        'user_phone': user_phone,
        'profile_image': imageDirectoryPath+profile_image.name
    }
    print(document)
    my_client = mongo.MongoDbConnectionClient
    dbname = my_client['image-uploader-database']
    collection_name = dbname["user_data"]
    collection_name.insert_one(document)
    return Response({'user created successfully'})


@api_view(['GET'])
@csrf_exempt
def fetch_all(request):
    my_client = mongo.MongoDbConnectionClient
    dbname = my_client['image-uploader-database']
    collection_name = dbname["user_data"]
    users = collection_name.find({})  # fetch all documents from collection
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
