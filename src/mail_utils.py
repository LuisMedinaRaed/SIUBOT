from email.message import EmailMessage
import smtplib

def enviar_mail(receptor, asunto, cuerpo):
    """
    Envía un correo electrónico con los datos proporcionados al destinatario especificado.

    Parameters:
        receptor (str): La dirección de correo electrónico del destinatario.
        asunto (str): El asunto del correo electrónico.
        cuerpo (str): El cuerpo o contenido del correo electrónico.

    Returns:
        None

    Raises:
        Exception: Captura cualquier excepción que pueda ocurrir durante el proceso y la imprime.
    """
    from juicio_utils import cargar_configuracion
    # Crear el objeto EmailMessage
    config_data = cargar_configuracion("config.json")
    smtp_username = config_data["mail"]
    smtp_password = config_data["contrasena_mail"]
    smtp_server="smtp-mail.outlook.com"
    smtp_port=587
    email = EmailMessage()
    email["From"] = smtp_username
    email["To"] = receptor
    email["Subject"] = asunto
    email.set_content(cuerpo)       
    # Conectar al servidor SMTP y enviar el correo electrónico
    try:
        smtp = smtplib.SMTP(smtp_server, port=smtp_port)
        smtp.starttls()
        smtp.login(smtp_username, smtp_password)
        smtp.sendmail(smtp_username, receptor, email.as_string())
        smtp.quit()
    except Exception as e:
        print(f"Error al enviar el correo electrónico: {e}")