# populate_data.py
# Script para popular o banco de dados com dados iniciais

from app import app, db, Loja, Veiculo, Manutencao, FotoManutencao
from datetime import datetime, timedelta
import random

def populate_initial_data():
    """Popula o banco de dados com dados iniciais para demonstração"""
    
    with app.app_context():
        # Criar tabelas se não existirem
        db.create_all()
        
        # Verificar se já existem dados
        if Loja.query.first():
            print("Dados já existem no banco. Pulando população inicial.")
            return
        
        print("Populando banco de dados com dados iniciais...")
        
        # Criar lojas
        lojas_data = [
            {"nome": "Loja Centro", "endereco": "Rua Principal, 123 - Centro", "telefone": "(11) 3333-1111"},
            {"nome": "Loja Norte", "endereco": "Av. Norte, 456 - Zona Norte", "telefone": "(11) 3333-2222"},
            {"nome": "Loja Sul", "endereco": "Rua Sul, 789 - Zona Sul", "telefone": "(11) 3333-3333"},
            {"nome": "Loja Leste", "endereco": "Av. Leste, 321 - Zona Leste", "telefone": "(11) 3333-4444"},
            {"nome": "Loja Oeste", "endereco": "Rua Oeste, 654 - Zona Oeste", "telefone": "(11) 3333-5555"},
            {"nome": "Loja Shopping", "endereco": "Shopping Center, Loja 101", "telefone": "(11) 3333-6666"},
            {"nome": "Loja Express", "endereco": "Rua Expressa, 987 - Centro", "telefone": "(11) 3333-7777"}
        ]
        
        lojas = []
        for loja_data in lojas_data:
            loja = Loja(**loja_data)
            db.session.add(loja)
            lojas.append(loja)
        
        # Criar veículos
        veiculos_data = [
            {"placa": "ABC-1234", "modelo": "Fiat Uno", "marca": "Fiat", "ano": 2020, "cor": "Branco"},
            {"placa": "DEF-5678", "modelo": "Volkswagen Gol", "marca": "Volkswagen", "ano": 2019, "cor": "Prata"},
            {"placa": "GHI-9012", "modelo": "Chevrolet Onix", "marca": "Chevrolet", "ano": 2021, "cor": "Azul"},
            {"placa": "JKL-3456", "modelo": "Ford Ka", "marca": "Ford", "ano": 2018, "cor": "Vermelho"},
            {"placa": "MNO-7890", "modelo": "Renault Sandero", "marca": "Renault", "ano": 2022, "cor": "Preto"},
            {"placa": "PQR-1234", "modelo": "Honda Civic", "marca": "Honda", "ano": 2020, "cor": "Cinza"},
            {"placa": "STU-5678", "modelo": "Toyota Corolla", "marca": "Toyota", "ano": 2021, "cor": "Branco"}
        ]
        
        veiculos = []
        for veiculo_data in veiculos_data:
            veiculo = Veiculo(**veiculo_data)
            db.session.add(veiculo)
            veiculos.append(veiculo)
        
        # Commit para salvar lojas e veículos
        db.session.commit()
        
        # Criar algumas manutenções de exemplo
        manutencoes_data = [
            {
                "tipo": "loja",
                "titulo": "Troca de lâmpadas",
                "descricao": "Substituição de 15 lâmpadas LED no setor de hortifrúti. Lâmpadas antigas estavam com baixa luminosidade.",
                "preco_total": 450.00,
                "data_manutencao": datetime.now() - timedelta(days=5),
                "loja_id": lojas[0].id
            },
            {
                "tipo": "veiculo",
                "titulo": "Revisão preventiva",
                "descricao": "Revisão completa do veículo incluindo troca de óleo, filtros e verificação de freios.",
                "preco_total": 320.00,
                "data_manutencao": datetime.now() - timedelta(days=3),
                "veiculo_id": veiculos[0].id
            },
            {
                "tipo": "loja",
                "titulo": "Reparo no sistema de refrigeração",
                "descricao": "Correção de vazamento no sistema de refrigeração do setor de frios. Substituição de mangueiras e recarga de gás.",
                "preco_total": 850.00,
                "data_manutencao": datetime.now() - timedelta(days=7),
                "loja_id": lojas[1].id
            },
            {
                "tipo": "veiculo",
                "titulo": "Troca de pneus",
                "descricao": "Substituição de 4 pneus dianteiros. Pneus antigos estavam carecas e apresentavam risco de segurança.",
                "preco_total": 680.00,
                "data_manutencao": datetime.now() - timedelta(days=2),
                "veiculo_id": veiculos[1].id
            },
            {
                "tipo": "loja",
                "titulo": "Manutenção do ar condicionado",
                "descricao": "Limpeza e manutenção dos aparelhos de ar condicionado. Substituição de filtros e recarga de gás refrigerante.",
                "preco_total": 1200.00,
                "data_manutencao": datetime.now() - timedelta(days=10),
                "loja_id": lojas[2].id
            }
        ]
        
        for manutencao_data in manutencoes_data:
            manutencao = Manutencao(**manutencao_data)
            db.session.add(manutencao)
        
        # Commit final
        db.session.commit()
        
        print("✅ Dados iniciais criados com sucesso!")
        print(f"   - {len(lojas)} lojas cadastradas")
        print(f"   - {len(veiculos)} veículos cadastrados")
        print(f"   - {len(manutencoes_data)} manutenções de exemplo criadas")
        print("\n🚀 Sistema pronto para uso!")
        print("   Acesse: http://localhost:5000")

if __name__ == "__main__":
    populate_initial_data()
