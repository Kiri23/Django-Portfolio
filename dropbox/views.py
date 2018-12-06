from django.shortcuts import render, HttpResponse
from django.conf import settings
from django.http import JsonResponse
from .models import Excel
from django.utils import timezone

import pandas as pd
import requests
from threading import Thread
from io import StringIO
import json
import time

from openpyxl import load_workbook
from io import BytesIO

"""
  Decorator function to start a new thread
"""


def start_new_thread(function):
    def decorator(*args, **kwargs):
        t = Thread(target=function, args=args, kwargs=kwargs)
        t.daemon = True
        t.start()
    return decorator


def link_account(request):
    print("parte importante")
    print(settings.APP_KEY)
    print(settings.APP_SECRET)
    app_key = settings.APP_KEY
    app_secret = settings.APP_SECRET

    # flow = dropbox.client.DropboxOAuth2FlowNoRedirect(app_key, app_secret)
    # authorize_url = flow.start()
    # print ('1. Go to: ' + authorize_url)
    # print ('2. Click "Allow" (you might have to log in first)')
    # print ('3. Copy the authorization code.')
    # code = raw_input("Enter the authorization code here: ").strip())

    # # This will fail if the user enters an invalid authorization code
    # access_token, user_id = flow.finish(code)
    # client = dropbox.client.DropboxClient(access_token)
    # print ('linked account: ', client.account_info())

    # print ("---------One Time Process Done---------")
    # print ("\n")

    print("Your access token is:", settings.DROPBOX_TOKEN)

    # You need to save this access_token obtained in some text file.
    # and then refer to upload.py


def uploadFileToDropbox(request):
    '''
    https://dropbox.github.io/dropbox-api-v2-explorer/#files_upload
    This api explorer generate this code
    '''
    url = "https://content.dropboxapi.com/2/files/upload"

    headers = {
        "Authorization": "Bearer " + settings.DROPBOX_TOKEN,
        "Content-Type": "application/octet-stream",
        "Dropbox-API-Arg": "{\"path\":\"/FileTestFromCodigo.xlsx\",\"mode\":{\".tag\":\"overwrite\"}}"
    }
    # Esto se repite abajo file
    url_file = 'https://www.dropbox.com/s/8erg8l44p3ovt5q/FileTestCloud.xlsx?raw=1'
    file = requests.get(url_file, allow_redirects=True)
    # data = open(file.content, "rb").read()
    r = requests.post(url, headers=headers, data=file.content)
    print(r)
    # ################ READ Workbook
    # wb=load_workbook(filename=BytesIO(file.content))
    # sheet = wb.active
    # print (sheet['F1'].value)
    # sheet['F2'] = "Titulo hecho en codigo from python"
    # wb.save("FileTestFromCodigo.xlsx")


# Create your views here.
def excelToDb(request):

    # file = 'FileTest.xlsx'
    # file = '/Users/Christiannogueras/Library/Mobile Documents/com~apple~CloudDocs/Temporero/FileTestCloud.xlsx'
    # http = urllib3.PoolManager()
    # r = http.request('GET', file)
    # print(r.data)
    longWait()
    watchfordog()
    xl = download()
    sheet_name = xl.sheet_names[0]
    df1 = xl.parse(sheet_name)
    print (df1.to_string())
    peta_length = df1['Petal Length']
    Sepal_Width = df1['Sepal Width']
    Sepal_Lenght = df1['Sepal Length']
    isbn = df1['ISBN']
    titulo = df1['Titulo']
    departarmento = df1['Departamento']
    cantidad = df1['Cantidad']

    print(peta_length)
    print(Sepal_Lenght)
    print(Sepal_Width)
    print(isbn)
    print(titulo)
    print(departarmento)
    print(cantidad)

    # Change Excel cell
    # titulo[0] = "Changing a cell in Pandas DB"
    # Save Excel To Local file with PD
    writer = pd.ExcelWriter('XlsExcel.xls')
    df1.to_excel(writer, sheet_name)
    writer.save()
    print("Finally Save")

    # realtor = Realtor(name="persona en el codigo",
    #                   phone="787-334-333", email="aa@hotmail.com")
    # realtor.save()
    # book = Book(realtor=realtor, title="titulo del libro en codigo",
    #             category="Salud", price=5, photo_main="photos/2018/10/28/ComunicaLibroDelete.jpg")
    # book.save()
    print('book must be saved')
    # return redirect(index)


def saveExcel():
    writer = pd.ExcelWriter('XLSexcel.xls')
    df1.to_excel(writer, sheet_name)
    writer.save()
    print("Finally Save")


def saveToDropbox():
    # global date_modified_past
    # global date_modified_present

    print('printing date from past')
    print(date_modified_past)
    print("Date from present in server")
    print(date_modified_present)
    print('testing if theyre equal ', date_modified_past == date_modified_present)

    url = "https://content.dropboxapi.com/2/files/upload"

    headers = {
        "Authorization": "Bearer " + settings.DROPBOX_TOKEN,
        "Content-Type": "application/octet-stream",
        "Dropbox-API-Arg": "{\"path\":\"/testDirectory/FileTestFromCodigo.xlsx\",\"mode\":{\".tag\":\"overwrite\"}}"
    }
    # Esto se repite abajo file
    # url_file = 'https://www.dropbox.com/s/8erg8l44p3ovt5q/FileTestCloud.xlsx?raw=1'

    # file = requests.get(url_file, allow_redirects=True)
    data = open('./testDirectory/FileTestFromCodigo.xlsx', "rb").read()
    # dbug
    # print (data)
    # debug
    r = requests.post(url, headers=headers, data=data)  # file.content
    jsonr = r.json()
    date_modified_past = date_modified_present  # swap values,global variable
    date_modified_present = jsonr['server_modified']
    print("Date from server present")
    print(date_modified_present)
    print("date from past ", date_modified_past)

#
# This is my attemp to be the main method
def fecthNewData(request, debug = True):
    if (debug):
        debugFetchNewData()
    # The file to search
    searchQuery = "FileTestFromCodigo"
    # search in dropbox for the searQuery
    searchResponse = searchFile(searchQuery, debug = False)
    # parse the datetime of the first match that got in the response
    strDatetime = searchResponse["matches"][0]["metadata"]["server_modified"]
    # Compare if the datetime of the file is different from the last time
    isTheFileModified = compareDatetime(strDatetime,debug = True)
    if (isTheFileModified):
        print("fecthNewData: Archivo Modificado")
        # Check what is modified in the file
        compareTwoFileDf(debug = True)

    return JsonResponse(isTheFileModified, safe=False)
    # return HttpResponse(date_modified_present)


def searchFile(nameOfFile: str, debug = False):
    '''
        This function search file in dropbox.

        :param nameOfFile: The name of the file to search 
        :type nameOfFile: string
        :return: The response in Json format
    '''
    url = "https://api.dropboxapi.com/2/files/search"
    headers = {
        "Authorization": "Bearer B54iI51sVOIAAAAAAAAAIvznsQP2LKP3rZXSVTtcVMu1fAB6LjI5jPls_B1tEDU1",
        "Content-Type": "application/json"
    }
    data = {
        "path": "",
        "query": nameOfFile
    }
    r = requests.post(url, headers=headers, data=json.dumps(data))
    responseJsonData = r.json()
    if (debug):
        print("searchFile: Json Response: \n", 
        json.dumps([responseJsonData], indent=4, sort_keys=True))
    return responseJsonData


def compareDatetime(strDatetime, debug = False):

    date_modified_past = getLatestDateTimeFromDb()
    date_modified_present = strDatetime
    if (debug):
        print(f"compareDatetime: datetime past: {date_modified_past}")
        print(f"compareDatetime: datetime present: {date_modified_present}")
    # If both string are not empty check if they are equal
    if (date_modified_past and date_modified_present):
        if not (date_modified_past == date_modified_present):
            print("compareDatetime: Saving dateTime")
            datePastDb = Excel(date_modified_past = date_modified_present)
            datePastDb.save()
            return True  # La fecha de los archivos ha cambiado
        else:
            return False  # La fecha de los archivos no ha cambiado
    else:
        print("compareDatetime: One of the Datetime was empty. Most likely datetime past. Running again the method")

    return False  # Una de las dos fechas fue empty o None(null)

# Get the latest values that is not null
# obj= Model.objects.filter(date_modified_past__isnull = True).latest('date_modified_past')

def getLatestDateTimeFromDb(debug = False):
    latest_datetime_notNull = Excel.objects.filter(date_modified_past__isnull = False).latest('date_modified_past')
    latest_datetimeStr = timezone.localtime(latest_datetime_notNull.date_modified_past).strftime("%Y-%m-%dT%H:%M:%SZ")
    if (debug):
        print(f"getLatestDateTimeFromDb: datetime coming from db {latest_datetimeStr}")
    return latest_datetimeStr

def getLatestFileDfFromDb(debug = False):
    latest_file_notNull = Excel.objects.filter(old_fileStr__isnull = False)  
    latest_file_notNull = list(latest_file_notNull)[-1].old_fileStr 
    # print("latest file not null: ",latest_file_notNull)
    latestFileDf = pd.read_csv(StringIO(latest_file_notNull))
    if (debug):
        print("getLatestFileDfFromDb: Latest dtaframe from db: ", latestFileDf.to_string())
    return  latestFileDf


@start_new_thread
def compareTwoFileDf(debug = False):

    old_fileDf = getLatestFileDfFromDb()
    present_fileDF1 = download()
    sheet_name = present_fileDF1.sheet_names[0]
    dataFrame = present_fileDF1.parse(sheet_name)
    present_fileDf = dataFrame
    # Check if dataframe is not empty 
    if not (old_fileDf.empty):
        if not (present_fileDf.equals(old_fileDf)):
            if (debug):                
                print("compareTwoFileDf: Los dos archivos se suponen que no sean iguales")
                print("compareTwoFileDf: old File pandas: ", old_fileDf.to_string())
                print("compareTwoFileDf: present File pandas: ", present_fileDf.to_string())
            datePastDb = Excel(old_fileStr = present_fileDf.to_csv())
            datePastDb.save()
            print("compareTwoFileDf: Archivos guardado en base de dato")
            detectChanges(present_fileDf, old_fileDf, debug = True)
    else:
        print("compareTwoFileDf: olfd_fileDF was empty")

    peta_length = dataFrame['Petal Length']
    # print(peta_length)
    # print(present_fileDf.equals(old_fileDf))


"""
 The download takes times is better if I do this Asynchronously to not block
 the UI for the user
"""
# @start_new_thread
def download():
    fileUrl = 'https://www.dropbox.com/s/bp83npagpmfui48/FileTestFromCodigo.xlsx?raw=1'
    file = pd.ExcelFile(fileUrl)
    return file
# me quede aqui. detectar cambios en dataframe
def detectChanges(file1: pd.DataFrame, file2: pd.DataFrame, debug = False):
    print("metodo detect change")
    if (debug):
        print(f"detectChanges: Detectar cambios en file1: {file1}")
        print(f"detectChanges: Detectar cambios en file2: {file2}")
    # detectar si hay una actualizacion. e.g si no hay mas row 
    # detectar si se añadio un nuevo record 
    # detectar si se hicieron las dos cosas. actualizacion y añadir
    

def debugFetchNewData():
    print("debugFetchNewData: Latest Datetime from db ",getLatestDateTimeFromDb())
    print ("debugFetchNewData: Latest dataframe from db: ", getLatestFileDfFromDb())

@start_new_thread
def longWait():
    print("Entering a Long wait simulated")
    for item in range(0, 10):
        time.sleep(1)
        if item == 9:
            print("end of looop")


# ######### Wtach Dogg
import sys
import logging
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler, FileSystemEventHandler
class EventHandler(FileSystemEventHandler):
    def on_any_event(self, event):
        print("EVENT")
        print(event.event_type)
        print(event.src_path)
        print()
        saveToDropbox()


@start_new_thread
def watchfordog():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = './testDirectory'
    event_handler = EventHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    time.sleep(120)
    observer.stop()
    observer.join()
    print("End listening for chagening file ")
