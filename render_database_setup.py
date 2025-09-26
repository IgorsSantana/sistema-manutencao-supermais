#!/usr/bin/env python3
# render_database_setup.py - Script específico para configuração no Render

import os
import sys
import psycopg2
import psycopg2.extras
from urllib.parse import urlparse

def setup_render_database():
    """Configura o banco PostgreSQL no Render"""
    
    # Obter URL do banco do Render
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL não encontrada!")
        print("💡 Configure a variável DATABASE_URL no Render:")
        print("   1. Acesse seu app no Render")
        print("   2. Vá em Environment")
        print("   3. Adicione DATABASE_URL: <sua_url_postgresql>")
        return False
    
    try:
        print("🔧 Configurando banco PostgreSQL no Render...")
        
        # Parse da URL do banco
        parsed = urlparse(database_url)
        
        # Conectar ao banco
        conn = psycopg2.connect(database_url)
        conn.autocommit = True
        cursor = conn.cursor()
        
        print("✅ Conectado ao PostgreSQL com sucesso!")
        
        # Criar tabelas necessárias
        create_tables(cursor)
        
        # Fechar conexão
        cursor.close()
        conn.close()
        
        print("🎉 Banco PostgreSQL configurado com sucesso!")
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Erro ao conectar ao banco: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
        return False

def create_tables(cursor):
    """Cria as tabelas necessárias no PostgreSQL"""
    print("📝 Criando tabelas no PostgreSQL...")
    
    # SQL para criar tabelas
    tables_sql = [
        # Tabela Loja
        """
        CREATE TABLE IF NOT EXISTS loja (
            id SERIAL PRIMARY KEY,
            nome VARCHAR(100) NOT NULL UNIQUE,
            endereco VARCHAR(200),
            telefone VARCHAR(20),
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        
        # Tabela Veiculo
        """
        CREATE TABLE IF NOT EXISTS veiculo (
            id SERIAL PRIMARY KEY,
            placa VARCHAR(10) NOT NULL UNIQUE,
            modelo VARCHAR(50) NOT NULL,
            marca VARCHAR(50),
            ano INTEGER,
            cor VARCHAR(30),
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """,
        
        # Tabela Manutencao
        """
        CREATE TABLE IF NOT EXISTS manutencao (
            id SERIAL PRIMARY KEY,
            tipo VARCHAR(20) NOT NULL,
            titulo VARCHAR(100) NOT NULL,
            descricao TEXT,
            preco_total DECIMAL(10,2) DEFAULT 0.0,
            data_manutencao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            loja_id INTEGER REFERENCES loja(id),
            veiculo_id INTEGER REFERENCES veiculo(id)
        );
        """,
        
        # Tabela FotoManutencao
        """
        CREATE TABLE IF NOT EXISTS foto_manutencao (
            id SERIAL PRIMARY KEY,
            nome_arquivo VARCHAR(100) NOT NULL,
            caminho_arquivo VARCHAR(200) NOT NULL,
            data_upload TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            manutencao_id INTEGER NOT NULL REFERENCES manutencao(id) ON DELETE CASCADE
        );
        """
    ]
    
    # Executar cada comando SQL
    for sql in tables_sql:
        cursor.execute(sql)
        print("   ✅ Tabela criada")
    
    print("✅ Todas as tabelas foram criadas/verificadas!")

def check_connection():
    """Verifica a conexão com o banco"""
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL não configurada!")
        return False
    
    try:
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        cursor.close()
        conn.close()
        
        print("✅ Conexão com banco verificada!")
        return True
        
    except Exception as e:
        print(f"❌ Erro na verificação: {e}")
        return False

if __name__ == "__main__":
    print("🌐 Sistema de Manutenção - Configuração Render PostgreSQL")
    print("=" * 60)
    
    if len(sys.argv) > 1 and sys.argv[1] == 'check':
        check_connection()
    else:
        setup_render_database()
    print("=" * 60)
