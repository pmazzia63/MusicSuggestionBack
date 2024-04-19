import boto3

# Création d'un client S3
s3 = boto3.client('s3')

# Lister tous les buckets
response = s3.list_buckets()

# Affichage des noms des buckets
for bucket in response['Buckets']:
    print(bucket['Name'])

# Create an S3 client
s3 = boto3.client('s3')

# Specify the file to upload
filename = 'test_local2.txt'
bucket_name = 'datauser'

# Upload the file
s3.upload_file(filename, bucket_name, filename)
