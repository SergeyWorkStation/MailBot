from cryptography.fernet import Fernet
import configparser

config = configparser.ConfigParser()
config.read('config.ini')
SECRET_KEY = config['crypt']['key']
FERNET = Fernet(SECRET_KEY)


def encrypt(password):
    return FERNET.encrypt(password.encode()).decode()


def decrypt(encrypted_password):
    return FERNET.decrypt(encrypted_password).decode()

