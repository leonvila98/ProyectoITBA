import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("full_data.csv")


def get_countries():
  next = '0'
  newcountries=[]

  while next != '3':
    print("""
    1. País"
    2. Nuevo país"
    3. Menú principal""")
    next = input("")
    if next == '1':
      country = input("Ingresá el nombre del país").capitalize()
      print("Pais agregado:", country)
      newcountries.append(country)
    elif next == '2':
      newcountries = []
    elif next == '3':
      return newcountries
    else:
      print("Opción erronea")

def get_time_frame():
  dates=['start', 'end']
  print("""
  1. Cambiar rango de tiempo
  2. Menú principal""")
  next = input("")
  if next == '1':
    dates[0] = input("Fecha de inicio (aaaa-mm-dd): ")
    dates[1] = input("Fecha de límite (aaaa-mm-dd): ")
  elif next == '2':
      return
  else:
    print("Opción erronea")
  return dates


def get_cases(selected_country):
  cases_dates = list(selected_country["data"]["date"])
  cases = list(selected_country["data"]["total_cases"])
  plt.plot(cases_dates,cases, linestyle="solid", label=selected_country["name"])

def get_deaths(selected_country):
  deaths_dates = list(selected_country["data"]["date"])
  deaths = list(selected_country["data"]["total_deaths"])
  plt.plot_date(deaths_dates,deaths, linestyle="solid", label=selected_country["name"])

def crear_cruces(first_country, second_country, option):  
  x_first_country = list(first_country["date"])
  x_second_country = list(second_country["date"])

  y_first_country = list(first_country[f"total_{option}"])
  y_second_country = list(second_country[f"total_{option}"])

  crucex = []
  crucey = []
  
  for i in range(1, len(x_first_country)):
    if (y_first_country[i] == y_second_country[i]) or (y_first_country[i] > y_second_country[i] and y_first_country[i-1] < y_second_country[i-1]) or (y_first_country[i] < y_second_country[i] and y_first_country[i-1] > y_second_country[i-1]):
      crucex.append(x_second_country[i])
      crucey.append(y_second_country[i])

  plt.plot(crucex,crucey, 'ro')
  plt.xticks(x_second_country[::100], rotation=60)
  

def programa():
  option = '0'
  countries = []
  dates = ['start', 'end']

  while option != '5':
    print("""
    GRAFICADOR COVID-19\n"
    Ingrese una opción para continuar:
    1. Países de consulta
    2. Rango de tiempo
    3. Consultar casos 
    4. Consultar muertes 
    5. Salir""")
    option = input("")

    if option == '1':
      countries = get_countries()
      print("Paises:", countries)
    elif option == '2':
      dates = get_time_frame() 
      for i in range(len(countries)): 
        countrydata = df[(df["date"].between(dates[0],dates[1]))&(df["location"] == countries[i])]
        countries[i] = {"name": countries[i], "data": countrydata}
    elif option == '3':
      for country in countries:
        get_cases(country)
      for i in range(len(countries)):
        for y in range(len(countries)):
            crear_cruces(countries[i]["data"], countries[y]["data"], "cases")
      plt.legend()
      plt.show()

    elif option == '4':
      for country in countries:
        get_deaths(country)
      for i in range(len(countries)-1):
        for y in range(len(countries)):
            crear_cruces(countries[i]["data"], countries[y]["data"], "deaths")
      plt.legend()
      plt.show()
    elif option == '5':
      break
    else:
      print("Opción inválida")
      break


programa()


