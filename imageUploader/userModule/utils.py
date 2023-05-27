import os
import re


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


def saveImage(profile_image, imagepath):
    if not os.path.exists(imagepath):
        os.makedirs(imagepath)

    file_path = os.path.join(imagepath, profile_image.name)

    with open(file_path, 'wb') as destination:
        for chunk in profile_image.chunks():
            destination.write(chunk)
