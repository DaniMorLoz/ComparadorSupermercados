import csv
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service

login_credentials = {
    'username': '',
    'password': ''
}
url_mercadona = "https://www.telecompra.mercadona.es/ns/entrada.php"
url_carrefour = "https://www.carrefour.es/supermercado"
url_dia = "https://www.dia.es/compra-online/login/singlelogin"

a,b = 'áéíóúüÁÉÍÓÚÜ','aeiouuAEIOUU'

def getListaMercadona(w):
    driver.implicitly_wait(2)
    driver.get(url_mercadona)
    time.sleep(3)
    for key, val in login_credentials.items():
        driver.find_element(By.ID,key).send_keys(val)
    driver.find_element(By.XPATH,'//input[@type="submit"]').click()
    
    driver.switch_to.frame('rightFrame')
    driver.find_element(By.CLASS_NAME,'clsTab').click()
    driver.find_element(By.CLASS_NAME,'celda25').click()

    driver.switch_to.default_content()
    driver.switch_to.frame('mainFrame')

    driver.find_elements
    lista = driver.find_element(By.CLASS_NAME,'tablaproductos').find_element(By.TAG_NAME,'tbody').find_elements(By.TAG_NAME,'tr')
    for elem in lista:
        nombre = elem.find_elements(By.XPATH,'.//td')[0].text.replace(",",".").translate(str.maketrans(a,b)).lower()
        try:
            precio = elem.find_elements(By.XPATH,".//td")[2].find_element(By.XPATH,'.//span[@class="precio_ud tdcenter"]').text.split(': ')[1].replace(",",".")
        except:
            precio = elem.find_elements(By.XPATH,".//td")[2].find_element(By.XPATH,'.//span[@class="tdcenter"]').text.replace(",",".")
        w.writerow([nombre,precio])

def getListaCarrefour(w):
    driver.get(url_carrefour)
    driver.find_element(By.ID,'onetrust-accept-btn-handler').click()
    driver.find_element(By.XPATH,'//span[@class="icon-cross-thin"]').click()
    driver.find_element(By.CLASS_NAME,'account-header').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@name="username" and @type="email"]')))
    driver.find_element(By.XPATH,'//input[@name="username" and @type="email"]').send_keys('')
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Continuar"]')))
    driver.find_element(By.XPATH,'//input[@value="Continuar"]').click()
    time.sleep(3)
    driver.find_elements(By.XPATH,'//input[@name="password"]')[-1].send_keys('')
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//input[@value="Continuar"]')))
    driver.find_element(By.XPATH,'//input[@value="Continuar"]').click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="list-header"]')))
    driver.find_element(By.XPATH,'//div[@class="list-header"]').click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//a[@title="Mis listas"]')))
    driver.find_element(By.XPATH,'//a[@title="Mis listas"]').click()
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="list-item__name"]')))
    driver.find_element(By.XPATH,'//div[@class="list-item__name"]').click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="list-detail__list-container"]')))
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/4);")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
    time.sleep(2)
    driver.execute_script("window.scrollTo(0, 3*document.body.scrollHeight/4);")
    time.sleep(2)
    secciones = driver.find_elements(By.XPATH,'//div[@class="list-detail__list-container"]')
    for seccion in secciones:
        productos = seccion.find_elements(By.CLASS_NAME,'list-detail__item')
        for producto in productos:
            nombre = producto.find_element(By.CLASS_NAME,'product-card__title').text.replace(",",".").translate(str.maketrans(a,b))
            precio = producto.find_element(By.CLASS_NAME,'product-card__price-per-unit').text.replace(",",".")
            w.writerow([nombre,precio])

def getListaDia(w):
    driver.get(url_dia)
    WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, 'onetrust-accept-btn-handler')))
    driver.find_element(By.ID,'onetrust-accept-btn-handler').click()
    driver.find_element(By.XPATH,'//input[@id="userName"]').send_keys('')
    driver.find_element(By.XPATH,'//input[@id="password"]').send_keys('')
    driver.find_element(By.XPATH,'//button[@id="btn-sct-login-btn-acceso"]').click()
    time.sleep(3)
    driver.get('https://www.dia.es/compra-online/my-account/saved-list/0069043884')
    elementos = driver.find_element(By.ID,'your_order').find_elements(By.XPATH,'.//td[@headers="header1"]')
    lista = []
    for elemento in elementos:
        lista.append(elemento.find_element(By.TAG_NAME,'a').get_attribute('href'))
    for url in lista:
        driver.get(url)
        nombre = driver.find_element(By.XPATH,'//h1[@itemprop="name"]').text.replace(",",".").translate(str.maketrans(a,b))
        precio = driver.find_element(By.XPATH,'//span[@class="average-price"]').text.replace(",",".")
        w.writerow([nombre,precio])


options = Options()
ua = UserAgent()
userAgent = ua.random
options.add_argument(f'user-agent={userAgent}')
s = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(options=options,service=s)

with open('results/results_carrefour.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    getListaCarrefour(writer)
with open('results/results_mercadona.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    getListaMercadona(writer)
with open('results/results_dia.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    getListaDia(writer)
driver.close()