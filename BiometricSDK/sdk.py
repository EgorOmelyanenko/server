import base64

import requests
import json
import re
import datetime
import ast


class Biometric_Client:
    def __init__(self, url, port, subscription_key):
        """
        Initialize SDK client for simple work with API server using python.
        :param subscription_key: your subscription key that you can get from our manager.
        :param url: API server url. For example: "https://expasoft.com"
        :param port: API server port. For example: "11337"

        :type self: Biometric_Client
        :type subscription_key: str
        :type port: int
        :type url: str
        """
        self.url = url
        self.port = port
        self.subscription_key = subscription_key
        self.connection_string = url + ":" + str(port) + "/" + subscription_key + "/"
        self.client = requests.session()
        self.client.verify = False
        #self.client.cert = "./cacert.pem"

    def add_profile(self, name, birth_date, gender, tags=""):
        """
        Add new profile for client with current subscription key.
        :param name: person name. String. For example "Ivan Ivanovich Ivanov". No longer then 255 characters.
        :param birth_date: person birthday. String in format "DD.MM.YYYY". For example "01.01.2001"
        :param gender: person gender. Character 'm' for male and 'f' for female. For example "m".
        :param tags: string tags. Any string for additional profile info in simple format. No longer then 255 character.
        May be empty.
        :type name: str
        :type birth_date: str
        :type gender: chr
        :type tags: str
        :type self: Biometric_Client
        :return:
        * "error"  - error condition. 1 - result with error. 0 - result without error
        * "result" - if no error: id of new profile. Integer value. If have error then contains error string.
        :rtype: dict
        """
        if not (gender == 'm' or gender == 'f'):
            raise Exception("Wrong gender format. Must be 'm' for male or 'f' for female.")
        try:
            datetime.datetime.strptime(birth_date, '%d.%m.%Y')
        except Exception as e:
            raise Exception("Wrong birthday format. Must be 'DD.MM.YYYY'")
        if name == "":
            raise Exception("Empty name.")

        connection_string = self.connection_string + "add_profile"
        r = self.client.post(url=connection_string, data=json.dumps(
            {"name": name, "birth_date": birth_date, "gender": gender, "tags": tags}))

        res = re.split("ID:", r.text)
        if len(res) == 2:
            return {"error": 0, "result": int(res[1])}
        else:
            return {"error": 1, "result": r.text}

    def get_profiles_ids(self):
        """
        Get profiles ids for current client.
        :type self: Biometric_Client
        :return:
        * error  - error condition. 1 - result with error. 0 - result without error
        * result - if no error: list of profiles ids for current client. List of integer values. If have error then returns
        :rtype: dict
        """
        connection_string = self.connection_string + "get_profiles"
        r = self.client.get(url=connection_string)
        try:
            result = ast.literal_eval(r.text)
            return {"error": 0, "result": result}
        except Exception as e:
            return {"error": 1, "result": r.text}

    def enroll_profile_face(self, profile_id, filename):
        """
        Enroll new face sample for profile.
        :param profile_id: id of profile where face image will be enrolled. Integer value.
        :type profile_id: str
        :param filename: name of image file with person face. String value.
        :type filename: str
        :return:
        * error  - error condition. 1 - result with error. 0 - result without error
        * result - if no error: id of new image. Integer value. If have error then returns error string.
        :rtype: dict
        """
        connection_string = self.connection_string + str(profile_id) + "/enroll_profile_face"

        f = open(filename, 'rb')
        img = f.read()

        r = self.client.post(url=connection_string, files={"img": base64.b64encode(img)})
        res = re.split("ID:", r.text)

        if len(res) == 2:
            return {"error": 0, "result": int(res[1])}
        else:
            return {"error": 1, "result": r.text}

    def verify_profile_by_face(self, profile_id, filename):
        """
        :param profile_id: id of profile which face image will be enrolled. Integer value.
        :type profile_id: int
        :param filename: name of image file with person face. String value.
        :type filename: str
        :return:
        * error  - error condition. 1 - result with error. 0 - result without error
        * result - if no error: dictionary:
            ** "score" - float value between 0 and 1. Bigger value mean that verifying image most look like sample image
            that enrolled to profile before.
            ** "image_id" - id of image that most look like verifying image. Integer value.
        If have error then returns error string.
        :rtype: dict
        """
        connection_string = self.connection_string + str(profile_id) + "/verify_profile_face"
        f = open(filename, 'rb')
        img = f.read()

        r = self.client.post(url=connection_string, files={"img": base64.b64encode(img)})
        try:
            result = ast.literal_eval(r.text)
            return {"error": 0, "result": {"score": result[0], "image_id": result[1]}}
        except Exception as e:
            return {"error": 1, "result": r.text}

    def identify_profile_by_face(self, filename, top, threshold=0):
        """
        Identify person profile by face image.
        :param filename: name of image file with person face. String value.
        :type filename: str
        :param top: number of profiles which enrolled faces most look like identifying face image. Integer value.
        Maximum value is 50
        :type top: int
        :param threshold: threshold for score in identification function.
        :type threshold: float
        :return:
        * error  - error condition. 1 - result with error. 0 - result without error
        * result - if no error: list of dictionaries. Each item of list contains:
            ** "profile_id" - id of person profile.
            ** "score" - float value between 0 and 1. Bigger value mean that identifying image most look like sample image
            that was enrolled to profile before.
            ** "image_id" - id of image that most look like identifying image. Integer value. If image_id is zero that means
            that enrolled images for profile doesn't exists.
        If have error then return error string.
        :rtype: dict
        """
        if top <= 0:
            raise Exception("Top parameter must have positive value.")
        connection_string = self.connection_string + "identify_profile_face"
        f = open(filename, 'rb')
        img = f.read()
        r = self.client.post(url=connection_string,
                             files={"img": base64.b64encode(img), "top": str(top), "thresh": str(threshold)})
        try:
            result = ast.literal_eval(r.text)
            return {"error": 0, "result": [{"profile_id": i[0], "score": i[1], "image_id": i[2]} for i in result]}
        except Exception as e:
            return {"error": 1, "result": r.text}

    def get_profile_images_ids(self, profile_id):
        """
        Get enrolled images ids for profile.
        :param profile_id: id of person profile which images ids needed.
        :type profile_id: int
        :return:
        * error  - error condition. 1 - result with error. 0 - result without error
        * result - if no error: list of enrolled images ids for profile. List of integer values. If have error then returns
        error string.
        :rtype: dict
        """
        connection_string = self.connection_string + str(profile_id) + "/get_image_ids"
        r = self.client.post(url=connection_string)
        try:
            result = ast.literal_eval(r.text)
            return {"error": 0, "result": result}
        except Exception as e:
            return {"error": 1, "result": r.text}

    def get_profile_image(self, profile_id, image_id, filename=""):
        """
        Get profile image by id and save it to file.
        :param profile_id: id of person profile which image is needed. Integer value.
        :type profile_id: int
        :param image_id: id of person face image that was enrolled before. Integer value.
        :type image_id: int
        :param filename: filename where image will be saved. String value. May be empty value that mean that saving
        image not needed.
        :type filename: str
        :return:
        * error  - error condition. 1 - result with error. 0 - result without error
        * result - if no error: binary JPEG image represented as string. If have error then returns
        :rtype: dict
        """
        connection_string = self.connection_string + str(profile_id) + "/get_image/" + str(image_id)
        r = self.client.post(url=connection_string)
        try:
            res = json.loads(r.text)
            img = base64.b64decode(res["img"])
            if not filename == "":
                f = open(filename, "wb")
                f.write(img)
                f.close()
            return {"error": 0, "result": img}
        except Exception as e:
            return {"error": 1, "result": r.text}

    def delete_profile(self, profile_id):
        """
        Delete profile by id.
        :param profile_id: id of deleting profile. Integer value.
        :type profile_id: int
        :return:
        * error  - error condition. 1 - result with error. 0 - result without error
        * result - if no error: id of deleted profile. Integer value. If have error then returns error string.
        :rtype: dict
        """
        connection_string = self.connection_string + str(profile_id) + "/delete_profile"
        r = self.client.post(url=connection_string)
        if "deleted" not in r.text:
            return {"error": 1, "result": r.text}
        else:
            return {"error": 0, "result": int(re.findall("([0-9]+)", r.text)[0])}

    def delete_image(self, profile_id, image_id):
        """

        :param profile_id: id of profile. Integer value.
        :type profile_id: int
        :param image_id: id of deleting image.
        :type image_id: int
        :return:
        * error  - error condition. 1 - result with error. 0 - result without error
        * result - if no error: id of deleted image. Integer value. If have error then returns error string.
        :rtype: dict
        """
        connection_string = self.connection_string + str(profile_id) + "/delete_image/" + str(image_id)
        r = self.client.post(connection_string)
        if "deleted" not in r.text:
            return {"error": 1, "result": r.text}
        else:
            return {"error": 0, "result": int(re.findall("([0-9]+)", r.text)[0])}

    def enroll_profile_voice(self, profile_id, filename, extension):
        """
        Enroll new voice sample for profile.
        :param profile_id: id of profile where face image will be enrolled. Integer value.
        :type profile_id: int
        :param filename: name of audio file with person voice. String value. See main documentation for more format details.
        :type filename: str
        :param extension: audio file extension. Supported extensions:
        * WAV
        * MP3
        * OGG
        * FLAC
        :type extension: str
        :return:
        * error  - error condition. 1 - result with error. 0 - result without error
        * result - if no error: id of new voice sample. Integer value. If have error then returns error string.
        :rtype: dict
        """
        connection_string = self.connection_string + str(profile_id) + "/enroll_profile_voice"
        f = open(filename, 'rb')
        voice = f.read()
        r = self.client.post(url=connection_string, files={"voice": base64.b64encode(voice), "file_type": extension})
        res = re.split("ID:", r.text)
        if len(res) == 2:
            return {"error": 0, "result": int(res[1])}
        else:
            return {"error": 1, "result": r.text}

    def get_profile_voices_ids(self, profile_id):
        """
        Get enrolled voices ids for profile.
        :param profile_id: id of person profile which voices ids needed.
        :type profile_id: int
        :return:
        * error  - error condition. 1 - result with error. 0 - result without error
        * result - if no error: list of enrolled voices ids for profile. List of integer values. If have error then returns error string.
        :rtype: dict
        """
        connection_string = self.connection_string + str(profile_id) + "/get_voice_ids"
        r = self.client.post(url=connection_string)
        try:
            result = ast.literal_eval(r.text)
            return {"error": 0, "result": result}
        except Exception as e:
            return {"error": 1, "result": r.text}

    def verify_profile_by_voice(self, profile_id, filename, extension):
        """
        Verify person profile by face image.
        :param profile_id: id of profile which voice will be verified. Integer value.
        :type profile_id: int
        :param filename: name of audio file with person voice. String value. See main documentation for more format details.
        :type filename: str
        :param extension: audio file extension. Supported extensions:
        * WAV
        * MP3
        * OGG
        * FLAC
        :type extension: str
        :return:
        * error  - error condition. 1 - result with error. 0 - result without error
        * result - if no error: score of verification in interval from 0 to ~110. Float value.
        :rtype: dict
        """
        connection_string = self.connection_string + str(profile_id) + "/verify_profile_voice"
        f = open(filename, 'rb')
        voice = f.read()
        r = self.client.post(url=connection_string, files={"voice": base64.b64encode(voice), "file_type": extension})
        try:
            return {"error": 0, "result": float(r.text)}
        except Exception as e:
            return {"error": 1, "result": r.text}

    def identify_profile_by_voice(self, filename, top, extension, threshold=0):
        """
        Identify person profile by voice.
        :param filename: name of audio file with person voice. String value.
        :type filename: str
        :param top: number of profiles which enrolled voices most look like identifying voice. Integer value. Maximum value
        is 50
        :type top: int
        :param extension: audio file extension. Supported extensions:
        * WAV
        * MP3
        * OGG
        * FLAC
        :type extension: str
        :param threshold: hreshold for score in identification function.
        :type threshold: float
        :return:
        * error  - error condition. 1 - result with error. 0 - result without error
        * result - if no error: list of dictionaries. Each item of list contains:
            ** "profile_id" - id of person profile.
            ** "score" - float value between 0 and ~110. Bigger value mean that identifying voice most look like sample voice
            that was enrolled to profile before.
        If have error then return error string.
        :rtype: dict
        """
        if top <= 0:
            raise Exception("Top parameter must have positive value.")
        connection_string = self.connection_string + "identify_profile_voice"
        f = open(filename, 'rb')
        voice = f.read()
        r = self.client.post(url=connection_string, files={"voice": base64.b64encode(voice), "top": str(top),
                                                           "thresh": str(threshold), "file_type": extension})
        try:
            result = ast.literal_eval(r.text)
            return {"error": 0, "result": [{"profile_id": i[0], "score": i[1]} for i in result]}
        except Exception as e:
            return {"error": 1, "result": r.text}

    def get_profile_voice(self, profile_id, voice_id, filename=""):
        """
        Get profile voice sample by id and save it to file.
        :param profile_id: id of person profile which voice sample is needed. Integer value.
        :type profile_id: int
        :param voice_id: id of person voice sample that was enrolled before. Integer value.
        :type voice_id: int
        :param filename: filename where voice will be saved. String value. May be empty value that mean that saving voice not
        needed
        :type filename: str
        :return:
        * error  - error condition. 1 - result with error. 0 - result without error
        * result - if no error: binary wav file represented as string. If have error then returns error string.
        :rtype: dict
        """
        connection_string = self.connection_string + str(profile_id) + "/get_voice/" + str(voice_id)
        r = self.client.post(url=connection_string)
        try:
            res = json.loads(r.text)
            data = base64.b64decode(res["voice"])
            if not filename == "":
                f = open(filename, "wb")
                f.write(data)
                f.close()
            return {"error": 0, "result": data}
        except Exception as e:
            return {"error": 1, "result": r.text}

    def delete_voice(self, profile_id, voice_id):
        """
        Delete voice by id.
        :param profile_id: id of profile. Integer value.
        :type profile_id: int
        :param voice_id: id of deleting image.
        :type voice_id: int
        :return:
        * error  - error condition. 1 - result with error. 0 - result without error
        * result - if no error: id of deleted voice. Integer value. If have error then returns error string.
        :rtype: dict
        """
        connection_string = self.connection_string + str(profile_id) + "/delete_voice/" + str(voice_id)
        r = self.client.post(connection_string)
        if "deleted" not in r.text:
            return {"error": 1, "result": r.text}
        else:
            return {"error": 0, "result": int(re.findall("([0-9]+)", r.text)[0])}

    def predict_gender(self, filename):
        """
        Predict gender by face.
        :param filename: name of image file with person face. String value.
        :type filename: str
        :return:
        * error  - error condition. 1 - result with error. 0 - result without error
        * result - if no error: "Male" or "Female". String value. If have error then returns error string.
        :rtype: dict
        """
        connection_string = self.connection_string + "predict_gender"
        f = open(filename, 'rb')
        img = f.read()
        f.close()
        r = self.client.post(url=connection_string, files={"img": base64.b64encode(img)})
        if "Female" in r.text or "Male" in r.text:
            return {"error": 0, "result": r.text}
        else:
            return {"error": 1, "result": r.text}

    def predict_age(self, filename):
        """
        Predict age by face.
        :param filename: name of image file with person face. String value.
        :type filename: str
        :return:
        * error  - error condition. 1 - result with error. 0 - result without error
        * result - if no error: predicted age. Integer value. If have error then returns error string.
        :rtype: dict
        """
        connection_string = self.connection_string + "predict_age"
        f = open(filename, 'rb')
        img = f.read()
        f.close()
        r = self.client.post(url=connection_string, files={"img": base64.b64encode(img)})
        try:
            return {"error": 0, "result": int(r.text)}
        except Exception as e:
            return {"error": 1, "result": r.text}

    def detect_acustic_event(self, filename, extension):
        """
        Detect acustic evens in audio file. Such as: fire alarm, crying baby, breaking glass, gun shot, barking dog.
        Also it detects anomaly voices and give wary response.
        :param filename: name of audio file that will be used for acustic event detection
        :type filename: str
        :param extension: audio file extension. Supported extensions:
        * WAV
        * MP3
        * OGG
        * FLAC
        :type extension: str
        :return:
        * error  - error condition. 1 - result with error. 0 - result without error
        * result - if no error: list of names of detected acustic events. If have error then returns error string.
        :rtype: dict
        """
        connection_string = self.connection_string + "acustic_event"
        f = open(filename, 'rb')
        voice = f.read()
        f.close()
        r = self.client.post(url=connection_string, verify=True, files={"voice": base64.b64encode(voice), "file_type": extension})
        try:
            res = json.loads(r.text)
            return {"error": 0, "result": res}
        except Exception as e:
            return {"error": 1, "result": r.text}

    def detect_document(self, input_filename, output_filename=""):
        """
        Detect documents on photo. Such as Russian passport, Russian driver's license, Russian SNILS, international
        passport, car registration certificate.
        :param input_filename: path to input image.
        :type input_filename: str
        :param output_filename: path to output image that will be contains bounding boxes of detected documents. May be
        empty
        :type output_filename: str
        :return:
        * error  - error condition. 1 - result with error. 0 - result without error
        * result - if no error: Dictionary:
        ** img - binary jpg image.
        ** detects - names of detected documents.
        If have error then returns error string.
        :rtype:dict
        """
        connection_string = self.connection_string + "detect_document"
        f = open(input_filename, 'rb')
        img = f.read()
        f.close()
        r = self.client.post(url=connection_string, files={"img": base64.b64encode(img)})
        try:
            res = json.loads(r.text)
            img = base64.b64decode(res["img"])
            if output_filename is not "":
                with open(output_filename, "wb") as f:
                    f.write(img)
            return {"error": 0, "result": {"file": img, "detects": res["detects"]}}
        except Exception as e:
            return {"error": 1, "result": r.text}

    def detect_faces(self, filename):
        """
        Detect faces on image and return faces positions.
        :param filename: path to input image where faces needed to detect.
        :type filename: str
        :return:
        * error  - error condition. 1 - result with error. 0 - result without error
        * result - if no error: list of dictionaries with bounding boxes coordinates("top", "bottom", "left", "right").
                   If have error then returns error string.
        :rtype: dict
        """
        connection_string = self.connection_string + "detect_faces"
        f = open(filename, 'rb')
        img = f.read()
        f.close()
        r = self.client.post(url=connection_string, files={"img": base64.b64encode(img)})
        try:
            dets = json.loads(r.text)
            return {"error": 0, "result": dets}
        except Exception as e:
            return {"error": 1, "result": r.text}

    def get_aligned_faces(self, filename, prefix):
        """
        Detects faces on image. Aligned and cropped them then returns as binary jpg images with bounding boxes that
        contains faces positions in original image/
        :param filename: path to input image
        :type filename: str
        :param prefix: part of path to output files. It will be saved at 'prefix + str(n) + ".jpg"'.
        Example for "images/aligned" prefix with 2 faces detects: "images/aligned1.jpg", "images/aligned2.jpg"
        :type prefix: str
        :return:
        * error  - error condition. 1 - result with error. 0 - result without error
        * result - if no error: list of dictionaries:
        ** img - binary jpg image.
        ** bbox - bounding boxes coordinates("top", "bottom", "left", "right")
        If have error then returns error string.
        :rtype: dict
        """
        connection_string = self.connection_string + "get_aligned_faces"
        f = open(filename, 'rb')
        img = f.read()
        f.close()
        r = self.client.post(url=connection_string, files={"img": base64.b64encode(img)})
        try:
            faces = json.loads(r.text)
            dets = []
            for i, f in enumerate(faces):
                img = base64.b64decode(f[0])
                if not prefix == "":
                    with open(prefix + str(i) + ".jpg", "wb") as fl:
                        fl.write(img)
                dets.append({"img": img, "bbox": f[1]})
            return {"error": 0, "result": dets}
        except Exception as e:
            return {"error": 1, "result": r.text}

    def get_cropped_faces(self, filename, prefix):
        """
        Detects faces on image and crop them then returns as binary jpg images with bounding boxes that
        contains faces positions in original image.
        :param filename: path to input image
        :type filename: str
        :param prefix: part of path to output files. It will be saved at 'prefix + str(n) + ".jpg"'.
        Example for "images/aligned" prefix with 2 faces detects: "images/aligned1.jpg", "images/aligned2.jpg"
        :type prefix: str
        :return:
        * error  - error condition. 1 - result with error. 0 - result without error
        * result - if no error: list of dictionaries:
        ** img - binary jpg image.
        ** bbox - bounding boxes coordinates("top", "bottom", "left", "right")
        If have error then returns error string.
        :rtype: dict
        """
        connection_string = self.connection_string + "get_cropped_faces"
        f = open(filename, 'rb')
        img = f.read()
        f.close()
        r = self.client.post(url=connection_string, verify=True, files={"img": base64.b64encode(img)})
        try:
            faces = json.loads(r.text)
            dets = []
            for i, f in enumerate(faces):
                img = base64.b64decode(f[0])
                if not prefix == "":
                    with open(prefix + str(i) + ".jpg", "wb") as fl:
                        fl.write(img)
                dets.append({"img": img, "bbox": f[1]})
            return {"error": 0, "result": dets}
        except Exception as e:
            return {"error": 1, "result": r.text}

    def authenticate_profile_by_voice(self, profile_id, filename, extension, language, transcription):
        """
        Verify person profile by face image.
        :param profile_id: id of profile which voice will be verified. Integer value.
        :type profile_id: int
        :param filename: name of audio file with person voice. String value. See main documentation for more format details.
        :type filename: str
        :param extension: audio file extension. Supported extensions:
        * WAV
        * MP3
        * OGG
        * FLAC
        :type extension: str
        :param language: native language of record. Supported languages:
        * "ru-RU" - russian.
        * "en-EN" - american english.
        :type language: str
        :param transcription: transcription of numbers in record.
        :type transcription: str

        :return:
        * error  - error condition. 1 - result with error. 0 - result without error
        * result - if no error: score of verification in interval from 0 to ~110. Float value.
        :rtype: dict
        """
        connection_string = self.connection_string + str(profile_id) + "/authenticate_profile_by_voice"
        f = open(filename, 'rb')
        voice = f.read()
        r = self.client.post(url=connection_string, files={"voice": base64.b64encode(voice), "file_type": extension,
                                                           "language": language, "transcription": transcription})
        try:
            return {"error": 0, "result": float(r.text)}
        except Exception as e:
            return {"error": 1, "result": r.text}