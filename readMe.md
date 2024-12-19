# Aplicación de Gestión de Tareas

Esta es una aplicación de gestión de tareas desarrollada con Python, Streamlit y SQLAlchemy que permite administrar tareas diarias de manera eficiente.

## Características

- ✅ Agregar nuevas tareas con título y descripción
- 📋 Listar todas las tareas existentes
- ✔️ Marcar tareas como completadas 
- 🗑️ Eliminar tareas
- 💾 Exportar e importar tareas en formato JSON
- 🎯 Interfaz gráfica intuitiva
- 🗄️ Persistencia de datos con SQLite

## Requisitos


## Instalación

1. Clona este repositorio:
bash
git clone <url-del-repositorio>
cd gestion-tareas


2. Instala las dependencias:

bash
pip install -r requirements.txt


## Uso

1. Ejecuta la aplicación:

bash
streamlit run main.py


2. La aplicación se abrirá en tu navegador predeterminado

3. Funcionalidades principales:
   - **Agregar Tarea**: Ingresa título y descripción para crear nueva tarea
   - **Listar Tareas**: Visualiza todas las tareas con opciones para completar y eliminar
   - **Exportar/Importar**: Guarda o carga tareas desde archivos JSON

## Estructura del Proyecto


gestion-tareas/
│
├── main.py # Archivo principal de la aplicación
├── tareas.db # Base de datos SQLite (se crea automáticamente)
├── requirements.txt # Dependencias del proyecto
└── README.md # Documentación


## Base de Datos

La aplicación utiliza SQLite a través de SQLAlchemy con el siguiente modelo:

python
class Tarea(Base):
tablename = 'tareas'
id = Column(Integer, primary_key=True)
titulo = Column(String(100), nullable=False)
descripcion = Column(String(500))
completada = Column(Boolean, default=False)


## Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo LICENSE para más detalles.