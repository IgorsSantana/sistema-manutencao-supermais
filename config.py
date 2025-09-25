# config.py
# Configurações do Sistema de Manutenção

import os

class Config:
    # Configurações do Flask
    SECRET_KEY = 'santo_antonio_super_mais_2024'
    
    # Configurações do Banco de Dados
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações de Upload
    UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # Configurações da Aplicação
    DEBUG = True
    HOST = '0.0.0.0'
    PORT = 5000
