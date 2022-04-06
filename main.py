from selenium import webdriver
import time
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import csv
import pandas as pd
from sklearn import preprocessing
from sklearn.cluster import KMeans
from sklearn.metrics import pairwise_distances_argmin_min

# URL DE HOTELES

# DESPEGAR
despegar = 'https://www.despegar.com.co/hoteles/?adjus&gclid=EAIaIQobChMI34qB6Yjl9gIVBojICh0fiwmjEAAYAiAAEgI_ufD_BwE&mktdata=kw%3Ddespegar%2520hoteles%26c%3D574414115743%26cc%3DCO%26mt%3De%26n%3Dg%26p%3D%26ap%3D%26d%3Dc%26dm%3D%26targetid%3Dkwd-18654789471%26campaignid%3D15854888810%26adgroupid%3D130785166303%26ExperimentId%3D%26locationid%3D1029332%26accountid%3D2593993521%26pr%3DG%26adjust_adgroup%3D130785166303%26adjust_campaign%3D15854888810%26adjust_t%3Dovd1mo_r45y7l_v9v5li%26adjust_creative%3D574414115743%26key%3DUT81AK9JAFEGJ4D69OVO6J673E%26adjust_tracker_limit%3D1000000000%26gclid%3DEAIaIQobChMI34qB6Yjl9gIVBojICh0fiwmjEAAYAiAAEgI_ufD_BwE%26id%3D20220327004822140405128019449595%26trackeame_user_id%3D12FE645FF1F916442636987873a79cdac-9f16-414d-ba55-4e8def7464c749189494'

# TRIPADVISOR
tripadvisor = 'https://www.tripadvisor.co/Hotels'

#-------------------------------------------------------
# Comienzo App
print("-----------------------------------------------")
print("Bienvenido al WebScrapper de Hoteles:")
print("-----------------------------------------------" + "\n")
print("Digite el nombre de la ciudad:")
ciudad = input();
print("-----------------------------------------------" + "\n")

# Inicializacion de Drivers
driver = webdriver.Chrome('./chromedriver.exe')
driver.maximize_window()


# Obtencion de informacion Booking
def getDespegarInformation():
    print("-----------------DESPEGAR-----------------")

    driver.get(despegar)
    time.sleep(2)

    date = driver.find_element_by_class_name('sbox5-switch-svg  ')
    date.click()
    time.sleep(1)

    hotel = driver.find_element_by_class_name('input-tag')

    hotel.click()
    time.sleep(2)
    hotel.send_keys(ciudad)

    time.sleep(2)
    confirmHotel = driver.find_element_by_class_name('item-text')
    confirmHotel.click()

    time.sleep(2)
    searchBtn = driver.find_element_by_class_name('sbox5-btn-svg')
    searchBtn.click()

    #BS4
    html_txt = driver.page_source
    soup = BeautifulSoup(html_txt, features="html.parser")

    time.sleep(2)
    cookies = driver.find_element_by_xpath('//div[@class="lgpd-banner"]//a[@class="lgpd-banner--button eva-3-btn -white -md"]')
    cookies.click()

    time.sleep(2)
    moreResultsBtn = driver.find_element_by_xpath('//eva-button//span[@class="-md -default eva-3-btn-ghost"]')
    moreResultsBtn.click()
    time.sleep(3)

    nameDespegarList = []
    priceDespegarList = []
    ratingHotelList = []

    #Nombre Hotel
    print("-----------------------------------------------" + "\n")
    print("Nombre de los hoteles Despegar")
    print("-----------------------------------------------")

    nombreHoteles = driver.find_elements_by_xpath('//div[@class="cluster-content"]//div[@class="offer-card-title"]')

    for i in nombreHoteles:
        nameDespegarList.append(i.text)
        print(i.text)
    print(len(nameDespegarList))
    # Precio

    print("-----------------------------------------------")
    print("Precio del Hotel en Despegar:")
    print("-----------------------------------------------")

    priceDespegar = driver.find_elements_by_xpath('//div[@class="pricebox-value-container"]//div[@class="pricebox-value"]//span[@class="pricebox-big-text"]')

    for n in priceDespegar:
        cantidad = float(n.text.replace(".",""))
        priceDespegarList.append(cantidad)
        print(cantidad)
    print(len(priceDespegarList))
    #print("-----------------------------------------------")
    #print("Rating del Hotel en Despegar:")
    # Precio
    #noteDespegar = soup.find_all('span', class_='rating-text')

    #for n in noteDespegar:
     #   ratingHotelList.append(n.text)
      #  print(n.text)
    #print(len(ratingHotelList))

    # Archivo CSV

    with open('hoteles.csv', 'w', newline='') as file:

        writer = csv.writer(file)
        for w in range(0, len(nameDespegarList)):
            writer.writerow([nameDespegarList[w], priceDespegarList[w]])
        file.close()
    time.sleep(3)
def getTripAdvisorInformation():
    print("------Tripadvisor------")

    driver.get(tripadvisor)
    time.sleep(2)

    inputHotel = driver.find_element_by_xpath('//input[@class="fhEMT _G B- z _J Cj R0"]')
    inputHotel.click()
    time.sleep(2)
    typeHotel = driver.find_element_by_xpath('//input[@class="fhEMT _G B- z _J Cj R0"]')
    typeHotel.click()
    typeHotel.send_keys(ciudad)
    time.sleep(2)
    recomendationHotel = driver.find_element_by_xpath('//a[@class="bPaPP w z _S _F Wc Wh Q B- _G"]')
    recomendationHotel.click()

    sectionHotel = driver.find_element_by_xpath('//a[@class="ebMYO Ra _S z _Z w o v _Y Wh k _T ddFHE"]')
    sectionHotel.click()

    # BS4
    html_txt = driver.page_source
    soup = BeautifulSoup(html_txt, features="html.parser")

    # Listas
    nameTripAdvisorList = []
    priceTripAdvisorList = []

    # Busqueda
    numeroPaginas = 4

    #----------AQUI COMIENZAN LAS PAGINAS--------------

    for i in range(1, numeroPaginas):

        time.sleep(4)

        # Busca Nombre y Precio
        nombreHoteles = driver.find_elements_by_xpath('//a[@data-clicksource="HotelName"]')
        priceTripAdvisor = driver.find_elements_by_xpath('//div[@data-clickpart="chevron_price"]')

        time.sleep(4)
        # Muestra Nombre
        for n in nombreHoteles:
            nameTripAdvisorList.append(n.text)
        # Muestra Precio
        for m in priceTripAdvisor:
            priceStr = str(m.text)
            price = priceStr.replace("$", "")
            price2 = price.replace(" ", "")
            cantidad =  float(price2.replace(".", ""))
            priceTripAdvisorList.append(cantidad)
        time.sleep(4)
        # Archivo CSV
        with open('hoteles.csv', 'a', newline='') as file:

            writer = csv.writer(file)
            for w in range(0, len(nameTripAdvisorList)):
                writer.writerow([nameTripAdvisorList[w], priceTripAdvisorList[w]])
            file.close()

        time.sleep(2)
        # Click al iguiente boton
        siguientePg = driver.find_element_by_xpath('//a[@data-page-number="' + str(i + 1) + '"]')
        siguientePg.click()
        time.sleep(4)

    print(len(nameTripAdvisorList))
    print(len(priceTripAdvisorList))

# Ejecucion
#getBookingInformation()
#getDespegarInformation()
#getTripAdvisorInformation()

# Cierre Selenium
driver.quit()

#----------------------------------------o--------------------------------------------

#LECTURA PANDAS
df = pd.read_csv('hoteles.csv', sep=",", header=None, encoding='latin1') #Lectura del CSV y su configuracion
df.columns =['Nombre', 'Precio'] #PD Columns

#Procesamiento de Informaciòn

#Precios Limites
maxPriceCSV = 1000000.0
minPriceCSV = 50000.0

#Eliminaciòn de hoteles dentro de un rango maximo y minimo
df = df.drop(df[df['Precio']> float(maxPriceCSV)].index) #Elimina Precios por encima del precio Maximo
df = df.drop(df[df['Precio']< float(minPriceCSV)].index) #Elimina Precios por debajo del precio minimo

#Clasificacion Precios
maxPrice = df['Precio'].max() #100%
minPrice = df['Precio'].min() #1%
meanPrice = ((maxPrice + minPrice) / 2) #50%
meanUpperPrice = ((maxPrice + meanPrice) / 2) #75%
meanLowerPrice = ((minPrice + meanPrice) / 2) #25%

print("----------------")
print("Categorias")
print("----------------")
print("Max Price")
print(maxPrice)
print("----------------")
print("Mean Upper Price")
print(meanUpperPrice)
print("----------------")
print("Mean Price")
print(meanPrice)
print("----------------")
print("Mean Lower Price")
print(meanLowerPrice)
print("----------------")
print("Min Price")
print(minPrice)

#Clasificacion Precios

expensiveHotels = df.drop(df[df['Precio']> float(meanUpperPrice)].index)
expensiveHotels = df.drop(df[df['Precio']< float(maxPrice)].index)

modestHotels = df.drop(df[df['Precio']> float(meanPrice)].index)
modestHotels = df.drop(df[df['Precio']< float(meanUpperPrice)].index)

meanHotels = df.drop(df[df['Precio']> float(meanLowerPrice)].index)
meanHotels = df.drop(df[df['Precio']< float(meanPrice)].index)

cheapHotels = df.drop(df[df['Precio']> float(minPrice)].index)
cheapHotels = df.drop(df[df['Precio']< float(meanLowerPrice)].index)

print("\n--------------------------------")
print("Cantidad De Hoteles Por Categoria")
print("--------------------------------")
print("Hoteles Costos")
print(expensiveHotels.count(axis=0))
print("----------------")
print("Hoteles Precio Moderado")
print(modestHotels.count(axis=0))
print("----------------")
print("Hoteles Precio Medio")
print(meanHotels.count(axis=0))
print("----------------")
print("Hoteles Economicos")
print(cheapHotels.count(axis=0))


