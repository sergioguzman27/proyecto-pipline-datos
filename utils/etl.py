import io
import boto3
import numpy as np
import pandas as pd
import configparser
from querys import crear_dw
from utils import fuentes_origen
from datetime import datetime, date, timedelta
from utils.conexiones import get_db_connection, get_s3_client

class ETL():
    
    def __init__(self, config: configparser.ConfigParser) -> None:
        self.config = config
        self.fuente = fuentes_origen.FuentesOrigen(config)
        
    def crear_dw(self, rdsIdentifier: str):
        self.fuente.crear_instancia_rds(rdsIdentifier)
        host = self.fuente.get_host_db(rdsIdentifier)
        
        self.engine = get_db_connection(host, 'DW', self.config)
        self.engine_db = get_db_connection(host, 'RDS', self.config)
        result = self.engine.execute(crear_dw.DLL_QUERY)
        print('result ', result)
        
    def crear_dim_categoria(self):
        bucket = self.config.get('S3', 'BUCKET')
        
        # Leemos el archivo de categorias
        s3_client = get_s3_client(self.config)
        obj = s3_client.get_object(Bucket=bucket, Key='maestros/categorias.csv')
        categoria_df = pd.read_csv(io.BytesIO(obj['Body'].read()))
        
        # Leemos el archivo de subcategorias
        s3_client = get_s3_client(self.config)
        obj = s3_client.get_object(Bucket=bucket, Key='maestros/sub_categorias.csv')
        sub_categoria_df = pd.read_csv(io.BytesIO(obj['Body'].read()))
        
        # Unimos ambos csv para obtener la dimension de categorias
        categoria_dim_df = sub_categoria_df.merge(categoria_df, how='inner', left_on='Category Id', right_on='Category Id')
        categoria_dim_df.drop(['Category Id'], axis=1, inplace=True)
        categoria_dim_df.rename(
            columns={"Sub Category Id": "idSubCategory", "Sub Category": "subCategory", "Category": "category"},
            inplace=True
        )
        print('categoria_dim_df\n', categoria_dim_df)
        self.categoria_dim_df = categoria_dim_df
        
    def crear_dim_cliente(self):
        # Leemos la tabla de regiones
        region_df = pd.read_sql_query('SELECT * FROM Region', con=self.engine_db)
        
        # Leemos la tabla de Ciudades
        ciudades_df = pd.read_sql_query('SELECT * FROM City', con=self.engine_db)
        
        # Leemos la tabla de Clientes
        clientes_df = pd.read_sql_query('SELECT * FROM Customer', con=self.engine_db)
        
        # Unimos regiones con ciudades
        ciudad_region_df = ciudades_df.merge(region_df, how='inner', left_on='idRegion', right_on='idRegion')
        ciudad_region_df.drop(['idRegion'], axis=1, inplace=True)
        
        # Unimos clientes con ciudades y regiones para formar la dimension clienets
        clientes_dim_df = clientes_df.merge(ciudad_region_df, how='inner', left_on='idCity', right_on='idCity')
        clientes_dim_df.drop(['idCity'], axis=1, inplace=True)
        print('clientes_dim_df\n', clientes_dim_df)
        self.clientes_dim_df = clientes_dim_df
        
    def crear_dim_fechas(self):
        # Leemos la tabla de ordenes y nos quedamos unicamente con el campo fecha
        ordenes_df = pd.read_sql_query('SELECT * FROM `Order`', con=self.engine_db)
        fechas_dim_df = ordenes_df[['date']].drop_duplicates()
        fechas_dim_df['fullDate'] = pd.to_datetime(fechas_dim_df['date'])
        
        def calcular_campos_fecha(row):
            year = row['fullDate'].year
            row['idDate'] = int(row['fullDate'].strftime('%Y%m%d'))
            row['dayOfWeek'] = row['fullDate'].weekday() + 1
            row['dayNumInMonth'] = int(row['fullDate'].strftime('%d'))
            row['dayNumOverall'] = row['fullDate'].timetuple().tm_yday
            row['dayName'] = row['fullDate'].strftime('%A')
            row['dayAbbrev'] = row['fullDate'].strftime('%a')
            row['weekdayFlag'] = row['dayOfWeek'] <= 5
            row['weekNumInYear'] = row['fullDate'].isocalendar()[1]
            row['weekNumOverall'] = row['fullDate'].isocalendar()[1]
            row['weekBeginDate'] = row['fullDate'] - timedelta(days=(row['dayOfWeek'] - 1))
            row['month'] = int(row['fullDate'].strftime('%m'))
            row['monthNumOverall'] = row['month']
            row['monthName'] = row['fullDate'].strftime('%B')
            row['monthAbbrev'] = row['fullDate'].strftime('%b')
            row['quarter'] = pd.Timestamp(row['fullDate']).quarter
            row['year'] = year
            
            return row
        
        # calculamos los campos de la dimension
        fechas_dim_df = fechas_dim_df.apply(lambda x: calcular_campos_fecha(x), axis=1)
        fechas_dim_df.drop(['date'], axis=1, inplace=True)
        print('fechas_dim_df\n', fechas_dim_df)
        self.fechas_dim_df = fechas_dim_df
        
        