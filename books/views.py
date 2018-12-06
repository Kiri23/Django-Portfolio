from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .choices import price_choices, bedroom_choices, state_choices

from .models import Book
from realtors.models import Realtor


def index(request):
    books = Book.objects.order_by('-list_date').filter(is_published=True)
    paginator = Paginator(books, 6)
    page = request.GET.get('page')
    paged_book = paginator.get_page(page)

    context = {
        'listings': paged_book,
        'method': say
    }

    # excelToDb()
    return render(request, 'listings/listings.html', context)


def listing(request, listing_id):
    book = get_object_or_404(Book, pk=listing_id)

    context = {
        'listing': book
    }

    return render(request, 'listings/listing.html', context)


def search(request):
    queryset_list = Book.objects.order_by('-list_date')

    # Keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(
                description__icontains=keywords)

    # City
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)

    # State
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)

    # Bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

    # Price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price)

    context = {
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'listings': queryset_list,
        'values': request.GET
    }

    return render(request, 'listings/search.html', context)


import pandas as pd


def excelToDb(request):
    # file = 'FileTest.xlsx'
    # file = '/Users/Christiannogueras/Library/Mobile Documents/com~apple~CloudDocs/Temporero/FileTestCloud.xlsx'
    file = 'https://www.dropbox.com/s/8erg8l44p3ovt5q/FileTestCloud.xlsx?raw=1'
    # http = urllib3.PoolManager()
    # r = http.request('GET', file)
    # print(r.data)

    xl = pd.ExcelFile(file)

    sheet_name = xl.sheet_names[0]
    df1 = xl.parse(sheet_name)

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

    # realtor = Realtor(name="persona en el codigo",
    #                   phone="787-334-333", email="aa@hotmail.com")
    # realtor.save()
    # book = Book(realtor=realtor, title="titulo del libro en codigo",
    #             category="Salud", price=5, photo_main="photos/2018/10/28/ComunicaLibroDelete.jpg")
    # book.save()
    print('book must be saved')
    return redirect(index)


def say():
    print("hello world from HTML")
