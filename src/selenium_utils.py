from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

def iniciar_sesion(driver, username, password):
    """
    Inicia sesión en el sistema web de AFIP.

    Parámetros:
    - driver (WebDriver): Instancia del navegador web utilizada para la interacción.
    - username (str): Nombre de usuario para iniciar sesión.
    - password (str): Contraseña asociada al nombre de usuario.

    La función realiza los siguientes pasos:
    1. Navega a la página de inicio de sesión.
    2. Localiza los elementos del formulario de inicio de sesión.
    3. Ingresa el nombre de usuario y la contraseña.
    4. Envía el formulario para iniciar sesión.
    """
    driver.get('https://auth.afip.gob.ar/persona/')
    driver.implicitly_wait(10)

    username_input = driver.find_element(By.ID, 'user')
    password_input = driver.find_element(By.ID, 'password')

    username_input.send_keys(username)
    password_input.send_keys(password)
    username_input.send_keys(Keys.RETURN)

def ingresarATENEA(driver):
    """
    Inicia sesión en el sistema web de AFIP.

    Parámetros:
    - driver (WebDriver): Instancia del navegador web utilizada para la interacción.
    - username (str): Nombre de usuario para iniciar sesión.
    - password (str): Contraseña asociada al nombre de usuario.

    La función realiza los siguientes pasos:
    1. Navega a la página de inicio de sesión.
    2. Localiza los elementos del formulario de inicio de sesión.
    3. Ingresa el nombre de usuario y la contraseña.
    4. Envía el formulario para iniciar sesión.
    """
    driver.implicitly_wait(10)
    driver.execute_script('document.f0.submit()')

def seleccionar_modulo(driver, modulo_value, sistema_value, perfil_value):
    """
    Selecciona un módulo, sistema y perfil en el sistema web de AFIP.

    Parámetros:
    - driver (WebDriver): Instancia del navegador web utilizada para la interacción.
    - modulo_value (str): Valor del módulo a seleccionar.
    - sistema_value (str): Valor del sistema a seleccionar.
    - perfil_value (str): Valor del perfil a seleccionar.

    La función realiza los siguientes pasos:
    1. Selecciona el módulo, sistema y perfil según los valores proporcionados.
    2. Hace clic en el botón de ingreso al módulo.
    """   
    driver.implicitly_wait(50)
    select_modulo = Select(driver.find_element(By.NAME, "ctl00$VentanaPrincipal$lugarAccesoIng"))
    select_modulo.select_by_value(modulo_value)

    select_sistema = Select(driver.find_element(By.ID, "ctl00_VentanaPrincipal_sistemaIng"))
    select_sistema.select_by_value(sistema_value)

    select_perfil = Select(driver.find_element(By.ID, "ctl00_VentanaPrincipal_perfilIng"))
    select_perfil.select_by_value(perfil_value)

    boton_ingreso = driver.find_element(By.ID, "ctl00_VentanaPrincipal_ingreso")
    boton_ingreso.click()

def cambiarSegundaPestana(driver):
    """
    Cambia el control a la segunda pestaña del navegador.

    Parámetros:
    - driver (WebDriver): Instancia del navegador web utilizada para la interacción.

    La función obtiene la lista de identificadores de ventana y cambia el control a la segunda pestaña.
    """
    driver.implicitly_wait(10)
    # Obtener la lista de identificadores de ventana (handles)
    handles = driver.window_handles
    # Cambiar el control a la segunda pestaña
    driver.switch_to.window(handles[1])
