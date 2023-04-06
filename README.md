<h1 align="center">
<br>
  <a href="https://www.galileo.edu/"><img src="https://estudiantes.galileo.edu/img/Logos/logo-noslogan.png" alt="Universidad Galileo" width="200"></a>
  <br>
  Proyecto 02 - Pipeline Ingeniería de Datos
</h1>

<h4 align="center">Proyecto final del curso Ciencia de datos con Python de la maestría en Data Science de Universidad Galileo <a href="https://www.galileo.edu/" target="_blank">Universidad Galileo</a>.</h4>


<p align="center">
  Explicación del proyecto a traves del siguiente enlace
  <a href="https://drive.google.com/file/d/1zLBw87Sp35PA3r2tmcTOLpoxW1VvG433/view?usp=sharing">https://drive.google.com/file/d/1zLBw87Sp35PA3r2tmcTOLpoxW1VvG433/view?usp=sharing</a>
</p>

## Instalación y levantado del proyecto

Esto requiere tener instalado una versión de Python 3 o un ambiente de conda o anaconda.

Pasos para instalar python, pip, crear y activar un entorno virtual con conda.

```sh
conda update conda --all
conda update anaconda
conda create --name <env_name> python=3.9
conda activate <env_name>
conda install pip
```

Pasos para instalar dependencias del proyecto con conda y pip.

```sh
conda activate <env_name>
conda install pandas
pip install --r requirements.txt
```

> Nota: Ahora ya puede ejecutar los notebooks con el ambiente de conda

## Elementos importantes dentro del proyecto

A continuación se listan los elementos mas importantes del proyecto y el propósito que tienen.

| Elemento | Tipo | Descripción | 
| ------ | ------ | ------ |
| `diagramas` | Carpeta | Contiene los diagramas relacionales de la base de datos y del datawarehouse |
| `querys` | Carpeta | Contiene las sentencias DLL para crear tanto la base de datos relacional como el DW |
| `reporteria` | Carpeta | Contiene las imagenes y archivo de Tablau que se usaron para el análisis |
| `utils` | Carpeta | Contiene los scripts de python para la parte de las conexiones, preparacion de los datos y el proceso ETL |
| `escec.cfg` | Archivo | Contiene las variables de configuración y claves de AWS |
| `exploracion-datos.ipynb` | Archivo | Notebook con la exploración del dataset utilizado |
| `preparacion_db.ipynb` | Archivo | Notebook con la ejecución del script para preparar las fuentes de origen |
| `proceso_etl.ipynb` | Archivo | Notebook con la ejecución del proceso ETL y carga al DW |
| `reporte.ipynb` | Archivo | Notebook que contiene la explicación completa del proyecto |
| `requirements.txt` | Archivo | Archivo con las librerias utilizadas dentro del proyecto |
| `sales.csv` | Archivo | Archivo del set de datos utilizado |

## Observaciones generales

> Es posible que las dos bases de datos tengan que estar creadas (vacias)

> La base de datos relacional como el DW se crearon en la misma instancia RDS

> El bucket tiene que estar creado en S3
