import boto3
from module_program.env_key import *

s3 = boto3.client(
    's3',
    aws_access_key_id='AKIAWSBWBJWOBGMXF4K2',
    aws_secret_access_key='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',
    region_name='ap-northeast-1')

def getBucketName():
    response = s3.list_buckets()
    for bucket in response['Buckets']:
        return bucket["Name"]

# def uploadToS3(local_file_path, bucket_name, object_name):
#     with open(local_file_path, 'rb') as file:
#         s3.upload_file(file, bucket_name, object_name)

def uploadToS3(file, bucket_name, object_name):
    s3.upload_fileobj(file, bucket_name, object_name)