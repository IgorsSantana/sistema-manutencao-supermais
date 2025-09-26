#!/usr/bin/env python3
# clear_database.py - Script para limpar completamente o banco PostgreSQL Render

import psycopg2
from datetime import datetime

# DATABASE_URL do PostgreSQL Render que já testamos anteriormente
DATABASE_URL = "postgresql://sistema_manutencao_db_user:w3kX5gECP59VVXpYttraO8SGPScSgC8i@dpg-d3b930buibrs73f9qbdg-a.oregon-postgres.render.com/sistema_manutencao_db"

def clear_database():
    """Limpa completamente o banco PostgreSQL"""
    print("🗑️ Sistema de Manutenção - Limpeza Total do Banco")
    print("=" * 60)
    print(f"🕒 Início: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        print("🔗 Conectando ao PostgreSQL Render...")
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        print("✅ Conectado ao banco PostgreSQL!")
        
        # Verificar dados existentes antes da limpeza
        print("\n📊 Dados existentes antes da limpeza:")
        check_existing_data(cursor)
        
        print("\n🚮 Iniciando limpeza completa...")
        
        # Sequência de limpeza respeitando relacionamentos FK
        clear_sequence = [
            # Fotos de manutenção (FK dependency)
            {
                'table': 'foto_manutencao',
                'description': 'Fotos de manutenção',
                'sql': 'DELETE FROM foto_manutencao'
            },
            
            # Manutenções (FK dependency)  
            {
                'table': 'manutencao',
                'description': 'Tradenças de manutenção',
                'sql': 'DELETE FROM manutencao'
            },
            
            # Lojas (independente)
            {
                'table': 'loja', 
                'description': 'Lojas cadastradas',
                'sql': 'DELETE FROM loja'
            },
            
            # Veículos (independente)
            {
                'table': 'veiculo',
                'description': 'Veículos cadastrados', 
                'sql': 'DELETE FROM veiculo'
            }
        ]
        
        # Executar limpeza sequencial
        total_deleted = 0
        for item in clear_sequence:
            try:
                print(f"🧹 Apagando {item['description']}...")
                cursor.execute(item['sql'])
                count = cursor.rowcount
                print(f"   ✅ {count} registros removidos de {item['table']}")
                total_deleted += count
                
            except Exception as e:
                print(f"   ⚠️ Warning {item['table']}: {e}")
                # Continuar mesmo com erro (tabela pode não existir)
        
        # Commit das mudanças
        conn.commit()
        print(f"\n🎉 Limpeza concluída! {total_deleted} registros removidos")
        
        # Verificar banco após limpeza
        print("\n📊 Status final:")
        check_existing_data(cursor)
        
        # Resetar contadores de sequência (opcional)
        print("\n🔄 Resetando contadores de ID:")
        sequence_reset = [
            "ALTER SEQUENCE loja_id_seq RESTART WITH 1",
            "ALTER SEQUENCE veiculo_id_seq RESTART WITH 1", 
            "ALTER SEQUENCE manutencao_id_seq RESTART WITH 1",
            "ALTER SEQUENCE foto_manutencao_id_seq RESTART WITH 1"
        ]
        
        for sql in sequence_reset:
            try:
                cursor.execute(sql)
                print(f"   ✅ Sequence reset executado")
            except Exception as e:
                # Sequence pode não existir ainda
                print(f"   ⚠️ Sequence reset skipped: {e}")
        
        conn.commit()
        
        cursor.close()
        conn.close()
        
        print("\n" + "="*60)
        print("✅ BANCO POSTGRESQL TOTALLY CLEARED - READY TO START FRESH!")
        print("🆕 Sua aplicação agora terá banco de dados vazio")
        print("💡 Acesse https://sistema-manutencao-supermais.onrender.com para usar")
        
        return True
        
    except psycopg2.Error as pe:
        print(f"❌ Erro PostgreSQL: {pe}")
        return False
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        return False

def check_existing_data(cursor):
    """Verifica dados existentes nas tabelas"""
    tables = ['loja', 'veiculo', 'manutencao', 'foto_manutencao']
    
    for table in tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"   📋 {table}: {count} registros")
        except Exception as e:
            print(f"   ⚠️ {table}: tabela não existe ou erro - {e}")

def confirm_action():
    """Confirma se o usuário quer realmente limpar tudo"""
    print("⚠️  ATENÇÃO: Esta ação apagará TODOS os dados do banco PostgreSQL!")
    print("📋 Será removido:")
    print("   🏪 Todas as lojas cadastradas")
    print("   🚗 Todos os veículos")
    print("   🔧 Todas as manutenções") 
    print("   📷 Todas as fotos anexas")
    print("\n❓ Esta ação é IRREVERSÍVEL!")
    
    confirmation = input("\nDigite 'LIMPAR' para confirmar: ")
    return confirmation == "LIMPAR"

if __name__ == "__main__":
    print("🗑️ Sistema de Manutenção - Database Clear Operation")
    print("↳ Limpeza completa PostgreSQL Render")
    print()
    
    if confirm_action():
        success = clear_database()
        
        if success:
            print("\n🎉 BANCO LIMPO COM SUCESSO!")
            print("🌐 Agora pode usar sua aplicação com banco vazio:")
            print("   URL: https://sistema-manutencao-supermais.onrender.com")
            print("   🆕 Nova cadastro de lojas funcionará do zero")
        else:
            print("\n❌ FALHA na limpeza! Verifique logs acima.")
    else:
        print("\n❌ Operação cancelada pelo usuário")
    
    print("\n👋 Finalizando script...")
