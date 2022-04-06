from selenium import webdriver
import time
from bs4 import BeautifulSoup
import csv
import pandas as pd

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

# Ejecucion Metodos Extraccion
#getDespegarInformation()
#getTripAdvisorInformation()

# Cierre Selenium
driver.quit()

#Se Procesa la informacion del CSV
df = pd.read_csv('hoteles.csv', sep=",", header=None, encoding='latin1') #Lectura del CSV y su configuracion
df.columns =['Nombre', 'Precio'] #PD Columns
df = df.drop_duplicates(subset=['Nombre'], keep='first', inplace=False) #Se eliminan datos repetidos

#Se limpia el CSV
f = open("hoteles.csv", "w+")
f.truncate()
df.to_csv('hoteles.csv', sep=",", encoding='latin1', index=False, index_label=None, header=False)
f.close()

#Procesamiento De Datos Categoricos
def dataProcessing():

    df = pd.read_csv('hoteles.csv', sep=",", header=None, encoding='latin1')  # Lectura del CSV y su configuracion
    df.columns = ['Nombre', 'Precio']  # PD Columns
    #Procesamiento Categorico de Informaciòn

    #Precios Limites
    maxPriceCSV = 1000000.0
    minPriceCSV = 50000.0

    #Eliminaciòn de hoteles dentro de un rango maximo y minimo
    df = df.drop(df[df['Precio']> float(maxPriceCSV)].index) #Elimina Precios por encima del precio Maximo
    df = df.drop(df[df['Precio']< float(minPriceCSV)].index) #Elimina Precios por debajo del precio minimo

    #Hoteles despues de la limpieza
    print("----------------")
    print("La cantidad de hoteles son :")
    print(df.count())

    #Porcentajes
    hundredPercent = df['Precio'].max() #100%
    eightyPercent = (hundredPercent * 0.8) #80%
    sixtyPercent = ((eightyPercent * 0.6) / 0.8) #60%
    fortyPercent = ((sixtyPercent * 0.4) / 0.6) #40%
    twentyPercent = ((fortyPercent * 0.2) / 0.4) #20%
    ceroPercent = df['Precio'].min() #0%

    print("\n----------------")
    print("Porcentajes")
    print("----------------")
    print("100%") #100%
    print(hundredPercent)
    print("----------------")
    print("80%") #75%
    print(eightyPercent)
    print("----------------")
    print("60%") #50%
    print(sixtyPercent)
    print("----------------")
    print("40%") #25%
    print(fortyPercent)
    print("----------------") #0%
    print("20%")
    print(twentyPercent)
    print("----------------") #0%
    print("0%")
    print(ceroPercent)

    #Clasificacion Precios

    veryExpensiveHotels = df.drop(df[df['Precio'] > float(eightyPercent)].index)
    veryExpensiveHotels = df.drop(df[df['Precio'] < float(hundredPercent)].index)
    print(veryExpensiveHotels)

    expensiveHotels = df.drop(df[df['Precio'] > float(sixtyPercent)].index)
    expensiveHotels = df.drop(df[df['Precio'] < float(eightyPercent)].index)
    print(expensiveHotels)

    meanHotels = df.drop(df[df['Precio'] > float(fortyPercent)].index)
    meanHotels = df.drop(df[df['Precio'] < float(sixtyPercent)].index)
    print(meanHotels)

    cheapHotels = df.drop(df[df['Precio'] > float(twentyPercent)].index)
    cheapHotels = df.drop(df[df['Precio'] < float(fortyPercent)].index)
    print(cheapHotels)

    veryCheapHotels = df.drop(df[df['Precio']> float(ceroPercent)].index)
    veryCheapHotels = df.drop(df[df['Precio']< float(twentyPercent)].index)
    print(veryCheapHotels)


    """
    #Se imprimen la cantidad de hoteles por categoria
    print("\n--------------------------------")
    print("Cantidad De Hoteles Por Categoria")
    print("--------------------------------")
    print("Muy costosos: " + str(veryExpensiveHotels['Precio'].count()))
    print("----------------")
    print("Costosos: " + str(expensiveHotels['Precio'].count()))
    print("----------------")
    print("Medios: " + str(meanHotels['Precio'].count()))
    print("---------------")
    print("Hoteles Economicos: " + str(cheapHotels['Precio'].count()))
    print("---------------")
    print("Hoteles Muy Economicos: " + str(veryCheapHotels['Precio'].count()))

    #TOP 5

    #Se organiza la informacion dentro de cada categoria

    veryExpensiveHotels.sort_values(by='Precio', ascending=False, inplace=True)
    veryExpensiveHotelsTop = veryExpensiveHotels.head(n=5)

    expensiveHotels.sort_values(by='Precio', ascending=False, inplace=True)
    expensiveHotelsTop = expensiveHotels.head(n=5)

    meanHotels.sort_values(by='Precio', ascending=False, inplace=True)
    meanHotelsTop = meanHotels.head(n=5)

    cheapHotels.sort_values(by='Precio', ascending=False, inplace=True)
    cheapHotelsTop = cheapHotels.head(n=5)

    veryCheapHotels.sort_values(by='Precio', ascending=False, inplace=True)
    veryCheapHotelsTop = veryCheapHotels.head(n=5)


    #Se imprimen el top 5 hoteles por categoria
    print("\n--------------------------------")
    print("Top 5 Hoteles por Categoria")
    print("--------------------------------")
    print("Muy costosos: ")
    print(veryExpensiveHotelsTop)
    print("----------------")
    print("Costosos: ")
    print(expensiveHotelsTop)
    print("----------------")
    print("Medios: ")
    print(meanHotelsTop)
    print("---------------")
    print("Hoteles Economicos: ")
    print(cheapHotelsTop)
    print("---------------")
    print("Hoteles Muy Economicos: ")
    print(veryCheapHotelsTop)
    """


#Ejecucion Metodo Procesamiento De Datos Categoricos
dataProcessing()
