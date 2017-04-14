from BiometricSDK.sdk import *
_Client = Biometric_Client(url='https://expasoft.com', port=2133,
                                        subscription_key='9fc9474b4bd16b492276eee41763a3cb')
def add_profile(name, birth=None, gender=None, tag=None):
    result = _Client.add_profile(name, '01.01.1111', 'm', tags="")
    return result

def del_profile(id):
    result = _Client.delete_profile(id)['error']
    return result
