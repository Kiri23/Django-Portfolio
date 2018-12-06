from array import *
import pandas as pd
T = [[10, 12, 15], [6, 10, 16], [3, 5, 10], [8, 12, 17],
     [4, 7, 12], [3, 4, 6], [5, 8, 13], [5, 7, 10]]
alcance = {}
media = {}
for idx, r in enumerate(T):
    a = r[0]
    m = r[1]
    b = r[2]
    # print(f" A = {a} \n M = {m} \n B= {b} \n")
    alcance['Actividad ' + str(idx)] = (((b - a) / 6) ** 2)
    # print(f" Alcance: {alcance} \n ")
    media['Actividad ' + str(idx)] = ((a + b + (4 * m)) / 6)
    # print(f" Media: {media} \n ")
    # print("Nueva Tarea \n")

print(pd.DataFrame([alcance, media], index=['Alcance', 'Media']))

# print(pd.DataFrame(media))

# 2d Array of the data
# data = [alcance,media]
# print (data)
# print(pd.DataFrame(data, columns=['Alcance', 'Media']) )
my_df = pd.DataFrame(data=[4, 5, 6, 7], index=range(0, 4), columns=['A'])
# print(pd.DataFrame(my_df))
