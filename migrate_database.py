#!/usr/bin/env python3
"""
Script de migração para adicionar colunas do Cloudinary ao banco de dados
"""
import os
import sys
from sqlalchemy import text

# Adicionar o diretório atual ao path para importar o app
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db

def migrate_database():
    """
    Adiciona as colunas do Cloudinary à tabela foto_manutencao
    """
    print("🔄 Iniciando migração do banco de dados...")
    
    with app.app_context():
        try:
            # Verificar se as colunas já existem
            result = db.session.execute(text("""
                SELECT column_name 
                FROM information_schema.columns 
                WHERE table_name = 'foto_manutencao' 
                AND column_name = 'cloudinary_public_id'
            """))
            
            if result.fetchone():
                print("✅ Colunas do Cloudinary já existem. Migração desnecessária.")
                return True
            
            print("📝 Adicionando colunas do Cloudinary...")
            
            # Adicionar as colunas do Cloudinary
            db.session.execute(text("""
                ALTER TABLE foto_manutencao 
                ADD COLUMN cloudinary_public_id VARCHAR(200),
                ADD COLUMN cloudinary_url VARCHAR(500),
                ADD COLUMN cloudinary_secure_url VARCHAR(500)
            """))
            
            # Tornar caminho_arquivo nullable (já pode ser None se usar Cloudinary)
            db.session.execute(text("""
                ALTER TABLE foto_manutencao 
                ALTER COLUMN caminho_arquivo DROP NOT NULL
            """))
            
            db.session.commit()
            print("✅ Migração concluída com sucesso!")
            print("📊 Colunas adicionadas:")
            print("   - cloudinary_public_id")
            print("   - cloudinary_url") 
            print("   - cloudinary_secure_url")
            print("   - caminho_arquivo agora é nullable")
            
            return True
            
        except Exception as e:
            print(f"❌ Erro durante a migração: {str(e)}")
            db.session.rollback()
            return False

def verify_migration():
    """
    Verifica se a migração foi aplicada corretamente
    """
    print("🔍 Verificando migração...")
    
    with app.app_context():
        try:
            # Verificar se as colunas existem
            result = db.session.execute(text("""
                SELECT column_name, data_type, is_nullable
                FROM information_schema.columns 
                WHERE table_name = 'foto_manutencao'
                ORDER BY column_name
            """))
            
            columns = result.fetchall()
            print("📋 Colunas da tabela foto_manutencao:")
            for col in columns:
                print(f"   - {col[0]}: {col[1]} ({'NULL' if col[2] == 'YES' else 'NOT NULL'})")
            
            # Verificar se as colunas do Cloudinary existem
            cloudinary_columns = [col[0] for col in columns if 'cloudinary' in col[0]]
            if len(cloudinary_columns) == 3:
                print("✅ Todas as colunas do Cloudinary foram adicionadas!")
                return True
            else:
                print(f"⚠️ Apenas {len(cloudinary_columns)} colunas do Cloudinary encontradas")
                return False
                
        except Exception as e:
            print(f"❌ Erro ao verificar migração: {str(e)}")
            return False

if __name__ == "__main__":
    print("🚀 Script de Migração do Banco de Dados")
    print("=" * 50)
    
    # Executar migração
    if migrate_database():
        # Verificar se funcionou
        if verify_migration():
            print("\n🎉 Migração concluída com sucesso!")
            print("✅ O app agora pode usar Cloudinary para armazenar imagens.")
        else:
            print("\n⚠️ Migração aplicada, mas verificação falhou.")
            sys.exit(1)
    else:
        print("\n❌ Falha na migração.")
        sys.exit(1)
