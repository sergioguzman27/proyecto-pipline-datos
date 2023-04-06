<h1 align="center">
<br>
  <a href="https://www.galileo.edu/"><img src="https://estudiantes.galileo.edu/img/Logos/logo-noslogan.png" alt="Universidad Galileo" width="200"></a>
  <br>
  Proyecto 02 - Pipeline Ingeniería de Datos
</h1>

<h4 align="center">Proyecto final del curso Ciencia de datos con Python de la maestría en Data Science de Universidad Galileo <a href="https://www.galileo.edu/" target="_blank">Universidad Galileo</a>.</h4>


<p align="center">
  Explicación del proyecto a traves del siguiente enlace
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