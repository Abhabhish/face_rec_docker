import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import numpy as np
import face_recognition
from .models import FaceData
import concurrent.futures


@csrf_exempt
def face(request):
    if request.method == 'POST':
        response = {}
        for root,dirs,files in os.walk('images'):
            for file in files:
                if '.jpg' in file.lower() or '.png' in file.lower() or '.jpeg' in file.lower():
                    img_path = os.path.join(root,file)
                    img = face_recognition.load_image_file(img_path)
                    fe = face_recognition.face_encodings(img)
                    if fe:
                        fe = fe[0]
                        all_faces = FaceData.objects.all()
                        for face in all_faces:
                            encoding = np.frombuffer(face.encodings, dtype=np.float64)
                            comparison = face_recognition.compare_faces([encoding], fe)
                            if all(comparison):
                                if img_path not in response:
                                    response[img_path] = []
                                response[img_path].append(face.file_path)
                        FaceData.objects.create(file_path=img_path, encodings=np.array(fe).tobytes())
        return JsonResponse(response)
    else:
        return JsonResponse({"error": "POST request required."}, status=400)

@csrf_exempt
def clean_db(request):
    if request.method == 'POST':
       FaceData.objects.all().delete()
       return JsonResponse({"msg": "DB deleted."})
    else:
        return JsonResponse({"error": "POST request required."}, status=400)




# ##########################
#         images = Image.objects.all()
#         hash_paths = {}
#         response_dict = {}

#         for image in images:
#             if image.hash in hash_paths:
#                 response_dict[image.path] = hash_paths[image.hash]
#                 hash_paths[image.hash].append(image.path)
#             else:
#                 hash_paths[image.hash] = [image.path]
#         return response_dict
# ##############################
#         images = Image.objects.all()
#         path_hash = {}
#         response_dict = {}

#         for image in images:
#             for k,v in path_hash:
#                 if v==image.hash:
#                     if image.path not in response_dict:
#                         response_dict[image.path]=[]
#                     response_dict[image.path].append(k)
#             path_hash[image.path] = image.hash
#         return response_dict
# #############################







# For aws lambda function implementation

    # if request.method == 'POST':

    #     img_paths = []
    #     for root,dirs,files in os.walk('images'):
    #         print(root,dirs,files)
    #         for file in files:
    #             if '.jpg' in file.lower() or '.png' in file.lower():
    #                 img_path = os.path.join(root,file)
    #                 img_paths.append(img_path)

    #     db_face_images = FaceData.objects.all()
    #     face_images_old = {}
    #     for face_image in db_face_images:
    #         encoding = np.frombuffer(face_image.encodings, dtype=np.float64)
    #         face_images_old[face_image.file_path] = encoding

    #     def get_face_encoding(img_path):
    #         img = face_recognition.load_image_file(img_path)
    #         fe = face_recognition.face_encodings(img)
    #         if fe:
    #             fe = fe[0]
    #             FaceData.objects.create(file_path=img_path, encodings=np.array(fe).tobytes())
    #             return [img_path,fe]

    #     def new_face_encodings(img_paths):
    #         result_dict = {}
    #         with concurrent.futures.ThreadPoolExecutor(max_workers=1) as executor:
    #             futures = {executor.submit(
    #                 get_face_encoding, img_path=img_path): img_path for img_path in img_paths}
    #             for future in concurrent.futures.as_completed(futures):
    #                 if future.result() is not None:
    #                    result_dict[future.result()[0]]=future.result()[1]
    #         return result_dict
                    
        
    #     face_images_new = new_face_encodings(img_paths)
    #     response_dict = {}
    #     for path_new ,encoding_new in face_images_new.items():
    #         for path_old,encoding_old in face_images_old.items():
    #             comparison = face_recognition.compare_faces([encoding_new], encoding_old)
    #             if all(comparison):
    #                 if path_new not in response_dict:
    #                     response_dict[path_new] = []
    #                 response_dict[path_new].append(path_old)
    #         face_images_old[path_new] = encoding_new
    #     return JsonResponse(response_dict)
    # else:
    #     return JsonResponse({"error": "POST request required."}, status=400)