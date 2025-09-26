#!/usr/bin/env python3
# inspect_and_clear.py - Inspeciona e limpa banco PostgreSQL corretamente

import psycopg2

DATABASE_URL = "postgresql://sistema_manutencao_db_user:w3kX5gECP59VVXpYttraO8SGPScSgC8i@dpg-d3b930buibrs73f9qbdg-a.oregon-postgres.render.com/sistema_manutencao_db"

def inspect_and_clear():
    print("🔍 Inspecionando banco PostgreSQL...")
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # 1. Listar todas as tabelas existentes
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cursor.fetchall()
        
        print("📋 Tabelas encontradas:")
        for table in tables:
            table_name = table[0]
            print(f"   - {table_name}")
            
            # Contar registros em cada tabela
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            print(f"     🔢 {count} registros")
        
        print("\n🧹 Iniciando limpeza...")
        
        # Limpar sequencialmente
        clear_order = ['foto_manutencao', 'manutencao', 'loja', 'veiculo']
        
        for table_name in clear_order:
            try:
                # Check if table exists
                cursor.execute(f"""
                    SELECT EXISTS (
                        SELECT FROM information_schema.tables 
                        WHERE table_schema = 'public' 
                        AND table_name = '{table_name}'
                    )
                """)
                
                exists = cursor.fetchone()[0]
                
                if exists:
                    cursor.execute(f"DELETE FROM {table_name}")
                    conn.commit()
                    print(f"✅ Limpeza de {table_name} - OK")
                else:
                    print(f"⚠️  Tabela {table_name} não existe - pulando")
                    
            except Exception as e:
                print(f"❌ Erro limpeza {table_name}: {e}")
                continue
        
        # Verificar resultado final
        print("\n📊 Status final após limpeza:")
        cursor.execute("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
        """)
        tables = cursor.fetchall()
        
        total_records = 0
        for table in tables:
            table_name = table[0]
            cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = cursor.fetchone()[0]
            total_records += count
            print(f"   {table_name}: {count} registros")
        
        print(f"\n🎯 Total de registros no banco: {total_records}")
        
        if total_records == 0:
            print("🎉 BANCO TOTALMENTE LIMPO!")
        else:
            print("📝 Ítem restante no banco (tabela pode conter dados)")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro conexão: {e}")

if __name__ == "__main__":
    print("🔄 Sistema de Inspecionar e Limpar PostgreSQL Render")
    print("="*50)
    inspect_and_clear() 
    print("\n✅ Operação concluída!")
