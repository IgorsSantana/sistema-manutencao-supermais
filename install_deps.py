#!/usr/bin/env python3
# install_deps.py - Script para instalar dependências necessárias

import subprocess
import sys
import os

# Lista de dependências necessárias para o sistema
DEPENDENCIES = [
    "flask",
    "flask-sqlalchemy", 
    "python-dotenv",
    "werkzeug"
]

def install_package(package):
    """Instala um pacote via pip"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        return True
    except subprocess.CalledProcessError:
        return False

def main():
    """Função principal para instalação de dependências"""
    print("🔧 Sistema de Manutenção - Instalador de Dependências")
    print("=" * 60)
    
    failed_packages = []
    
    print("📦 Instalando dependências...")
    
    for package in DEPENDENCIES:
        print(f"   Instalando {package}...")
        if install_package(package):
            print(f"   ✅ {package} instalado com sucesso")
        else:
            print(f"   ❌ Falha ao instalar {package}")
            failed_packages.append(package)
    
    print("\n" + "=" * 60)
    
    if not failed_packages:
        print("🎉 Todas as dependências foram instaladas com sucesso!")
        print("▶️  Agora você pode executar:")
        print("   python setup_db.py init  # Para configurar o banco")
        print("   python app.py            # Para iniciar o sistema")
    else:
        print("⚠️  Algumas dependências falharam:")
        for package in failed_packages:
            print(f"   - {package}")
        print("🔧 Tente instalar manualmente:")
        for package in failed_packages:
            print(f"   pip install {package}")

if __name__ == "__main__":
    main()
