# DESCARREGA DE LA BASE DE DADES DE LA NATURAL SCENES DATASET
import boto3 # Boto3 és l'Amazon Web Services (AWS) Software Development Kit (SDK) per a Python, que permet Python developers per a carregar programari que faci servir amb serveis com Amazon S3 i Amazon EC2. Heu carregat la resposta, mostreu la data, documentació al vostre lloc web , incloent-hi el llistat de serveis que estan suportats.
import os

# Configura el nom del bucket y el directori de descarga
BUCKET_NAME = 'natural-scenes-dataset' 
DOWNLOAD_DIR = './projecte/data' 

s3 = boto3.client('s3')

def download_s3_bucket(bucket_name, download_dir):
    """..."""
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)

    try:
        # Listar els objetes en el bucket
        response = s3.list_objects_v2(Bucket=bucket_name)
        if 'Contents' not in response:
            print(f"El bucket '{bucket_name}' NO existeix.")
            return
        
        # Iterar sobre cada arxiu en el bucket
        for obj in response['Contents']:
            key = obj['Key']
            dest_path = os.path.join(download_dir, key)

            # Crear directoris si es necesari
            os.makedirs(os.path.dirname(dest_path), exist_ok=True)

            print(f"Descargando {key} a {dest_path}")
            s3.download_file(bucket_name, key, dest_path)

        print(f"Tots els arxius s'han descarregat correctament en '{download_dir}'.")
    except Exception as e:
        print(f"ERROR: {e}")

# Executar funció
download_s3_bucket(BUCKET_NAME, DOWNLOAD_DIR)

