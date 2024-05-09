from django.contrib import admin
from django.urls import path
from faceapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('face/', views.face, name='face'),
    path('clear_db/',views.clean_db,name='clear_db')
]
