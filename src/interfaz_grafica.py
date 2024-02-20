import customtkinter
from customtkinter import filedialog
import os
from PIL import Image
import json
from pathlib import Path

from excel_utils import es_archivo_excel
from juicio_utils import procesar_juicios

class App(customtkinter.CTk):
    """
    Clase principal que representa la aplicación ESTJURAED BOT.

    Esta clase hereda de customtkinter.CTk, la cual proporciona una interfaz gráfica personalizada.
    La aplicación tiene tres secciones principales: 'Home', 'Estado Juicios' y 'Configuración'.
    Permite cargar un archivo, ejecutar un script, cambiar la apariencia y gestionar la configuración.

    Attributes:
        ruta_archivo (str): La ruta al archivo seleccionado para cargar.
        toplevel_window: Ventana superior utilizada para mostrar mensajes de error.
        imagen_logo: Imagen del logotipo de la aplicación.
        imagen_logo_estjuraed: Imagen del logotipo de EstJuraEd.
        imagen_ejecutar: Imagen para el botón de ejecutar.
        imagen_seleccionar_archivo: Imagen para el botón de seleccionar archivo.
        imagen_detener_ejecucion: Imagen para el botón de detener ejecución.
        imagen_home: Imagen para el botón de la página principal.
        imagen_estado_cuotas: Imagen para el botón de estado de cuotas.
        imagen_configuracion: Imagen para el botón de configuración.
        imagen_guardar: Imagen para el botón de guardar configuración.
        frame_navegacion: Marco de navegación que contiene botones de navegación.
        frame_navegacion_label: Etiqueta de título en el marco de navegación.
        frame_navegacion_boton_home: Botón de navegación para la página principal.
        frame_navegacion_boton_estado_juicios: Botón de navegación para el estado de juicios.
        frame_navegacion_boton_configuracion: Botón de navegación para la configuración.
        frame_navegacion_menu_apariencia: Menú desplegable para cambiar la apariencia.
        home_frame: Marco principal de la página principal.
        home_frame_large_image_label: Etiqueta grande para la imagen del logotipo de EstJuraEd en la página principal.
        home_frame_boton_cargar: Botón para cargar archivos en la página principal.
        home_frame_label_archivo: Etiqueta que muestra la ruta del archivo seleccionado en la página principal.
        home_frame_boton_ejecutar: Botón para ejecutar la aplicación en la página principal.
        estado_juicios_frame: Marco para la sección de estado de juicios.
        estado_juicios_text_widget: Widget de texto para mostrar el estado de juicios.
        configuracion_frame: Marco para la sección de configuración.
        configuracion_frame_label_titulo: Etiqueta de título en la sección de configuración.
        configuracion_frame_label_usuario: Etiqueta para el campo de usuario en la sección de configuración.
        configuracion_frame_label_contrasena: Etiqueta para el campo de contraseña en la sección de configuración.
        configuracion_frame_label_correo: Etiqueta para el campo de correo en la sección de configuración.
        configuracion_frame_label_contrasena_correo: Etiqueta para el campo de contraseña del correo en la sección de configuración.
        configuracion_frame_entry_usuario: Campo de entrada para el usuario en la sección de configuración.
        configuracion_frame_entry_contrasena: Campo de entrada para la contraseña en la sección de configuración.
        configuracion_frame_entry_correo: Campo de entrada para el correo en la sección de configuración.
        configuracion_frame_entry_contrasena_correo: Campo de entrada para la contraseña del correo en la sección de configuración.
        configuracion_frame_boton_guardar: Botón para guardar la configuración en la sección de configuración.

    Methods:
        __init__: Inicializa la aplicación y configura su interfaz gráfica.
        seleccionar_frame: Selecciona y muestra el frame correspondiente según el nombre proporcionado.
        evento_boton_home: Evento asociado al botón 'Home'.
        evento_boton_estado_cuotas: Evento asociado al botón 'Estado Cuotas'.
        evento_boton_configuracion: Evento asociado al botón 'Configuración'.
        evento_cambio_apariencia: Cambia la apariencia visual de la interfaz gráfica.
        cargar_archivo: Abre un cuadro de diálogo para seleccionar un archivo y guarda la ruta del archivo seleccionado.
        cargar_resultado: Carga el contenido del archivo 'data/estadoCuotas.txt' en el widget Text de la interfaz gráfica.
        iniciar_aplicacion: Inicia el script, carga datos desde un archivo Excel, procesa la información y actualiza la interfaz.
        guardar_informacion: Guarda la información de usuario, contraseña, correo y contraseña del correo en un archivo JSON.
        cargar_informacion: Carga la información de usuario, contraseña, correo y contraseña del correo desde un archivo JSON.
        abrir_errorArchivo: Abre una ventana de error en caso de que se intente ejecutar sin cargar un archivo.
        abrir_errorExcel: Abre una ventana de error si el archivo seleccionado no es un archivo de Excel válido.
    """
    def __init__(self, *args, **kwargs):
        """
        Inicializa la aplicación ESTJURAED BOT.

        Parámetros:
        - args: Argumentos adicionales.
        - kwargs: Argumentos clave adicionales.

        Retorna:
        - None
        """
        super().__init__(*args, **kwargs)

        self.title("ESTJURAED BOT")

        # Obtén la ruta al directorio actual
        directorio_actual = Path(__file__).resolve().parent.parent

        # Ruta al archivo de datos
        ruta_datos = directorio_actual / 'data'

        # Ruta al directorio de imágenes
        ruta_imagenes = directorio_actual / 'images'

        # Ruta al directorio del script
        ruta_script = Path(__file__).resolve().parent

        self.iconbitmap(ruta_imagenes / "first_icon.ico")

        ancho = 700
        alto = 500
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry('{}x{}+{}+{}'.format(ancho, alto, x, y))

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.imagen_logo = customtkinter.CTkImage(light_image=Image.open(os.path.join(ruta_imagenes, "logo_light.png")),
                                                 dark_image=Image.open(os.path.join(ruta_imagenes, "logo_dark.png")), size=(30, 30)) 
        self.imagen_logo_estjuraed = customtkinter.CTkImage(Image.open(os.path.join(ruta_imagenes, "logo_estjuraed.png")), size=(500, 150))
        self.imagen_ejecutar = customtkinter.CTkImage(Image.open(os.path.join(ruta_imagenes, "ejecutar.png")), size=(20, 20))
        self.imagen_seleccionar_archivo = customtkinter.CTkImage(Image.open(os.path.join(ruta_imagenes, "seleccionar.png")), size=(20, 20))
        self.imagen_detener_ejecucion = customtkinter.CTkImage(Image.open(os.path.join(ruta_imagenes, "detener.png")), size=(20, 20))
        self.imagen_home = customtkinter.CTkImage(light_image=Image.open(os.path.join(ruta_imagenes, "home_dark.png")),
                                                 dark_image=Image.open(os.path.join(ruta_imagenes, "home_light.png")), size=(20, 20))
        self.imagen_estado_cuotas = customtkinter.CTkImage(light_image=Image.open(os.path.join(ruta_imagenes, "cuotas_light.png")),
                                                 dark_image=Image.open(os.path.join(ruta_imagenes, "cuotas_dark.png")), size=(20, 20))
        self.imagen_configuracion = customtkinter.CTkImage(light_image=Image.open(os.path.join(ruta_imagenes, "configuracion_light.png")),
                                                 dark_image=Image.open(os.path.join(ruta_imagenes, "configuracion_dark.png")), size=(20, 20))
        self.imagen_guardar = customtkinter.CTkImage(light_image=Image.open(os.path.join(ruta_imagenes, "guardar.png")))

        # Crear frame de navegación
        self.frame_navegacion = customtkinter.CTkFrame(self, corner_radius=0)
        self.frame_navegacion.grid(row=0, column=0, sticky="nsew")
        self.frame_navegacion.grid_rowconfigure(4, weight=1)

        self.frame_navegacion_label = customtkinter.CTkLabel(self.frame_navegacion, text="  ESTJURAED BOT", image=self.imagen_logo,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.frame_navegacion_label.grid(row=0, column=0, padx=20, pady=20)

        self.frame_navegacion_boton_home = customtkinter.CTkButton(self.frame_navegacion, corner_radius=0, height=40, border_spacing=10, text="Pagina Principal",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.imagen_home, anchor="w", command=self.evento_boton_home)
        self.frame_navegacion_boton_home.grid(row=1, column=0, sticky="ew")

        self.frame_navegacion_boton_estado_juicios = customtkinter.CTkButton(self.frame_navegacion, corner_radius=0, height=40, border_spacing=10, text="Estado Juicios",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.imagen_estado_cuotas, anchor="w", command=self.evento_boton_estado_cuotas)
        self.frame_navegacion_boton_estado_juicios.grid(row=2, column=0, sticky="ew")

        self.frame_navegacion_boton_configuracion = customtkinter.CTkButton(self.frame_navegacion, corner_radius=0, height=40, border_spacing=10, text="Configuracion",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.imagen_configuracion, anchor="w", command=self.evento_boton_configuracion)
        self.frame_navegacion_boton_configuracion.grid(row=3, column=0, sticky="ew")

        self.frame_navegacion_menu_apariencia = customtkinter.CTkOptionMenu(self.frame_navegacion, values=["Light", "Dark", "System"],
                                                                command=self.evento_cambio_apariencia)
        self.frame_navegacion_menu_apariencia.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # Crear frame home
        self.home_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.home_frame.grid_columnconfigure(0, weight=1)

        self.home_frame_large_image_label = customtkinter.CTkLabel(self.home_frame, text="", image=self.imagen_logo_estjuraed)
        self.home_frame_large_image_label.grid(row=0, column=0, padx=20, pady=10)

        self.home_frame_boton_cargar = customtkinter.CTkButton(self.home_frame, text="Cargar Archivo", image=self.imagen_seleccionar_archivo, compound="right", command=self.cargar_archivo)
        self.home_frame_boton_cargar.grid(row=1, column=0, padx=20, pady=10)

        self.home_frame_label_archivo = customtkinter.CTkLabel(self.home_frame, text="Archivo seleccionado: Ninguno")
        self.home_frame_label_archivo.grid(row=2, column=0, padx=20, pady=10)

        self.home_frame_boton_ejecutar = customtkinter.CTkButton(self.home_frame, text="Ejecutar", image=self.imagen_ejecutar, compound="right", command=self.iniciar_aplicacion)
        self.home_frame_boton_ejecutar.grid(row=3, column=0, padx=20, pady=10)

        # Crear frame estado juicios
        self.estado_juicios_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.estado_juicios_text_widget = customtkinter.CTkTextbox(self.estado_juicios_frame, wrap="word", height=500, width=450)
        self.estado_juicios_text_widget.grid(row=0, column=0, padx=20, pady=10)
        self.cargar_resultado()
        
        self.toplevel_window = None

        # Crear frame configuracion
        self.configuracion_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        self.configuracion_frame_label_titulo = customtkinter.CTkLabel(self.configuracion_frame, text="Configuración", font=("Helvetica", 20, "bold"))
        self.configuracion_frame_label_titulo.grid(row=0, column=0, columnspan=2, pady=20)  # Columnspan para ocupar dos columnas

        self.configuracion_frame_label_usuario = customtkinter.CTkLabel(self.configuracion_frame, text="Usuario:")
        self.configuracion_frame_label_contrasena = customtkinter.CTkLabel(self.configuracion_frame, text="Contraseña:")
        self.configuracion_frame_label_correo = customtkinter.CTkLabel(self.configuracion_frame, text="Correo:")
        self.configuracion_frame_label_contrasena_correo = customtkinter.CTkLabel(self.configuracion_frame, text="Contraseña del Correo:")

        self.configuracion_frame_entry_usuario = customtkinter.CTkEntry(self.configuracion_frame)
        self.configuracion_frame_entry_contrasena = customtkinter.CTkEntry(self.configuracion_frame, show="*")  # El atributo show="*" oculta la contraseña
        self.configuracion_frame_entry_correo = customtkinter.CTkEntry(self.configuracion_frame)
        self.configuracion_frame_entry_contrasena_correo = customtkinter.CTkEntry(self.configuracion_frame, show="*")

        self.configuracion_frame_label_usuario.grid(row=1, column=0, pady=10, padx=(50,0))
        self.configuracion_frame_label_contrasena.grid(row=2, column=0, pady=10, padx=(50,0))
        self.configuracion_frame_label_correo.grid(row=3, column=0, pady=10, padx=(50,0))
        self.configuracion_frame_label_contrasena_correo.grid(row=4, column=0, pady=10, padx=(50,0))

        self.configuracion_frame_entry_usuario.grid(row=1, column=1, pady=10, padx=(0,50))
        self.configuracion_frame_entry_contrasena.grid(row=2, column=1, pady=10, padx=(0,50))
        self.configuracion_frame_entry_correo.grid(row=3, column=1, pady=10, padx=(0,50))
        self.configuracion_frame_entry_contrasena_correo.grid(row=4, column=1, pady=10, padx=(0,50))

        self.cargar_informacion()

        self.configuracion_frame_boton_guardar = customtkinter.CTkButton(self.configuracion_frame, text="Guardar", image=self.imagen_guardar, compound="right", command=self.guardar_informacion)
        self.configuracion_frame_boton_guardar.grid(row=5, column=0, columnspan=2, pady=20)        

        self.configuracion_frame.columnconfigure(0, weight=1)
        self.configuracion_frame.columnconfigure(1, weight=1)

        self.seleccionar_frame("home")

    def seleccionar_frame(self, nombre):
        """
        Selecciona y muestra el frame correspondiente según el nombre proporcionado.

        Parámetros:
        - nombre (str): El nombre del frame a seleccionar.

        Retorna:
        - None
        """
        # set button color for selected button
        self.frame_navegacion_boton_home.configure(fg_color=("gray75", "gray25") if nombre == "home" else "transparent")
        self.frame_navegacion_boton_estado_juicios.configure(fg_color=("gray75", "gray25") if nombre == "estado_juicios" else "transparent")
        self.frame_navegacion_boton_configuracion.configure(fg_color=("gray75", "gray25") if nombre == "configuracion" else "transparent")

        # show selected frame
        if nombre == "home":
            self.home_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.home_frame.grid_forget()
        if nombre == "estado_juicios":
            self.estado_juicios_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.estado_juicios_frame.grid_forget()
        if nombre == "configuracion":
            self.configuracion_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.configuracion_frame.grid_forget()

    def evento_boton_home(self):
        """
        Evento asociado al botón 'Home' que selecciona y muestra el frame 'Home'.

        Retorna:
        - None
        """
        self.seleccionar_frame("home")

    def evento_boton_estado_cuotas(self):
        """
        Evento asociado al botón 'Estado Cuotas' que selecciona y muestra el frame 'Estado Cuotas'.

        Retorna:
        - None
        """
        self.seleccionar_frame("estado_juicios")

    def evento_boton_configuracion(self):
        """
        Evento asociado al botón 'Configuracion' que selecciona y muestra el frame 'Configuración'.

        Retorna:
        - None
        """
        self.seleccionar_frame("configuracion")

    def evento_cambio_apariencia(self, nueva_apariencia):
        """
        Cambia la apariencia visual de la interfaz gráfica.

        Esta función toma un parámetro que representa la nueva apariencia deseada y utiliza la función
        'set_appearance_mode' del módulo customtkinter para cambiar la apariencia visual de la interfaz gráfica.

        Args:
            nueva_apariencia (str): La nueva apariencia deseada para la interfaz gráfica.

        Returns:
            None
        """
        customtkinter.set_appearance_mode(nueva_apariencia)

    def cargar_archivo(self):
        """
        Abre un cuadro de diálogo para seleccionar un archivo y guarda la ruta del archivo seleccionado.

        Retorna:
        - None
        """
        self.ruta_archivo = filedialog.askopenfilename(title="Seleccionar archivo", filetypes=[("Todos los archivos", "*.*")])
        if self.ruta_archivo:
            self.home_frame_label_archivo.configure(text=f"Archivo seleccionado: {self.ruta_archivo}")

    def cargar_resultado(self):
        """
        Carga el contenido del archivo 'data/estadoCuotas.txt' en el widget Text de la interfaz gráfica.

        Retorna:
        - None
        """
        directorio_actual = Path(__file__).resolve().parent.parent
        ruta_datos = directorio_actual / 'data'
        archivo = os.path.join(ruta_datos, "estadoCuotas.txt")

        if os.path.exists(archivo):
            # Limpiar contenido actual del widget Text
            self.estado_juicios_text_widget.delete(1.0, "end")

            # Leer el contenido del archivo y cargarlo en el widget Text
            with open(archivo, "r", encoding="utf-8") as file:
                contenido = file.read()
                self.estado_juicios_text_widget.insert(1.0, contenido)
        
    def iniciar_aplicacion(self):
        """
        Inicia el script, realiza la carga de datos desde un archivo Excel, procesa la información y actualiza
        la interfaz gráfica con el resultado.

        Retorna:
        - None
        """
        try:
            if es_archivo_excel(self.ruta_archivo):
                self.home_frame_label_archivo.configure(text=f"Script en ejecución!")
                procesar_juicios(self)
                self.home_frame_label_archivo.configure(text=f"Finalizo la ejecución del Script!")
                self.cargar_resultado()
            else:
                self.abrir_errorExcel()   
        except AttributeError as e:
            self.abrir_errorArchivo()
    
    def guardar_informacion(self):
        """
        Guarda la información de usuario, contraseña, mail y contraseña del correo
        en un archivo JSON. Además, deshabilita el botón de guardar después de la operación.

        Obtiene los datos de los campos Entry de la interfaz gráfica y los almacena
        en un archivo 'config.json'. Luego, deshabilita el botón de guardar para evitar
        múltiples guardados consecutivos.

        Returns:
        - None
        """
        # Obtener los datos de los Entry
        usuario = self.configuracion_frame_entry_usuario.get()
        contrasena = self.configuracion_frame_entry_contrasena.get()
        mail = self.configuracion_frame_entry_correo.get()
        contrasena_mail = self.configuracion_frame_entry_contrasena_correo.get()

        # Guardar la información en un archivo JSON
        datos = {"usuario": usuario, "contrasena": contrasena, "mail": mail, "contrasena_mail": contrasena_mail}
        with open("config.json", "w") as archivo:
            json.dump(datos, archivo)

    def cargar_informacion(self):
        """
        Carga la información de usuario, contraseña, mail y contraseña del correo
        desde un archivo JSON y la asigna a los campos Entry correspondientes.

        Intenta cargar la información desde el archivo 'config.json' y asigna los
        valores a los campos Entry de la interfaz gráfica. Si el archivo no existe,
        maneja la excepción FileNotFoundError sin generar un error.

        Returns:
        - None
        """
        try:
            # Intentar cargar la información desde el archivo JSON
            with open("config.json", "r") as archivo:
                datos = json.load(archivo)

            # Asignar la información a las variables de los Entry
            self.configuracion_frame_entry_usuario.insert("end",datos.get("usuario", ""))
            self.configuracion_frame_entry_contrasena.insert("end",datos.get("contrasena", ""))
            self.configuracion_frame_entry_correo.insert("end",datos.get("mail", ""))
            self.configuracion_frame_entry_contrasena_correo.insert("end",datos.get("contrasena_mail", ""))
        except FileNotFoundError:
            # Manejar la excepción si el archivo no existe
            pass

    def abrir_errorArchivo(self):
        """
        Abre una ventana de error en caso de que se intente ejecutar sin cargar un archivo.

        Retorna:
        - None
        """
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = VentanaErrorArchivo(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it

    def abrir_errorExcel(self):
        """
        Abre una ventana de error en caso de que el archivo seleccionado no sea un archivo de Excel válido.

        Retorna:
        - None
        """
        if self.toplevel_window is None or not self.toplevel_window.winfo_exists():
            self.toplevel_window = VentanaErrorExcel(self)  # create window if its None or destroyed
        else:
            self.toplevel_window.focus()  # if window exists focus it

def crear_interfaz():
    """
    Crea y lanza la interfaz gráfica de la aplicación.

    Crea una instancia de la clase App, que representa la aplicación con la interfaz gráfica, y lanza el bucle principal
    de la aplicación.

    Retorna:
    - None
    """
    app = App()
    app.mainloop() 

class VentanaErrorArchivo(customtkinter.CTkToplevel):
    """
    VentanaErrorArchivo es una clase que representa una ventana de error específica para la selección de archivos.

    Esta ventana se utiliza para informar al usuario sobre la falta de selección de un archivo. Contiene una
    imagen de error, un mensaje indicando el error y un botón para cerrar la ventana.

    Args:
        *args: Argumentos posicionales pasados a la clase base.
        **kwargs: Argumentos de palabras clave pasados a la clase base.

    Attributes:
        imagen_error (customtkinter.CTkImage): Imagen de error para mostrar en la ventana.
        label_imagen_error (customtkinter.CTkLabel): Etiqueta para la imagen de error.
        label_error (customtkinter.CTkLabel): Etiqueta que muestra el mensaje de error.
        self_boton_aceptar (customtkinter.CTkButton): Botón "Aceptar" para cerrar la ventana.

    Methods:
        __init__: Inicializa la ventana de error y configura sus componentes.
    """
    def __init__(self, *args, **kwargs):
        """
        Inicializa una nueva instancia de la clase VentanaErrorArchivo.

        Args:
            *args: Argumentos posicionales pasados a la clase base.
            **kwargs: Argumentos de palabras clave pasados a la clase base.
        """
        super().__init__(*args, **kwargs)

        self.title("ERROR")

        self.update_idletasks()
        ancho = 300
        alto = 110
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry('{}x{}+{}+{}'.format(ancho, alto, x, y))

        self.attributes("-topmost", True)  # Asegurar que la nueva ventana esté en la parte superior

        directorio_actual = Path(__file__).resolve().parent.parent
        ruta_imagenes = directorio_actual / 'images'

        self.imagen_error = customtkinter.CTkImage(light_image=Image.open(os.path.join(ruta_imagenes, "errorLight.png")),
                                                 dark_image=Image.open(os.path.join(ruta_imagenes, "errorDark.png")), size=(30, 30))

        # Etiqueta para la imagen
        self.label_imagen_error = customtkinter.CTkLabel(self, text="", image=self.imagen_error)
        self.label_imagen_error.grid(row="0", column="0", pady=15, padx=(40, 0))

        self.label_error = customtkinter.CTkLabel(self, text="ERROR: Seleccione un archivo", padx=30, pady=10)
        self.label_error.grid(row="0", column="1", padx=(0, 0))

        # Botón Aceptar para cerrar la ventana
        self_boton_aceptar = customtkinter.CTkButton(self, text="Aceptar", command=self.destroy)
        self_boton_aceptar.grid(row="1", column="0", columnspan="2")

        # Configurar la propagación de la fila 1 para que el botón ocupe todo el espacio disponible
        self.grid_rowconfigure(1, weight=1)

        # Configurar la columna 0 para que se expanda horizontalmente
        self.grid_columnconfigure(0, weight=1)
        
        self.focus_force()

class VentanaErrorExcel(customtkinter.CTkToplevel):
    """
    VentanaErrorExcel es una clase que representa una ventana de error específica para archivos Excel.

    Esta ventana proporciona información sobre un error relacionado con archivos Excel, como un archivo
    inválido. Contiene una imagen de error, un mensaje de error y un botón para cerrar la ventana.

    Args:
        *args: Argumentos posicionales pasados a la clase base.
        **kwargs: Argumentos de palabras clave pasados a la clase base.

    Attributes:
        imagen_error (customtkinter.CTkImage): Imagen de error para mostrar en la ventana.
        label_imagen_error (customtkinter.CTkLabel): Etiqueta para la imagen de error.
        label_error (customtkinter.CTkLabel): Etiqueta para mostrar el mensaje de error.
        self_boton_aceptar (customtkinter.CTkButton): Botón "Aceptar" para cerrar la ventana.

    Methods:
        __init__: Inicializa la ventana de error y configura sus componentes.
    """
    def __init__(self, *args, **kwargs):
        """
        Inicializa una nueva instancia de la clase VentanaErrorExcel.

        Args:
            *args: Argumentos posicionales pasados a la clase base.
            **kwargs: Argumentos de palabras clave pasados a la clase base.
        """
        super().__init__(*args, **kwargs)

        self.title("ERROR")

        self.update_idletasks()
        ancho = 300
        alto = 110
        x = (self.winfo_screenwidth() // 2) - (ancho // 2)
        y = (self.winfo_screenheight() // 2) - (alto // 2)
        self.geometry('{}x{}+{}+{}'.format(ancho, alto, x, y))

        self.attributes("-topmost", True)  # Asegurar que la nueva ventana esté en la parte superior

        directorio_actual = Path(__file__).resolve().parent.parent
        ruta_imagenes = directorio_actual / 'images'

        self.imagen_error = customtkinter.CTkImage(light_image=Image.open(os.path.join(ruta_imagenes, "errorLight.png")),
                                                 dark_image=Image.open(os.path.join(ruta_imagenes, "errorDark.png")), size=(30, 30))

        # Etiqueta para la imagen
        self.label_imagen_error = customtkinter.CTkLabel(self, text="", image=self.imagen_error)
        self.label_imagen_error.grid(row="0", column="0", pady=15, padx=(40, 0))

        self.label_error = customtkinter.CTkLabel(self, text="ERROR: Archivo invalido")
        self.label_error.grid(row="0", column="1", padx=(0, 60))

        # Botón Aceptar para cerrar la ventana
        self_boton_aceptar = customtkinter.CTkButton(self, text="Aceptar", command=self.destroy)
        self_boton_aceptar.grid(row="1", column="0", columnspan="2")

        # Configurar la propagación de la fila 1 para que el botón ocupe todo el espacio disponible
        self.grid_rowconfigure(1, weight=1)

        # Configurar la columna 0 para que se expanda horizontalmente
        self.grid_columnconfigure(0, weight=1)
