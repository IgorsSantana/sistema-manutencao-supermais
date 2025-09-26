#!/usr/bin/env python3
# setup_db.py - Script principal para configuração do banco de dados

import os
import sys
from datetime import datetime
from pathlib import Path

# Adicionar o diretório do projeto ao path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

try:
    from app import app, db, Loja, Veiculo, Manutencao, FotoManutencao
    IMPORTS_SUCCESS = True
except ImportError as e:
    print(f"❌ Erro ao importar módulos: {e}")
    print("⚠️  Certifique-se de que o arquivo app.py está funcionando corretamente")
    IMPORTS_SUCCESS = False

def init_database():
    """Inicializa o banco de dados e cria dados de exemplo"""
    if not IMPORTS_SUCCESS:
        print("❌ Não é possível continuar sem imports corretos")
        return False
        
    try:
        with app.app_context():
            print("🔧 Configurando o banco de dados do Sistema de Manutenção...")
            
            # Criar todas as tabelas
            db.create_all()
            print("✅ Tabelas criadas com sucesso!")
            
            # Verificar se já existem dados
            if Loja.query.count() > 0:
                print("ℹ️  O banco já contém dados.")
                print(f"   - Lojas: {Loja.query.count()}")
                print(f"   - Veículos: {Veiculo.query.count()}")
                print(f"   - Manutenções: {Manutencao.query.count()}")
                print(f"   - Fotos: {FotoManutencao.query.count()}")
                return True
            
            print("📝 Inserindo dados de exemplo...")
            
            # Criar lojas de exemplo
            loja_examples = [
                {
                    'nome': 'Loja Centro',
                    'endereco': 'Rua das Flores, 123 - Centro',
                    'telefone': '(11) 3456-7890'
                },
                {
                    'nome': 'Loja Bairro Novo', 
                    'endereco': 'Av. Principal, 456 - Bairro Novo',
                    'telefone': '(11) 2345-6789'
                }
            ]
            
            lojas_criadas = []
            for loja_data in loja_examples:
                loja = Loja(**loja_data, data_cadastro=datetime.utcnow())
                db.session.add(loja)
                lojas_criadas.append(loja)
            
            db.session.commit()
            print("✅ Lojas de exemplo criadas")
            
            # Criar veículos de exemplo
            veiculo_examples = [
                {
                    'placa': 'ABC-1234',
                    'modelo': 'Palio',
                    'marca': 'Fiat',
                    'ano': 2020,
                    'cor': 'Branco'
                },
                {
                    'placa': 'XYZ-9876',
                    'modelo': 'Gol',
                    'marca': 'Volkswagen',
                    'ano': 2019,
                    'cor': 'Prata'
                }
            ]
            
            veiculos_criados = []
            for veiculo_data in veiculo_examples:
                veiculo = Veiculo(**veiculo_data, data_cadastro=datetime.utcnow())
                db.session.add(veiculo)
                veiculos_criados.append(veiculo)
            
            db.session.commit()
            print("✅ Veículos de exemplo criados")
            
            # Criar manutenções de exemplo
            if lojas_criadas and veiculos_criados:
                manutencao_examples = [
                    {
                        'tipo': 'loja',
                        'titulo': 'Troca de lâmpadas LED',
                        'descricao': 'Substituição de todas as lâmpadas fluorescentes por LED na loja',
                        'preco_total': 450.00,
                        'loja_id': lojas_criadas[0].id
                    },
                    {
                        'tipo': 'veiculo',
                        'titulo': 'Revisão completa',
                        'descricao': 'Revisão geral incluindo troca de óleo, filtros e verificações',
                        'preco_total': 350.00,
                        'veiculo_id': veiculos_criados[0].id
                    }
                ]
                
                for manutencao_data in manutencao_examples:
                    data_manut = datetime.utcnow()
                    manutencao = Manutencao(
                        **manutencao_data,
                        data_manutencao=data_manut,
                        data_cadastro=data_manut
                    )
                    db.session.add(manutencao)
                
                db.session.commit()
                print("✅ Manutenções de exemplo criadas")
            
            print("\n🎉 Banco de dados configurado com sucesso!")
            print("🎯 Para rodar o sistema:")
            print("   python app.py")
            
            return True
            
    except Exception as e:
        print(f"❌ Erro ao configurar banco: {e}")
        return False

def check_database():
    """Verifica o status atual do banco de dados"""
    if not IMPORTS_SUCCESS:
        return
        
    try:
        with app.app_context():
            print("🔍 Status do banco de dados:")
            print(f"   📊 Lojas: {Loja.query.count()}")
            print(f"   🚗 Veículos: {Veiculo.query.count()}")
            print(f"   🔧 Manutenções: {Manutencao.query.count()}")
            print(f"   📷 Fotos: {FotoManutencao.query.count()}")
            
            # Verificar detalhes das lojas
            lojas = Loja.query.all()
            if lojas:
                print("\n📋 Lojas cadastradas:")
                for loja in lojas:
                    print(f"   - {loja.nome} ({loja.telefone})")
                    
            veiculos = Veiculo.query.all()
            if veiculos:
                print("\n🚗 Veículos cadastrados:")
                for veiculo in veiculos:
                    print(f"   - {veiculo.placa} - {veiculo.modelo} ({veiculo.ano})")
                    
    except Exception as e:
        print(f"❌ Erro ao verificar banco: {e}")

def reset_database():
    """Reset completo do banco de dados"""
    if not IMPORTS_SUCCESS:
        return False
        
    try:
        with app.app_context():
            print("🗑️  Resetando banco de dados...")
            db.drop_all()
            print("✅ Banco resetado")
            return init_database()
    except Exception as e:
        print(f"❌ Erro ao resetar banco: {e}")
        return False

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Configuração do banco de dados - Sistema de Manutenção')
    parser.add_argument('action', choices=['init', 'reset', 'check', 'status'], 
                       help='Ação a executar: init (inicializar), reset (reconfigurar), check/status (verificar)')
    
    args = parser.parse_args()
    
    print("🏗️  Sistema de Manutenção - Gerenciador de Banco de Dados")
    print("=" * 60)
    
    if args.action in ['init', 'reset']:
        if args.action == 'init':
            success = init_database()
        else:
            success = reset_database()
            
        if success:
            print("\n✅ Configuração concluída com sucesso!")
            print("▶️  Execute: python app.py para iniciar o sistema")
        else:
            print("\n❌ Configuração falhou!")
            sys.exit(1)
            
    elif args.action in ['check', 'status']:
        check_database()
        print("\n✅ Verificação concluída!")
    
    print("\n" + "=" * 60)
    print("🎯 Sistema pronto para uso!")
