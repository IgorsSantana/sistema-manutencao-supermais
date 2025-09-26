# init_db.py - Script de inicialização do banco de dados

import os
import sys
from datetime import datetime
from app import app, db, Loja, Veiculo, Manutencao, FotoManutencao

def init_database():
    """Inicializa o banco de dados e cria dados de exemplo"""
    
    with app.app_context():
        # Criar todas as tabelas
        print("🔧 Criando tabelas do banco de dados...")
        db.create_all()
        print("✅ Tabelas criadas com sucesso!")
        
        # Verificar se já existem dados
        if Loja.query.count() > 0:
            print("ℹ️  Banco de dados já contém dados. Pulando inserção de dados de exemplo.")
            return
        
        print("📝 Inserindo dados de exemplo...")
        
        # Criar lojas de exemplo
        loja_centro = Loja(
            nome="Loja Centro",
            endereco="Rua das Flores, 123 - Centro",
            telefone="(11) 3456-7890",
            data_cadastro=datetime.utcnow()
        )
        
        loja_bairro = Loja(
            nome="Loja Bairro Novo",
            endereco="Av. Principal, 456 - Bairro Novo",
            telefone="(11) 2345-6789",
            data_cadastro=datetime.utcnow()
        )
        
        db.session.add(loja_centro)
        db.session.add(loja_bairro)
        db.session.commit()
        print("✅ Lojas de exemplo criadas")
        
        # Criar veículos de exemplo
        veiculo_palio = Veiculo(
            placa="ABC-1234",
            modelo="Palio",
            marca="Fiat",
            ano=2020,
            cor="Branco",
            data_cadastro=datetime.utcnow()
        )
        
        veiculo_gol = Veiculo(
            placa="XYZ-9876",
            modelo="Gol",
            marca="Volkswagen",
            ano=2019,
            cor="Prata",
            data_cadastro=datetime.utcnow()
        )
        
        db.session.add(veiculo_palio)
        db.session.add(veiculo_gol)
        db.session.commit()
        print("✅ Veículos de exemplo criados")
        
        # Criar manutenções de exemplo
        manutencao_loja = Manutencao(
            tipo="loja",
            titulo="Troca de lâmpadas",
            descricao="Substituição de todas as lâmpadas fluorescentes por LED",
            preco_total=450.00,
            data_manutencao=datetime.utcnow(),
            loja_id=loja_centro.id
        )
        
        manutencao_veiculo = Manutencao(
            tipo="veiculo",
            titulo="Revisão geral",
            descricao="Revisão completa do veículo incluindo troca de óleo e filtros",
            preco_total=350.00,
            data_manutencao=datetime.utcnow(),
            veiculo_id=veiculo_palio.id
        )
        
        db.session.add(manutencao_loja)
        db.session.add(manutencao_veiculo)
        db.session.commit()
        print("✅ Manutenções de exemplo criadas")
        
        print("\n🎉 Banco de dados inicializado com sucesso!")
        print(f"📊 Resumo:")
        print(f"   - {Loja.query.count()} lojas criadas")
        print(f"   - {Veiculo.query.count()} veículos criados")
        print(f"   - {Manutencao.query.count()} manutenções criadas")

def reset_database():
    """Remove todas as tabelas e cria novamente"""
    with app.app_context():
        print("🗑️  Removendo todas as tabelas...")
        db.drop_all()
        print("✅ Tabelas removidas")
        init_database()

def check_database():
    """Verifica o status atual do banco de dados"""
    with app.app_context():
        print("🔍 Verificando status do banco de dados...")
        print(f"   - Lojas: {Loja.query.count()}")
        print(f"   - Veículos: {Veiculo.query.count()}")
        print(f"   - Manutenções: {Manutencao.query.count()}")
        print(f"   - Fotos: {FotoManutencao.query.count()}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Gerenciador do banco de dados')
    parser.add_argument('action', choices=['init', 'reset', 'check'], 
                       help='Ação a executar')
    
    args = parser.parse_args()
    
    if args.action == 'init':
        init_database()
    elif args.action == 'reset':
        reset_database()
    elif args.action == 'check':
        check_database()
