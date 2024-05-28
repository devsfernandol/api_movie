import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Nombre del archivo SQLite que se utilizará como base de datos.
sqlite_file_name = "../database.sqlite"

# Obtiene el directorio base del archivo actual.
base_dir = os.path.dirname(os.path.realpath(__file__))

# Construye la URL de la base de datos SQLite.
# Esto utiliza el directorio base y el nombre del archivo SQLite.
database_url = f"sqlite:///{os.path.join(base_dir, sqlite_file_name)}"

# Crea una instancia del motor de base de datos usando la URL construida.
# El parámetro echo=True habilita el registro de todas las consultas SQL ejecutadas.
engine = create_engine(database_url, echo=True)

# Crea una fábrica de sesiones configurada para utilizar el motor de base de datos creado.
# Una sesión sirve como una conexión temporal a la base de datos.
Session = sessionmaker(bind=engine)

# Crea una clase base para los modelos de SQLAlchemy.
# Esta clase se utilizará para definir las tablas de la base de datos.
Base = declarative_base()
