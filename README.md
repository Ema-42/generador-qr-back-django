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

## 🌐 Endpoints disponibles

### Códigos QR

- `GET /qr/` - Listar todos los códigos QR
- `POST /qr/` - Crear un nuevo código QR
- `GET /qr/{id}/` - Obtener un código QR específico
- `PUT /qr/{id}/` - Actualizar un código QR
- `DELETE /qr/{id}/` - Eliminar un código QR

### Documentación

- `GET /qr/docs/` - Documentación interactiva (Swagger UI)
- `GET /qr/schema/` - Esquema OpenAPI

## 📖 Uso de la API

### Crear un código QR

```bash
curl -X POST http://127.0.0.1:8000/qr/ \
  -H "Content-Type: application/json" \
  -d '{"data": "https://ejemplo.com", "size": "medium"}'
```

### Obtener todos los códigos QR

```bash
curl -X GET http://127.0.0.1:8000/qr/
```

### Obtener un código QR específico

```bash
curl -X GET http://127.0.0.1:8000/qr/1/
```

## 📚 Documentación interactiva

Una vez que el servidor esté ejecutándose, puedes acceder a la documentación interactiva en:

```
http://127.0.0.1:8000/qr/docs/
```

Esta interfaz te permite probar todos los endpoints directamente desde el navegador.

## 🗂️ Estructura del proyecto

```
generador_qr_api/
├── qr/                     # Aplicación principal
│   ├── models.py          # Modelos de datos
│   ├── views.py           # Vistas/ViewSets
│   ├── serializers.py     # Serializadores
│   └── urls.py            # URLs de la app
├── generador_qr_api/      # Configuración del proyecto
│   ├── settings.py        # Configuración
│   └── urls.py            # URLs principales
├── manage.py              # Comando de Django
├── requirements.txt       # Dependencias
└── README.md             # Este archivo
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

Tu nombre - [tu-email@ejemplo.com](mailto:tu-email@ejemplo.com)

## 🔗 Enlaces útiles

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Rest Framework](https://www.django-rest-framework.org/)
- [drf-spectacular](https://drf-spectacular.readthedocs.io/)
