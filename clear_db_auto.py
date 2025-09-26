#!/usr/bin/env python3
# clear_db_auto.py - Script AUTOMÁTICO para limpar banco PostgreSQL

import psycopg2

DATABASE_URL = "postgresql://sistema_manutencao_db_user:w3kX5gECP59VVXpYttraO8SGPScSgC8i@dpg-d3b930buibrs73f9qbdg-a.oregon-postgres.render.com/sistema_manutencao_db"

if __name__ == "__main__":
    print("🧹 Limpando banco PostgreSQL automaticamente...")
    
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Limpeza ordenada por dependências FK
        clear_commands = [
            "DELETE FROM foto_manutencao",
            "DELETE FROM manutencao", 
            "DELETE FROM loja",
            "DELETE FROM veiculo"
        ]
        
        for cmd in clear_commands:
            cursor.execute(cmd)
            print(f"✅ Executado: {cmd}")
        
        conn.commit()
        print("\n🎉 Banco limpo com sucesso!")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Erro: {e}")
    
    print("✅ Script finalizado!")
