from django.urls import path

from . import views

urlpatterns = [
    path('', views.excelToDb, name='excelToDb'),
    path('upload', views.uploadFileToDropbox, name='uploadToDropbox'),
    path('save', views.saveToDropbox, name='save'),
    path('fetch', views.fecthNewData, name='fetchNewData')
    # path('import', views.excelToDb, name='excelToDb')
]
