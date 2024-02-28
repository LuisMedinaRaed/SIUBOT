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
    """
    Envía un mensaje al chat de Telegram.

    Args:
        message (str): El mensaje a enviar.
    """
    apiURL = f'https://api.telegram.org/bot{apiToken}/sendMessage'

    try:
        response = requests.post(apiURL, json={'chat_id': chatID, 'text': message})
        print(response.text)
    except Exception as e:
        print(e)

def agregar_al_registro(mensaje):
    """
    Agrega un mensaje al archivo de registro.

    Args:
        mensaje (str): El mensaje a agregar al registro.
    """
    registro_filepath = os.path.join(os.getcwd(), "registro.txt")
    with open(registro_filepath, 'a') as registro_file:
        registro_file.write(f'{datetime.now()} - {mensaje}\n')     

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
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

# Crear una nueva instancia del driver de Chrome
driver = webdriver.Chrome(options=chrome_options,service=ChromeService(ChromeDriverManager().install()))

agregar_al_registro(f"Inicio de la ejecución")
print("Inicio de la ejecución")

# La URL de la página de inicio de sesión
LOGIN_URL = 'https://guarani.unt.edu.ar/autogestion/acceso'

driver.get(LOGIN_URL)
driver.implicitly_wait(10)

# Localizamos los elementos del formulario de inicio de sesión
username_input = driver.find_element(By.ID, 'usuario')
password_input = driver.find_element(By.ID, 'password')
submit_button = driver.find_element(By.ID, 'login')

# Rellenamos el formulario de inicio de sesión
username_input.send_keys(username) 
password_input.send_keys(password) 

# Hacemos clic en el botón de inicio de sesión
username_input.send_keys(Keys.RETURN)

driver.implicitly_wait(10)

# Comprobamos si el inicio de sesión ha sido correcto
if driver.current_url == 'https://guarani.unt.edu.ar/autogestion/inicio_alumno':
  print("Inicio de sesión correcto")
  agregar_al_registro(f"Inicio de sesión correcto")
  driver.get('https://guarani.unt.edu.ar/autogestion/actuacion_provisoria')
  driver.implicitly_wait(10)
  time.sleep(1)

  
  # Obtener la ruta del archivo de registro para Actuación Provisoria
  registro_actuacion_filepath = os.path.join(os.getcwd(), "registro_actuacion.json")

  # Intentar cargar el registro desde el archivo
  try:
      with open(registro_actuacion_filepath, 'r') as registro_actuacion_file:
          registro_actuacion = json.load(registro_actuacion_file)
  except FileNotFoundError:
      # Si el archivo no existe, crear uno vacío
      registro_actuacion = {}

  # Verificar si ya se envió el mensaje para Actuación Provisoria
  if nombre_materia not in registro_actuacion:
      if fecha_examen in driver.page_source:
        send_to_telegram(f"YA ESTÁN LAS NOTAS DE {nombre_materia} EN ACTUACION PROVISORIA")
        agregar_al_registro(f"YA ESTÁN LAS NOTAS DE {nombre_materia} EN ACTUACION PROVISORIA")
        # Registrar la materia en el archivo
        registro_actuacion[nombre_materia] = True
        with open(registro_actuacion_filepath, 'w') as registro_actuacion_file:
            json.dump(registro_actuacion, registro_actuacion_file)
      else:
          print(f"No se encontraron notas para {nombre_materia} en Actuacion Provisoria.") 
          agregar_al_registro(f"No se encontraron notas para {nombre_materia} en Actuacion Provisoria.")
  else:
      print(f"Ya se envió el mensaje para {nombre_materia} en Actuación Provisoria.")
      agregar_al_registro(f"Ya se envió el mensaje para {nombre_materia} en Actuación Provisoria.")

  driver.get('https://guarani.unt.edu.ar/autogestion/historia_academica')
  driver.implicitly_wait(10)
  # Localizar el enlace por el atributo 'consulta'
  elemento_enlace = driver.find_element(By.CSS_SELECTOR, 'a[consulta="todo"]')
  elemento_enlace.click()
  time.sleep(1)
  # Obtener la ruta del archivo de registro para Historia Academica
  registro_historia_filepath = os.path.join(os.getcwd(), "registro_historia.json")

  # Intentar cargar el registro desde el archivo
  try:
      with open(registro_historia_filepath, 'r') as registro_historia_file:
          registro_historia = json.load(registro_historia_file)
  except FileNotFoundError:
      # Si el archivo no existe, crear uno vacío
      registro_historia = {}

  # Verificar si ya se envió el mensaje para Historia Academica
  if nombre_materia not in registro_historia:
      # No se ha enviado el mensaje para Historia Academica, enviar y registrar
      driver.get('https://guarani.unt.edu.ar/autogestion/historia_academica')
      driver.implicitly_wait(10)
      # Localizar el enlace por el atributo 'consulta'
      elemento_enlace = driver.find_element(By.CSS_SELECTOR, 'a[consulta="todo"]')
      elemento_enlace.click()
      time.sleep(1)

      if fecha_examen in driver.page_source:
          send_to_telegram(f"YA ESTÁN LAS NOTAS DE {nombre_materia} EN HISTORIA ACADEMICA")
          agregar_al_registro(f"YA ESTÁN LAS NOTAS DE {nombre_materia} EN HISTORIA ACADEMICA")

          # Registrar la materia en el archivo
          registro_historia[nombre_materia] = True

          with open(registro_historia_filepath, 'w') as registro_historia_file:
              json.dump(registro_historia, registro_historia_file)
      else:
          print(f"No se encontraron notas para {nombre_materia} en Historia Academica.")
          agregar_al_registro(f"No se encontraron notas para {nombre_materia} en Historia Academica.")
  else:
      print(f"Ya se envió el mensaje para {nombre_materia} en Historia Academica.")
      agregar_al_registro(f"Ya se envió el mensaje para {nombre_materia} en Historia Academica.")
else:
  print("Error al iniciar sesión")

print(f"Fin de la ejecución\n")
agregar_al_registro(f"Fin de la ejecución\n")

# Cierra el navegador
driver.close()
