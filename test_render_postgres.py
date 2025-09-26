#!/usr/bin/env python3
# test_render_postgres.py - Testa específico da conexão Render criada

import psycopg2
import sys
from datetime import datetime

# DATABASE_URL do PostgreSQL Render específico criado
DATABASE_URL = "postgresql://sistema_manutencao_db_user:w3kX5gECP59VVXpYttraO8SGPScSgC8i@dpg-d3b930buibrs73f9qbdg-a.oregon-postgres.render.com/sistema_manutencao_db"

def test_render_connection():
    """Testa conexão específica com o banco PostgreSQL do Render"""
    print("🔗 Sistema de Manutenção - Teste de Conexão PostgreSQL Render")
    print("=" * 70)
    
    try:
        print(f"📡 Conectando ao PostgreSQL Render...")
        print(f"🌐 Host: dpg-d3b930buibrs73f9qbdg-a.oregon-postgres.render.com")
        print(f"👤 Database: sistema_manutencao_db")
        
        # Conectar ao banco
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Teste 1: Conexão básica
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print("✅ Conexão estabelecida com sucesso!")
        print(f"   Resultado teste: {result}")
        
        # Teste 2: Informações do servidor
        cursor.execute("SELECT version()")
        version = cursor.fetchone()[0]
        print(f"🐘 PostgreSQL Version: {version}")
        
        # Teste 3: Verificar database
        cursor.execute("SELECT current_database()")
        db_name = cursor.fetchone()[0]
        print(f"📊 Database atual: {db_name}")
        
        # Teste 4: Permissões
        cursor.execute("SELECT current_user")
        user = cursor.fetchone()[0]
        print(f"👤 Usuário conectado: {user}")
        
        print("\n🔧 Esta é a configuração ideal para usar no Web Service!")
        print("✅ Use esta DATABASE_URL no Environment Variables do Render:")
        print(f"   DATABASE_URL={DATABASE_URL}")
        
        cursor.close()
        conn.close()
        
        print("\n🎉 Conexão testada com sucesso - Banco Render está funcionando!")
        return True
        
    except psycopg2.Error as pe:
        print(f"❌ Erro no PostgreSQL: {pe}")
        return False
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        return False

def create_tables_if_needed():
    """Criar tabelas no banco Render se necessário"""
    print("\n📝 Verificando estrutura do banco...")
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Verificar se as tabelas principais existem
        tables_check = [
            "loja", "veiculo", "manutencao", "foto_manutencao"
        ]
        
        for table in tables_check:
            cursor.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' 
                    AND table_name = %s
                )
            """, (table,))
            
            exists = cursor.fetchone()[0]
            if exists:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"   ✅ {table} - {count} registros")
            else:
                print(f"   ⚠️  {table} - NÃO encontrada")
        
        print("\n💡 O app criará automaticamente essas tabelas quando executar!")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"⚠️  Erro verificando tabelas: {e}")

if __name__ == "__main__":
    print(f"🕒 Teste executado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Testar conexão
    success = test_render_connection()
    
    if success:
        # Verificar/criar tabelas
        create_tables_if_needed()
        print("\n" + "="*70)
        print("✅ BANCO POSTGRESQL RENDER FUNCIONANDO!")
        print("🚀 Agora configure no Web Service do Render:")
        print(f"   Environment Variable: DATABASE_URL={DATABASE_URL}")
        print("   Then deploy ==> Deploy successful!")
    else:
        print("\n" + "="*70)
        print("❌ PROBLEMA NA CONEXÃO!")
        print("   Verifique se o banco PostgreSQL está ativo")
        print("   no Dashboard Render → status Running")
        sys.exit(1)
