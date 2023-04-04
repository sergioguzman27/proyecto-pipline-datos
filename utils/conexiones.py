import boto3
import configparser
from sqlalchemy.engine import URL
from sqlalchemy.engine import create_engine

def get_db_connection(host: str, config: configparser.ConfigParser):
    
    connection_url = URL.create(
        "mysql+mysqldb",
        username=config.get('RDS', 'DB_USER'),
        password=config.get('RDS', 'DB_PASSWORD'),
        host=host,
        database=config.get('RDS', 'DB_NAME')
    )
    
    return create_engine(connection_url)

def get_s3_client(config: configparser.ConfigParser):
    
    s3_client = boto3.client(
       "s3",
       aws_access_key_id=config.get('IAM', 'ACCESS_KEY'),
       aws_secret_access_key=config.get('IAM', 'SECRET_ACCESS_KEY'),
    )

    return s3_client