# config.py

class Config:
    # Configuración de la base de datos
    DB_HOST = "localhost"  # Cambia esto si tu base de datos está en otro servidor
    DB_USER = "root"       # Usuario de tu base de datos
    DB_PASSWORD = ""       # Contraseña de tu base de datos
    DB_NAME = "tienda_db"  # Nombre de tu base de datos
    DB_PORT = 3306         # Puerto para MySQL (default: 3306)

    # Otras configuraciones globales
    SECRET_KEY = ""  # Cambia esto por una clave más segura
    DEBUG = True
