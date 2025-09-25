# Sistema de Manutenção - Supermercado Santo Antonio Super Mais

## 📋 Descrição

Sistema web completo para gerenciamento de manutenções das 7 lojas e frota de veículos do Supermercado Santo Antonio Super Mais. Desenvolvido para uso do chefe de manutenção (mobile) e do dono das lojas (desktop e mobile).

## 🚀 Funcionalidades

### 🏪 Gestão de Lojas
- Cadastro completo de lojas com endereço e telefone
- Visualização organizada por seções
- Histórico de manutenções por loja
- Estatísticas de gastos por loja

### 🚗 Gestão da Frota
- Cadastro de veículos com placa, modelo, marca, ano e cor
- Organização por placas
- Histórico de manutenções por veículo
- Estatísticas de gastos por veículo

### 🔧 Gestão de Manutenções
- Cadastro de manutenções para lojas e veículos
- Upload de múltiplas fotos por manutenção
- Descrição detalhada dos serviços
- Controle de preços e custos
- Data da manutenção personalizável

### 📊 Dashboard e Relatórios
- Estatísticas gerais em tempo real
- Visualização de manutenções recentes
- Total de gastos por categoria
- Interface responsiva para mobile e desktop

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3.11 + Flask
- **Banco de Dados**: SQLite + SQLAlchemy
- **Frontend**: HTML5 + CSS3 + JavaScript
- **Framework CSS**: Pico CSS (responsivo)
- **Upload de Arquivos**: Werkzeug

## 📱 Responsividade

O sistema foi desenvolvido com foco na responsividade:
- **Mobile**: Interface otimizada para smartphones
- **Tablet**: Layout adaptado para tablets
- **Desktop**: Interface completa para computadores

## 🚀 Como Executar

### Pré-requisitos
- Python 3.11 ou superior
- pip (gerenciador de pacotes Python)

### Instalação

1. **Clone ou baixe o projeto**
```bash
cd manutencao_supermais
```

2. **Ative o ambiente virtual**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

3. **Instale as dependências**
```bash
pip install -r requirements.txt
```

4. **Execute a aplicação**
```bash
python app.py
```

5. **Acesse no navegador**
```
http://localhost:5000
```

## 📁 Estrutura do Projeto

```
manutencao_supermais/
├── app.py                 # Aplicação principal Flask
├── database.db           # Banco de dados SQLite
├── static/
│   └── uploads/          # Pasta para fotos das manutenções
├── templates/            # Templates HTML
│   ├── base.html         # Template base responsivo
│   ├── index.html        # Dashboard principal
│   ├── lojas.html        # Listagem de lojas
│   ├── cadastrar_loja.html
│   ├── detalhes_loja.html
│   ├── veiculos.html     # Listagem de veículos
│   ├── cadastrar_veiculo.html
│   ├── detalhes_veiculo.html
│   ├── manutencoes.html  # Listagem de manutenções
│   ├── cadastrar_manutencao.html
│   └── detalhes_manutencao.html
└── venv/                 # Ambiente virtual Python
```

## 👥 Usuários do Sistema

### Chefe de Manutenção
- **Dispositivo**: Mobile (smartphone)
- **Funcionalidades**: 
  - Cadastrar manutenções
  - Upload de fotos
  - Visualizar histórico
  - Acesso rápido via mobile

### Dono das Lojas
- **Dispositivo**: Desktop e Mobile
- **Funcionalidades**:
  - Visualizar todas as estatísticas
  - Acompanhar gastos por loja/veículo
  - Relatórios completos
  - Interface administrativa

## 🔧 Funcionalidades Principais

### Dashboard
- Estatísticas em tempo real
- Ações rápidas
- Manutenções recentes
- Visão geral das lojas e frota

### Gestão de Lojas
- Cadastro com informações completas
- Histórico de manutenções
- Cálculo de gastos por loja

### Gestão da Frota
- Cadastro de veículos
- Organização por placas
- Histórico de manutenções
- Cálculo de gastos por veículo

### Manutenções
- Cadastro detalhado
- Upload de fotos
- Categorização por tipo (loja/veículo)
- Controle de custos

## 📸 Suporte a Fotos

- Upload de múltiplas fotos por manutenção
- Formatos suportados: PNG, JPG, JPEG, GIF, WEBP
- Pré-visualização antes do upload
- Visualização em galeria
- Modal para visualização ampliada

## 💰 Controle Financeiro

- Registro de preços por manutenção
- Cálculo automático de totais
- Relatórios de gastos por categoria
- Estatísticas em tempo real

## 🔒 Segurança

- Validação de tipos de arquivo
- Sanitização de nomes de arquivo
- Limite de tamanho de upload (16MB)
- Validação de dados de entrada

## 📱 Interface Mobile

- Design responsivo
- Navegação otimizada para touch
- Botões grandes e acessíveis
- Layout adaptativo

## 🖥️ Interface Desktop

- Layout em grid responsivo
- Navegação completa
- Visualização otimizada
- Funcionalidades avançadas

## 🚀 Próximas Funcionalidades

- [ ] Relatórios em PDF
- [ ] Exportação de dados
- [ ] Sistema de usuários e permissões
- [ ] Notificações por email
- [ ] Backup automático
- [ ] API REST para integrações

## 📞 Suporte

Para dúvidas ou suporte técnico, entre em contato com a equipe de desenvolvimento.

---

**Supermercado Santo Antonio Super Mais**  
Sistema de Manutenção v1.0  
© 2024 - Todos os direitos reservados
