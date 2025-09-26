#!/usr/bin/env python3
# final_database_status.py - Verificação final do status do banco

import psycopg2
from datetime import datetime

DATABASE_URL = "postgresql://sistema_manutencao_db_user:w3kX5gECP59VVXpYttraO8SGPScSgC8i@dpg-d3b930buibrs73f9qbdg-a.oregon-postgres.render.com/sistema_manutencao_db"

def get_final_status():
    print("🔍 Verificação Final - Status do Banco PostgreSQL Render")
    print("=" * 65)
    print(f"🕒 Execução: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # 1. Conectividade
        cursor.execute("SELECT version()")
        version = cursor.fetchone()[0]
        print(f"✅ PostgreSQL: {version}")
        
        # 2. Listar e verificar todas as tabelas
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)
        
        tables = cursor.fetchall()
        
        print(f"\n📊 Estrutura do banco:")
        print(f"   📋 Total de tabelas: {len(tables)}")
        
        if len(tables) > 0:
            total_records = 0
            for table in tables:
                table_name = table[0]
                
                # Contar registros da tabela
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                total_records += count
                
                status_icon = "📭" if count == 0 else f"📄"
                print(f"   {status_icon} {table_name}: {count} registros")
            
            print(f"\n🎯 Total global de registros: {total_records}")
            
            if total_records == 0:
                print("🆕 STATUS: BANCO VAZIO - PRONTO PARA USO DO ZERO!")
            else:
                print(f"⚠️  STATUS: {total_records} registros ainda existem")
        else:
            print("❓ Nenhuma tabela customizada encontrada (só tables do sistema)")
        
        # 3. Informações adicionais do banco
        cursor.execute("SELECT current_database(), current_user")
        db_name, user = cursor.fetchone()
        
        print(f"\n🔧 Informações conexão:")
        print(f"   👤 User: {user}")
        print(f"   💾 Database: {db_name}")
        print(f"   🌐 Host: oregon-postgres.render.com")
        
        cursor.close()
        conn.close()
        
        return total_records == 0 if tables else True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    success = get_final_status()
    
    print("\n" + "="*65)
    
    if success:
        print("🎉 CONCLUSÃO: BANCO PERFEITO PARA COMEÇAR DO ZERO!")
        print("✅ URL da aplicação: https://sistema-manutencao-supermais.onrender.com")
        print("📱 Sistema totalmente limpo - novas lojas/veículos/manutenções pronto")
        print("⭐ Pode começar a usar sua aplicação normalmente!")
    else:
        print("⚠️  STATUS: Banco pode ter dados ou problemas de conexão")
        print("🔧 Verifique logs para mais detalhes")
    
    print("" )
