import os
from dotenv import load_dotenv

load_dotenv()
app_key = os.getenv('APP_SECRET_KEY')
database_password = os.getenv('DATABASE_PASSWORD')
token_key = os.getenv('TOKEN_KEY')
aws_access_key = os.getenv('IAM_ACCESS_KEY')
aws_secret_key = os.getenv('IAM-SECRET_ACCESS_KEY')
google_client_id = os.getenv('GOOGLE_CLIENT_ID')