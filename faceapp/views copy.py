import os
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import numpy as np
import face_recognition
from .models import FaceData

@csrf_exempt
def face(request):
    all_facedata = FaceData.objects.all()
    response = []
    if request.method == 'POST':
        try:
            file_path = 'images/a.png'
            img = face_recognition.load_image_file(file_path)
            fe = face_recognition.face_encodings(img)
            if fe:
                fe = fe[0]
            else:
                return JsonResponse(response, safe=False)
            for face_data in all_facedata: 
                encoding = np.frombuffer(face_data.encodings, dtype=np.float64)
                distance = face_recognition.face_distance([encoding], fe)
                threshold = 0.5
                if distance[0] < threshold:
                    response.append({"file_path": face_data.file_path, "distance": distance[0]})
            FaceData.objects.create(file_path=file_path, encodings=np.array(fe).tobytes())
            return JsonResponse(response, safe=False)
        except:
            return JsonResponse(response, safe=False)
    else:
        return JsonResponse({"error": "POST request required."}, status=400)

#####
