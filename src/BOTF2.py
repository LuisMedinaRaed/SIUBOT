from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import requests
import time
import datetime
import os

def send_to_telegram(message):

    apiToken = '' ## Ingresar Token del BOT
    chatID = '' ## Ingresar ID del chat
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# La URL de la página de inicio de sesión
LOGIN_URL = 'https://guarani.unt.edu.ar/autogestion/acceso'

# Creamos una instancia de Chrome y cargamos la página de inicio de sesión
driver = webdriver.Chrome('chromedriver',chrome_options=chrome_options)
driver.get(LOGIN_URL)
driver.implicitly_wait(10)

# Localizamos los elementos del formulario de inicio de sesión
username_input = driver.find_element(By.ID, 'usuario')
password_input = driver.find_element(By.ID, 'password')
submit_button = driver.find_element(By.ID, 'login')

# Rellenamos el formulario de inicio de sesión
username_input.send_keys('') ## Ingresar usuario del SIU GUARANI
password_input.send_keys('') ## Ingresar contraseña del SIU GUARANI

# Hacemos clic en el botón de inicio de sesión
username_input.send_keys(Keys.RETURN)

driver.implicitly_wait(10)

# Comprobamos si el inicio de sesión ha sido correcto
if driver.current_url == 'https://guarani.unt.edu.ar/autogestion/inicio_alumno':
  print("Inicio de sesión correcto")
  driver.get('https://guarani.unt.edu.ar/autogestion/actuacion_provisoria')
  driver.implicitly_wait(10)
  if "22/12/2022" in driver.page_source: ## INGRESAR FECHA DEL EXAMEN
      send_to_telegram("YA ESTÁN LAS NOTAS DE **") ## INGRESAR MATERIA QUE SE RINDIO
else:
  print("Error al iniciar sesión")

cwd = os.getcwd()
filename = os.path.join(cwd, "SIUBOT.txt")

with open(filename, 'a') as f:
  f.write(f'{datetime.datetime.now()} - Se ejecutó el script \n')

# Cierra el navegador cuando hayas terminado de trabajar con él
driver.close()
