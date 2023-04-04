import io
import boto3
import numpy as np
import pandas as pd
import configparser
from .conexiones import get_db_connection, get_s3_client
from querys import crear_db

class FuentesOrigen():
    
    def __init__(self, config: configparser.ConfigParser) -> None:
        self.config = config
        
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
        self.engine = get_db_connection(host, self.config)
        result = self.engine.execute(crear_db.DLL_QUERY)
        print('result ', result)
        
    def cargar_dataset(self, path: str):
        self.dataset = pd.read_csv(path)
        
    def cargar_datos_fuentes(self):
        # Cargamos Regiones a la BD
        regiones_df = self.dataset[['Region']]
        regiones_df.columns = ['region']
        regiones_df.drop_duplicates(inplace=True)
        regiones_df.reset_index(drop=True, inplace=True)
        regiones_df['idRegion'] = regiones_df.index + 1
        self.insertar_datos_db(regiones_df, 'Region')
        
        # Cargamos Ciudades a la BD
        ciudades_df = self.dataset[['City', 'State', 'Region']]
        ciudades_df.columns = ['city', 'state', 'region']
        ciudades_df.drop_duplicates(inplace=True)
        ciudades_df.reset_index(drop=True, inplace=True)
        ciudades_df['idCity'] = ciudades_df.index + 1
        ciudades_df = ciudades_df.merge(regiones_df, how='left', left_on='region', right_on='region')
        self.insertar_datos_db(ciudades_df.drop(['region'], axis=1), 'City')
        
        # Cargamos Clientes a la BD
        clientes_df = self.dataset[['Customer Name', 'City', 'Region']]
        clientes_df.columns = ['name', 'city', 'region']
        clientes_df.drop_duplicates(inplace=True)
        clientes_df.reset_index(drop=True, inplace=True)
        clientes_df['idCustomer'] = clientes_df.index + 1
        clientes_df = clientes_df.merge(ciudades_df, how='left', left_on=['city', 'region'], right_on=['city', 'region'])
        self.insertar_datos_db(clientes_df.drop(['city', 'state', 'idRegion', 'region'], axis=1), 'Customer')
        # print('clientes_df\n', clientes_df)
        
        # Cargamos categorias a un S3
        categorias_df = self.dataset[['Category']]
        categorias_df.drop_duplicates(inplace=True)
        categorias_df.reset_index(drop=True, inplace=True)
        categorias_df['Category Id'] = categorias_df.index + 1
        self.guardar_s3(categorias_df, 'maestros/categorias.csv')
        
        # Cargamos subcategorias a un S3
        sub_categorias_df = self.dataset[['Category', 'Sub Category']]
        sub_categorias_df.drop_duplicates(inplace=True)
        sub_categorias_df.reset_index(drop=True, inplace=True)
        sub_categorias_df['Sub Category Id'] = sub_categorias_df.index + 1
        sub_categorias_df = sub_categorias_df.merge(categorias_df, how='left', left_on='Category', right_on='Category')
        self.guardar_s3(sub_categorias_df.drop(['Category'], axis=1), 'maestros/sub_categorias.csv')
        
        # Cargamos Ordenes a la BD
        ordenes_df = self.dataset.copy()
        ordenes_df.drop_duplicates(inplace=True)
        print('ordenes_df1\n', ordenes_df)
        ordenes_df.reset_index(drop=True, inplace=True)
        ordenes_df['idOrder'] = ordenes_df.index + 1
        ordenes_df = ordenes_df.merge(clientes_df, how='left', left_on=['Customer Name', 'City', 'Region'], right_on=['name', 'city', 'region'])
        # print('ordenes_df2\n', ordenes_df)
        ordenes_df = ordenes_df.merge(sub_categorias_df, how='left', left_on=['Sub Category', 'Category'], right_on=['Sub Category', 'Category'])
        ordenes_df = ordenes_df[['idOrder', 'Order ID', 'Sales', 'Discount', 'Profit', 'Order Date', 'idCustomer', 'Sub Category Id']]
        ordenes_df.columns = ['idOrder', 'orderNumber', 'sales', 'discount', 'profit', 'date', 'idCustomer', 'sub_category_id']
        print('ordenes_df3\n', ordenes_df)
        self.insertar_datos_db(ordenes_df, 'Order')
        
    def guardar_s3(self, df: pd.DataFrame, key: str):
        self.s3_client = get_s3_client(self.config)
        bucket = self.config.get('S3', 'BUCKET')
        
        with io.StringIO() as csv_buffer:
            df.to_csv(csv_buffer, index=False)

            response = self.s3_client.put_object(
                Bucket=bucket, Key=key, Body=csv_buffer.getvalue()
            )

            status = response.get("ResponseMetadata", {}).get("HTTPStatusCode")

            if status == 200:
                print(f"Successful S3 put_object response. Status - {status}")
            else:
                print(f"Unsuccessful S3 put_object response. Status - {status}")
                
    def insertar_datos_db(self, df: pd.DataFrame, tabla: str):
        df.to_sql(tabla, con=self.engine, if_exists='append', chunksize=500, index=False)
