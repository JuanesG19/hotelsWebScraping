from selenium import webdriver
import time
import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import csv
import gc
from itertools import zip_longest

# URL DE HOTELES

# BOOKING
booking = 'https://www.booking.com/searchresults.es.html?aid=376374&label=esrow-OtlvhU2CXhSVxek50Z_17wS267754636760%3Apl%3Ata%3Ap1%3Ap22.563.000%3Aac%3Aap%3Aneg%3Afi%3Atikwd-65526620%3Alp1029332%3Ali%3Adec%3Adm%3Appccp%3DUmFuZG9tSVYkc2RlIyh9YcUSe6BbHz0Ad_yDShFFSHQ&lang=es&sid=3c1a56ee40179313176cd2bb6dadb53c&sb=1&sb_lp=1&src=index&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Findex.es.html%3Faid%3D376374%3Blabel%3Desrow-OtlvhU2CXhSVxek50Z_17wS267754636760%253Apl%253Ata%253Ap1%253Ap22.563.000%253Aac%253Aap%253Aneg%253Afi%253Atikwd-65526620%253Alp1029332%253Ali%253Adec%253Adm%253Appccp%253DUmFuZG9tSVYkc2RlIyh9YcUSe6BbHz0Ad_yDShFFSHQ%3Bsid%3D3c1a56ee40179313176cd2bb6dadb53c%3Bsb_price_type%3Dtotal%26%3B&ss=Ibagu%C3%A9%2C+Colombia&is_ski_area=&checkin_year=2022&checkin_month=5&checkin_monthday=16&checkout_year=2022&checkout_month=5&checkout_monthday=17&group_adults=2&group_children=0&no_rooms=1&b_h4u_keep_filters=&from_sf=1&dest_id=-586582&dest_type=city&search_pageview_id=178ca56cff7600e4&search_selected=true'

# DESPEGAR
despegar = 'https://www.despegar.com.co/hoteles/?adjus&gclid=EAIaIQobChMI34qB6Yjl9gIVBojICh0fiwmjEAAYAiAAEgI_ufD_BwE&mktdata=kw%3Ddespegar%2520hoteles%26c%3D574414115743%26cc%3DCO%26mt%3De%26n%3Dg%26p%3D%26ap%3D%26d%3Dc%26dm%3D%26targetid%3Dkwd-18654789471%26campaignid%3D15854888810%26adgroupid%3D130785166303%26ExperimentId%3D%26locationid%3D1029332%26accountid%3D2593993521%26pr%3DG%26adjust_adgroup%3D130785166303%26adjust_campaign%3D15854888810%26adjust_t%3Dovd1mo_r45y7l_v9v5li%26adjust_creative%3D574414115743%26key%3DUT81AK9JAFEGJ4D69OVO6J673E%26adjust_tracker_limit%3D1000000000%26gclid%3DEAIaIQobChMI34qB6Yjl9gIVBojICh0fiwmjEAAYAiAAEgI_ufD_BwE%26id%3D20220327004822140405128019449595%26trackeame_user_id%3D12FE645FF1F916442636987873a79cdac-9f16-414d-ba55-4e8def7464c749189494'

# TRIPADVISOR
tripadvisor = 'https://www.tripadvisor.co/Hotels'

#Hoteles.com
hotelespuntocom = 'https://co.hoteles.com';

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
def getBookingInformation():
    print("-----------------BOOKING-----------------")
    driver.get(booking)
    time.sleep(2)

    hotels = driver.find_element_by_name('ss')
    hotels.send_keys(Keys.CONTROL, 'a')
    hotels.send_keys(Keys.BACKSPACE)
    hotels.send_keys(ciudad)

    time.sleep(3)
    confirmBtn = driver.find_element_by_class_name('cd1e09fdfe')
    confirmBtn.click()

    search = driver.find_element_by_xpath('//*[@id="left_col_wrapper"]/div[1]/div/div/form/div/div[6]/button')
    search.click()

    #BS4
    html_txt = driver.page_source
    soup = BeautifulSoup(html_txt, features="html.parser")

    nameBookingList = []
    noteBookingList = []
    priceBookingList = []

    print("-----------------------------------------------" + "\n")
    print("Nombre hoteles Booking")

    nombreHoteles = driver.find_elements_by_xpath('//div[@data-testid="title"]')

    for i in nombreHoteles:
        nameBookingList.append(i.text)
        print(i.text)
    print(len(nameBookingList))

    print("-----------------------------------------------")
    print("Calificacion en Booking:")
    # Rating
    noteBooking = driver.find_elements_by_xpath('//div[@data-testid="review-score"]//div[@class="b5cd09854e d10a6220b4"]')

    for n in noteBooking:
        noteBookingList.append(n.text)
        print(n.text)
    print(len(noteBookingList))

    #Precio
    priceBooking = driver.find_elements_by_xpath('//span[@class="fcab3ed991 bd73d13072"]')

    for m in priceBooking:
        priceBookingList.append(m.text)
        print(m.text)
    print(len(priceBookingList))

# Archivo CSV

    with open('hoteles.csv', 'w', encoding='UTF8', newline='') as file:

        writer = csv.writer(file)
        for w in range(0, len(nameBookingList)):
            writer.writerow([nameBookingList[w], priceBookingList[w], noteBookingList[w]])
        file.close()

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
        priceDespegarList.append(n.text)
        print(n.text)
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

    with open('hoteles.csv', 'a') as file:

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
            priceTripAdvisorList.append(m.text)

        time.sleep(4)
        # Archivo CSV
        with open('hoteles.csv', 'a') as file:

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
# getBookingInformation()
getDespegarInformation()
getTripAdvisorInformation()

# Cierre
driver.quit()