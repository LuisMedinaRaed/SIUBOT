from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import requests
import datetime
import os
from datetime import datetime, timedelta
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
import json
from datetime import datetime
from pathlib import Path
import time

def send_to_telegram(message):

    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)

# Cargar la configuración desde el archivo JSON
with open('config.json') as config_file:
    config = json.load(config_file)

apiToken = config['telegram']['apiToken']
chatID = config['telegram']['chatID']
username = config['guarani']['username']
password = config['guarani']['password']
nombre_materia = config['examen']['nombre_materia']
fecha_examen = config['examen']['fecha']

chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--headless')
#chrome_options.add_argument('--no-sandbox')
#chrome_options.add_argument('--disable-dev-shm-usage')

 # Crear una nueva instancia del driver de Chrome
driver = webdriver.Chrome(options=chrome_options,service=ChromeService(ChromeDriverManager().install()))

# La URL de la página de inicio de sesión
LOGIN_URL = 'https://guarani.unt.edu.ar/autogestion/acceso'

driver.get(LOGIN_URL)
driver.implicitly_wait(10)

# Localizamos los elementos del formulario de inicio de sesión
username_input = driver.find_element(By.ID, 'usuario')
password_input = driver.find_element(By.ID, 'password')
submit_button = driver.find_element(By.ID, 'login')

# Rellenamos el formulario de inicio de sesión
username_input.send_keys(username) ## Ingresar usuario del SIU GUARANI
password_input.send_keys(password) ## Ingresar contraseña del SIU GUARANI

# Hacemos clic en el botón de inicio de sesión
username_input.send_keys(Keys.RETURN)

driver.implicitly_wait(10)

# Comprobamos si el inicio de sesión ha sido correcto
if driver.current_url == 'https://guarani.unt.edu.ar/autogestion/inicio_alumno':
  print("Inicio de sesión correcto")
  driver.get('https://guarani.unt.edu.ar/autogestion/actuacion_provisoria')
  driver.implicitly_wait(10)
  time.sleep(1)
  if fecha_examen in driver.page_source: 
      send_to_telegram(f"YA ESTÁN LAS NOTAS DE {nombre_materia} EN ACTUACION PROVISORIA") ## INGRESAR MATERIA QUE SE RINDIO
  driver.get('https://guarani.unt.edu.ar/autogestion/historia_academica')
  driver.implicitly_wait(10)
  # Localizar el enlace por el atributo 'consulta'
  elemento_enlace = driver.find_element(By.CSS_SELECTOR, 'a[consulta="todo"]')
  elemento_enlace.click()
  time.sleep(1)
  if fecha_examen in driver.page_source: 
      send_to_telegram(f"YA ESTÁN LAS NOTAS DE {nombre_materia} EN HISTORIA ACADEMICA") ## INGRESAR MATERIA QUE SE RINDIO
else:
  print("Error al iniciar sesión")

cwd = os.getcwd()
filename = os.path.join(cwd, "SIUBOT.txt")

with open(filename, 'a') as f:
  f.write(f'{datetime.now()} - Se ejecutó el script \n')

# Cierra el navegador cuando hayas terminado de trabajar con él
driver.close()
