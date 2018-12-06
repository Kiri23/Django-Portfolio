import pandas as pd
from books.models import Book

from django.apps import AppConfig

#  BOOK View EXCELTODB is the real deal this not work properly
class ExcelConfig(AppConfig):
    name = 'excel'


file = 'FileTest.xlsx'
xl = pd.ExcelFile(file)

print(xl.sheet_names[0])
sheet_name = xl.sheet_names[0]

df1 = xl.parse(sheet_name)

# print(df1.columns[1])

second_columns = df1.columns[2]


book = Book(title="titulo del libro en codigo", category="Salud", price=5)
book.save()

print(df1[second_columns])

print(df1['Sepal Length'])
print(df1['Sepal Width'])
print(df1['Petal Length'])
print(df1['ISBN'])

peta_length = df1['Petal Length']
Sepal_Width = df1['Sepal Width']
Sepal_Lenght = df1['Sepal Length']

print(peta_length)
print(Sepal_Lenght)
print(Sepal_Width)
