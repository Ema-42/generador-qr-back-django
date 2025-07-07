# Generador QR API

Una API REST desarrollada con Django Rest Framework para generar códigos QR de manera sencilla y eficiente.

## 🚀 Características

- **Generación de códigos QR**: Crear códigos QR personalizados
- **API RESTful**: Endpoints bien estructurados siguiendo estándares REST
- **Documentación interactiva**: Swagger UI integrado para pruebas
- **Base de datos**: Almacenamiento de códigos QR generados
- **Fácil de usar**: Interfaz simple y clara

## 🛠️ Tecnologías utilizadas

- **Django**: Framework web de Python
- **Django Rest Framework**: Para la creación de la API REST
- **drf-spectacular**: Generación automática de documentación OpenAPI/Swagger
- **SQLite**: Base de datos (por defecto)
- **Python**: Lenguaje de programación

## 📋 Requisitos previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)

## 🔧 Instalación

1. **Clonar el repositorio**

   ```bash
   git clone <url-del-repositorio>
   cd generador_qr_api
   ```

2. **Crear entorno virtual**

   ```bash
   python -m venv venv
   ```

3. **Activar entorno virtual**

   - En Windows:
     ```bash
     venv\Scripts\activate
     ```
   - En macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

4. **Instalar dependencias**

   ```bash
   pip install -r requirements.txt
   ```

5. **Realizar migraciones**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Ejecutar el servidor**
   ```bash
   python manage.py runserver
   ```
 

### Documentación

- `GET /qr/docs/` - Documentación interactiva (Swagger UI)
- `GET /qr/schema/` - Esquema OpenAPI

## 🐘 Configurar PostgreSQL (Neon) en un proyecto Django que usaba SQLite
### 🔧 Requisitos previos
### Proyecto Django funcionando localmente.

- **Cuenta creada en Neon** con una base de datos PostgreSQL activa.
- **Tener la cadena de conexión** (_Neon connection string_).
- **Tener un entorno virtual activo** (`venv`).

## Instalar dependencias necesarias:
```bash
pip install psycopg2-binary dj-database-url python-dotenv
```
## 📁 1. Crear archivo .env en la raíz del proyecto
Agregar esta línea con tu cadena de conexión real de Neon (puedes obtenerla desde el dashboard):
```bash
DATABASE_URL=postgresql://<usuario>:<contraseña>@<host>.neon.tech/<nombre_db>?sslmode=require
``` 
### 🔒 Reemplaza <usuario>, <contraseña>, <host>, y <nombre_db> con los valores de tu cuenta de Neon.


## ⚙️ 2. Modificar settings.py para usar .env y Neon
Agrega al inicio de settings.py:
```bash
import os
from dotenv import load_dotenv
load_dotenv()
```
```bash
import dj_database_url
```
```bash
DATABASES = {
    'default': dj_database_url.parse(
        os.environ.get("DATABASE_URL"),
        conn_max_age=600,
        ssl_require=True  # Importante para Neon
    )
}
``` 
## 4. Generar y aplicar migraciones a Neon

Detectar cambios en los modelos
```bash
python manage.py makemigrations
```
Aplicar migraciones a la base de datos Neon
```bash
python manage.py migrate
```

## 🧪 6. Verificar conexión
Puedes verificar la conexión directamente ejecutando:
 ```bash
python manage.py dbshell
``` 

## 🤝 Contribuir

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📝 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para más detalles.

## 👨‍💻 Autor

Emanuel Chusgo Santos - [emanuelchusgp@gmail.com](mailto:emanuelchusgp@gmail.com)

## 🔗 Enlaces útiles

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Rest Framework](https://www.django-rest-framework.org/)
- [drf-spectacular](https://drf-spectacular.readthedocs.io/)
