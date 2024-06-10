import os

# from dotenv import load_dotenv
# load_dotenv(dotenv_path='../.env')

DB_HOST = os.environ.get('DB_HOST')
DB_PORT = os.environ.get('DB_PORT')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASS = os.environ.get('DB_PASS')

JWT_SECRET = os.environ.get('JWT_SECRET')
PWD_SECRET = os.environ.get('PWD_SECRET')
