from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from datetime import datetime
from pathlib import Path
import json

from selenium_utils import iniciar_sesion, seleccionar_modulo, ingresarATENEA, cambiarSegundaPestana
from mail_utils import enviar_mail

class Juicio:
    """
    Clase que representa un objeto Juicio con atributos asociados.

    Atributos:
    - id (str): Identificador único del juicio.
    - bd (str): Número de base de datos asociado al juicio.
    - ano (str): Año del juicio.
    - cuit (str): Número de CUIT asociado al demandado.
    - demandado (str): Nombre del demandado en el juicio.
    - cant_cuota (str): Cantidad de cuotas del plan de pago.
    - imp_cuota (str): Importe de cada cuota del plan de pago.
    - fecha_ini (str): Fecha de inicio del plan de pago.
    - mail (str): Dirección de correo electrónico asociada al juicio.
    """
    def __init__(self, id, bd, ano, cuit, demandado, cant_cuota, imp_cuota, fecha_ini, mail):
        """
        Inicializa un objeto Juicio con los atributos proporcionados.

        Parámetros:
        - id (str): Identificador único del juicio.
        - bd (str): Número de base de datos asociado al juicio.
        - ano (str): Año del juicio.
        - cuit (str): Número de CUIT asociado al demandado.
        - demandado (str): Nombre del demandado en el juicio.
        - cant_cuota (str): Cantidad de cuotas del plan de pago.
        - imp_cuota (str): Importe de cada cuota del plan de pago.
        - fecha_ini (str): Fecha de inicio del plan de pago.
        - mail (str): Dirección de correo electrónico asociada al juicio.
        """
        self.id = id
        self.bd = bd
        self.ano = ano
        self.cuit = cuit
        self.demandado = demandado
        self.cant_cuota = cant_cuota
        self.imp_cuota = imp_cuota
        self.fecha_ini = fecha_ini
        self.mail = mail

def crearArchivo(ruta):
    """
    Crea un archivo de texto con la fecha de creación, un título y un espacio para datos.

    Parámetros:
    - ruta: La ruta del archivo a crear o sobrescribir.
    """
    # Obtiene la fecha y hora actual en el formato deseado (día/mes/año)
    fecha_actual = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    # Contenido del archivo con fecha de creación, título y espacio para datos
    contenido = f"Fecha: {fecha_actual}\n\nEstado CUOTAS\n\n"

    # Abre el archivo en modo de escritura, creando uno nuevo si no existe o sobrescribiendo si ya existe
    with open(ruta, 'w') as archivo:
        archivo.write(contenido)

def cargar_configuracion(ruta):
    """
    Carga la configuración desde un archivo JSON en la ruta especificada.

    Parámetros:
    - ruta (str): La ruta del archivo JSON que contiene la configuración.

    Retorna:
    - dict: Un diccionario que representa la configuración cargada desde el archivo JSON.
    """
    with open(ruta, "r") as config_file:
        return json.load(config_file)

def buscar_juicio(driver, juicio, anio):
    """
    Realiza una búsqueda de un juicio en el sistema web de AFIP.

    Parámetros:
    - driver (WebDriver): Instancia del navegador web utilizada para la interacción.
    - juicio (str): Número de juicio que se desea buscar.
    - anio (str): Año asociado al juicio que se desea buscar.
    """
    driver.get("https://juridicos.afip.gob.ar/atenea/siraef/gestion/Consulta_Juicio_Num.asp")

    campo_juicio = driver.find_element(By.NAME, "juicio")
    campo_anio = driver.find_element(By.NAME, "anio")

    campo_juicio.clear()
    campo_anio.clear()

    campo_juicio.send_keys(juicio)
    campo_anio.send_keys(anio)

    driver.execute_script('traer_juicio()')

def procesar_juicios(self):
    """
    Procesa los juicios leyendo datos desde un archivo Excel y realizando las operaciones necesarias.

    Returns:
    - None
    """
    from excel_utils import formatear_datos_a_juicios, leer_datos_excel
  # Leer datos desde Excel
    datos_leidos = leer_datos_excel(self.ruta_archivo, "Hoja1")

    # Formatear datos a objetos Juicio
    juicios = formatear_datos_a_juicios(datos_leidos)

    # Cargar configuración desde el archivo JSON
    config_data = cargar_configuracion("config.json")

    # Leer las credenciales
    username = config_data["usuario"]
    password = config_data["contrasena"]

    # Crear una nueva instancia del driver de Chrome
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))

    iniciar_sesion(driver, username, password)
    ingresarATENEA(driver)
    cambiarSegundaPestana(driver)
    seleccionar_modulo(driver, "AADP0E0000", "2", "4")

    # Obtén la ruta al directorio actual

    directorio_actual = Path(__file__).resolve().parent.parent

    # Ruta al archivo de datos
    ruta_datos = directorio_actual / 'data'

    crearArchivo(ruta_datos / "estadoCuotas.txt")

    # Acceder a los objetos Juicio
    for juicio in juicios:
        buscar_juicio(driver, juicio.bd, juicio.ano)
        procesar_tabla_honorarios(driver, juicio)

    # Cerrar el navegador cuando hayas terminado de trabajar con él
    driver.quit()

def encontrar_tabla_cuota(driver):
    """
    Encuentra y devuelve la tabla que contiene la palabra "cuota" en la primera celda.

    Parameters:
        driver (WebDriver): El controlador de Selenium WebDriver que representa la sesión del navegador.

    Returns:
        bs4.element.Tag or None: Si se encuentra una tabla que cumple con el criterio, se devuelve el objeto BeautifulSoup
        que representa la tabla interna. Si no se encuentra ninguna tabla, se devuelve None.

    Raises:
        Exception: Captura cualquier excepción que pueda ocurrir durante el proceso y la imprime.
    """
    try:
        # Obtener el contenido HTML de la página
        html_content = driver.page_source

        # Crear un objeto BeautifulSoup
        soup = BeautifulSoup(html_content, 'html.parser')

        # Buscar todas las tablas en la página
        tablas = soup.find_all('table')

        # Iterar sobre las tablas y encontrar la que contiene la palabra "cuota" en la primera celda
        for tabla in tablas:
            filas = tabla.find_all('tr')
            if filas and 'cuota' in filas[0].text.lower():
                tabla_interna = tabla.find_all('table')[0]
                return tabla_interna
        # Si no se encuentra ninguna tabla que cumpla con el criterio
        return None

    except Exception as e:
        print(f"Error: {e}")
        return None

def procesar_tabla_honorarios(driver,juicio):
    """
    Procesa la tabla de honorarios de un juicio en el sistema web de AFIP.

    Parámetros:
    - driver (WebDriver): Instancia del navegador web utilizada para la interacción.
    - juicio (Juicio): Objeto Juicio que contiene la información del juicio.

    La función realiza los siguientes pasos:
    1. Encuentra y hace clic en el elemento del label asociado a "Honorarios Estimados / Regulados".
    2. Calcula las fechas de vencimiento de las cuotas sumando 1 mes a la fecha de inicio del plan de pago.
    3. Busca la tabla de cuotas en la página y la procesa.
    4. Escribe la información de las cuotas en un archivo de texto.
    5. Envia un mail recordatorio del pago de cuotas.

    La información de cada cuota incluye el número de cuota, fecha de vencimiento y si la cuota ya se venció.
    También verifica si la cuota fue pagada o no, basándose en la información de la tabla.

    El número de juicio se agrega al principio del archivo.

    El archivo de salida es "data/estadoCuotas.txt" y se abre en modo append para agregar información sin sobreescribir.
    """
    # Encontrar el elemento del label por su texto y hacer click
    label_honorarios = driver.find_element(By.XPATH, "//label[contains(text(), 'Honorarios Estimados / Regulados')]")
    label_honorarios.click()

    # Fecha de inicio del plan de pago
    fecha_inicio_plan_pago = juicio.fecha_ini

    # Número de cuotas
    numero_cuotas = juicio.cant_cuota

    # Calcular las fechas de vencimiento sumando 1 mes a la fecha de inicio para cada cuota
    fechas_vencimiento_cuotas = [fecha_inicio_plan_pago + timedelta(days=(i * 30)) for i in range(numero_cuotas)]

    # Obtener la fecha actual
    fecha_actual = datetime.now()

    soup = encontrar_tabla_cuota(driver)

    # Obtén la ruta al directorio actual

    directorio_actual = Path(__file__).resolve().parent.parent

    # Ruta al archivo de datos
    ruta_datos = directorio_actual / 'data'
    
     # Abrir el archivo en modo append para escribir al final sin sobreescribir
    with open(ruta_datos / "estadoCuotas.txt", "a") as archivo_salida:
        # Escribir el número de juicio
        archivo_salida.write(f"Demandado: {juicio.demandado} - Numero de Juicio: {juicio.bd}\n\n")

        # Iterar sobre las cuotas y escribir la información en el archivo
        for i, fila in enumerate(soup.select('tr')[1:], start=1):
            cuota_info = f"Cuota {i} ("

            # Obtener datos de la fila
            datos_fila = [td.text.strip() for td in fila.select('td')]

            # Obtener fecha de vencimiento de la cuota actual
            fecha_vencimiento = fechas_vencimiento_cuotas[i - 1]
            cuota_info += f"Fecha de vencimiento: {fecha_vencimiento.strftime('%d/%m/%Y')})\n"

            # Obtener la fecha de pago
            fecha_pago = datos_fila[4]

            # Agregar condiciones adicionales
            if fecha_actual > fecha_vencimiento and (not fecha_pago or fecha_pago == "&nbsp;"):
                cuota_info += "La cuota se vencio y no fue pagada.\n"
            elif fecha_pago and fecha_pago != "&nbsp;":
                cuota_info += "La cuota fue pagada.\n"
            elif fecha_actual <= fecha_vencimiento and (not fecha_pago or fecha_pago == "&nbsp;"):
                cuota_info += "La cuota aun no se ha vencido y no fue pagada.\n"

            cuota_info += "\n"

            # Escribir la información de la cuota en el archivo
            archivo_salida.write(cuota_info)
        
        enviar_mail(str(juicio.mail), str(juicio.id), str(juicio.bd))

    