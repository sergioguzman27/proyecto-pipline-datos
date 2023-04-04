import boto3
import random
import datetime
import numpy as np
import pandas as pd
import configparser
from faker import Faker
from .conexiones import get_db_connection
from querys import crear_db

class FuentesOrigen():
    
    def __init__(self) -> None:
        self.config = configparser.ConfigParser()
        self.config.read('../escec.cfg')
        
        self.aws_conn = boto3.client(
            'rds',
            aws_access_key_id=self.config.get('IAM', 'ACCESS_KEY'),
            aws_secret_access_key=self.config.get('IAM', 'SECRET_ACCESS_KEY'),
            region_name=self.config.get('IAM', 'REGION_NAME')
        )
        
    def get_instancias_rds(self):
        rdsInstanceIds = []

        response = self.aws_conn.describe_db_instances()
        for resp in response['DBInstances']:
            rdsInstanceIds.append(resp['DBInstanceIdentifier'])
            db_instance_status = resp['DBInstanceStatus']

        return rdsInstanceIds
    
    def crear_instancia_rds(self, rdsIdentifier: str):
        try:
            response = self.aws_conn.create_db_instance(
                AllocatedStorage=10,
                DBName=self.config.get('RDS', 'DB_NAME'),
                DBInstanceIdentifier=rdsIdentifier,
                DBInstanceClass="db.t3.micro",
                Engine="mysql",
                MasterUsername=self.config.get('RDS', 'DB_USER'),
                MasterUserPassword=self.config.get('RDS', 'DB_PASSWORD'),
                Port=int(self.config.get('RDS', 'DB_PORT')),
                VpcSecurityGroupIds=[self.config.get('VPC', 'SECURITY_GROUP')],
                PubliclyAccessible=True
            )
            print(response)
        except self.aws_conn.exceptions.DBInstanceAlreadyExistsFault as ex:
            print("La Instancia de Base de Datos ya Existe.")
            
    def get_host_db(self, rdsIdentifier: str):
        try:
            instances = self.aws_conn.describe_db_instances(DBInstanceIdentifier=rdsIdentifier)
            rds_host = instances.get('DBInstances')[0].get('Endpoint').get('Address')
            print(rds_host)
            return rds_host
        except Exception as ex:
            print("La instancia de base de datos no existe o aun no se ha terminado de crear.")
            print(ex)
            return None
        
    def crear_base_relacional(self, host: str):
        self.engine = get_db_connection(host)
        result = self.engine.execute(crear_db.DLL_QUERY)
        print('result ', result)
        
    def cargar_dataset(self, path: str):
        self.dataset = pd.read_csv(path)
        
    def cargar_datos_db_relacional(self):
        # Cargamos primero la tabla Usuarios
        usuarios_df = self.dataset[['user_id', 'user_name']]
        usuarios_df.columns = ['IdUser', 'Username']
        usuarios_df.drop_duplicates(inplace=True)
        print('usuarios_df\n', usuarios_df)
        
        # Cargamos la tabla Productos
        productos_df = self.dataset[['product_id', 'product_name', 'about_product',
                                     'actual_price', 'discounted_price', 'img_link', 'product_link', 'category']]
        productos_df.columns = ['IdProduct', 'Name', 'Description', 'Price', 'DiscountPercentage',
                               'ImageLink', 'ProductoLink', 'category']
        productos_df['Price'] = productos_df['Price'].str.replace("₹",'')
        productos_df['Price'] = productos_df['Price'].str.replace(",",'')
        productos_df['Price'] = productos_df['Price'].astype('float64')
        
        productos_df['DiscountPercentage'] = productos_df['DiscountPercentage'].str.replace('%','')
        productos_df['DiscountPercentage'] = productos_df['DiscountPercentage'].astype('float64')
        
        productos_df['category'] = productos_df.apply(lambda x: self._get_categoria(x), axis=1)
        categorias_df = self.get_categorias_df()
        productos_df = productos_df.merge(
            categorias_df, how='inner', left_on='category', right_on='Name_Cat', suffixes=('', '_Cat')
        )
        productos_df['CategoryId'] = productos_df['CategoryId_Cat']

        productos_df.drop_duplicates(inplace=True).drop(['category', 'CategoryId_Cat', 'Name_Cat'], inplace=True)
        print('productos_df\n', productos_df)
        
        # Cargamos la tabla Reseñas
        review_df = self.dataset[['review_id', 'review_title', 'review_content', 'discounted_price',
                                  'rating', 'user_id']]
        
        
        
        
    def _get_categoria(self, row):
        categorias = row['category'].split('|')
        return categorias[1] if len(categorias) > 1 else categorias[0]
    
    def get_categorias_df(self):
        categorias_df = self.dataset[['category']]
        categorias_df['category'] = categorias_df.apply(lambda x: self._get_categoria(x), axis=1)
        categorias_unicas = categorias_df['category'].unique().tolist()
        categorias_df = pd.DataFrame({'Name': categorias_unicas})
        categorias_df['CategoryId'] = categorias_df.index + 1
        
        return categorias_df
    
    def cargar_datos_maestros_s3(self):
        # Cargamos el maestro de categorias
        categorias_df = self.get_categorias_df()
        print('categorias_df\n', categorias_df)
        
        # Cargamos el maestro de Tipos de Review con datos de prueba
        tipos_review_df = pd.DataFrame({
            'Type': ['Reseña comparativa', 'Reseña de experto', 'Reseña de usuario', 'Reseña por uso']
        })
        tipos_review_df['ReviewTypeId'] = tipos_review_df.index + 1
        print('tipos_review_df\n', tipos_review_df)
        
