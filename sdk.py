from BiometricSDK.sdk import *
_Client = Biometric_Client(url='https://expasoft.com', port=2133,
                                        subscription_key='9fc9474b4bd16b492276eee41763a3cb')
def add_profile(name, birth=None, gender=None, tag=None):
    result = _Client.add_profile(name, '01.01.1111', 'm', tags="")
    return result

def del_profile(id):
    result = _Client.delete_profile(id)['error']
    return result

def ident_profile():
    imgName=r'srvimg/img.jpg'
    imgName0 = r'srvimg/currentPhoto0.jpg'
    _Client.get_aligned_faces(imgName, "srvimg/currentPhoto")
    result = _Client.identify_profile_by_face(imgName0, 1, 0)
    return result

def get_profile_imgs_id(id):
    result = _Client.get_profile_images_ids(id)
    return result

def get_profile_image(profile_id,image_id, filename):
    result = _Client.get_profile_image(profile_id, image_id, filename)
    return result