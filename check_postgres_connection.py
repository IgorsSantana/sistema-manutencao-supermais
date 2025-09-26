#!/usr/bin/env python3
# check_postgres_connection.py - Verificar conexão PostgreSQL

import os
import sys
import psycopg2
from urllib.parse import urlparse

def test_postgres_connection():
    """Testa a conexão com PostgreSQL"""
    print("🔍 Sistema de Teste - PostgreSQL Connection")
    print("=" * 60)
    
    # Obter DATABASE_URL
    database_url = os.environ.get('DATABASE_URL')
    
    if not database_url:
        print("❌ DATABASE_URL não configurada!")
        print("💡 Configure a variável de ambiente:")
        print("   export DATABASE_URL='sua_url_postgresql'")
        return False
    
    try:
        print(f"🔗 Testando conexão...")
        print(f"📡 URL: {database_url[:50]}...")
        
        # Conectar ao banco
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Teste básico
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        
        print("✅ Conectou ao PostgreSQL com sucesso!")
        print(f"📊 Test result: {result}")
        
        # Descobrir detalhes do banco
        cursor.execute("SELECT version()")
        version = cursor.fetchone()[0]
        print(f"🐘 PostgreSQL version: {version}")
        
        # Verificar se as tabelas existem
        test_tables()
        
        cursor.close()
        conn.close()
        
        print("\n🎉 Teste concluído - PostgreSQL funcionando!")
        return True
        
    except psycopg2.Error as e:
        print(f"❌ Erro PostgreSQL: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        return False

def test_tables():
    """Verifica se as tabelas existem"""
    try:
        database_url = os.environ.get('DATABASE_URL')
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()
        
        # Lista de tabelas esperadas
        expected_tables = ['loja', 'veiculo', 'manutencao', 'foto_manutencao']
        
        print("\n📋 Verificando tabelas...")
        
        for table in expected_tables:
            cursor.execute(f"""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_name = '{table}'
                AND table_schema = 'public'
            """)
            exists = cursor.fetchone()
            
            if exists:
                # Consultar número de registros
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"   ✅ {table} - {count} registros")
            else:
                print(f"   ❌ {table} - NÃO existe")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"⚠️ Erro ao verificar tabelas: {e}")

def show_postgres_info():
    """Mostra informações detalhadas"""
    try:
        database_url = os.environ.get('DATABASE_URL')
        parsed = urlparse(database_url)
        
        print("🔧 Informações da conexão:")
        print(f"   Host: {parsed.hostname}")
        print(f"   Port: {parsed.port}")
        print(f"   DB User: {parsed.username}")
        print(f"   Database: {parsed.path[1:]}")
        
    except Exception as e:
        print(f"⚠️ Erro ao analisar URL: {e}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Teste PostgreSQL Render')
    parser.add_argument('--info', action='store_true', 
                       help='Mostrar informações da conexão')
    
    args = parser.parse_args()
    
    if args.info:
        show_postgres_info()
    
    success = test_postgres_connection()
    
    if success:
        print("\n✅ PostgreSQL está pronto para usar!")
        print("🎯 Execute: python app.py para iniciar o sistema")
    else:
        print("\n❌ Problema na configuração")
        print("📖 Consulte: RENDER_SETUP_GUIDE.md")
        sys.exit(1)
    print("=" * 60)
