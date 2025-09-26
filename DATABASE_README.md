# 📊 Configuração e Gerenciamento do Banco de Dados
**Sistema de Manutenção - Supermercado Santo Antonio Super Mais**

## 🚀 Configuração Rápida

### 1. Instalar Dependências
```bash
python install_deps.py
```

### 2. Configurar Banco de Dados
```bash
# Opção 1: Configuração básica
python setup_db.py init

# Opção 2: Iniciar aplicação (cria banco automaticamente)
python app.py
```

### 3. Verificar Status do Banco
```bash
python setup_db.py status
```

## 📋 Estrutura do Banco de Dados

### 🔗 **Modelos Principais:**

#### 📍 **Loja**
- `id` - Chave primária
- `nome` - Nome da loja (único)
- `endereco` - Endereço completo
- `telefone` - Número de contato
- `data_cadastro` - Data de criação

#### 🚗 **Veículo**
- `id` - Chave primária
- `placa` - Placa do veículo (única)
- `modelo` - Modelo do veículo
- `marca` - Marca fabricante
- `ano` - Ano do veículo
- `cor` - Cor do veículo
- `data_cadastro` - Data de cadastro

#### 🔧 **Manutenção**
- `id` - Chave primária
- `tipo` - 'loja' ou 'veiculo'
- `titulo` - Título da manutenção
- `descricao` - Detalhes da manutenção
- `preco_total` - Custo total
- `data_manutencao` - Data da manutenção
- `data_cadastro` - Data de registro
- `loja_id` - Referência à loja (FK)
- `veiculo_id` - Referência ao veículo (FK)

#### 📷 **FotoManutenção**
- `id` - Chave primária
- `nome_arquivo` - Nome do arquivo
- `caminho_arquivo` - Caminho físico
- `data_upload` - Data do upload
- `manutencao_id` - Referência à manutenção (FK)

## 🗄️ Configurações de Banco Suportadas

### **SQLite (Desenvolvimento)**
⚠️ **Configuração padrão, ideal para desenvolvimento**:
```bash
python app.py  # Funciona automaticamente
```

### **PostgreSQL (Produção)**
💡 **Para ambiente de produção**:
```bash
# Instalar dependência
pip install psycopg2-binary

# Configurar variável de ambiente
export DATABASE_URL=postgresql://usuario:senha@localhost:5432/manutencao_supermais

# Executar sistema
python app.py
```

### **MySQL (Produção)**
💡 **Alternativa para produção**:
```bash
# Instalar dependência
pip install PyMySQL

# Configurar variável de ambiente  
export DATABASE_URL=mysql://usuario:senha@localhost:3306/manutencao_supermais

# Executar sistema
python app.py
```

## 🔧 Comandos de Gerenciamento

### **Setup Inicial**
```bash
# Instalar dependências necessárias
python install_deps.py

# Configurar banco e dados de exemplo
python setup_db.py init

# Iniciar aplicação
python app.py
```

### **Gerenciamento do Banco**
```bash
# Verificar status atual
python setup_db.py status

# Reset completo (⚠️ APAGA TODOS OS DADOS)
python setup_db.py reset

# Apenas configura nova estrutura
python setup_db.py init
```

## 🛠️ Solução de Problemas

### **Erro: Módulo não encontrado**
```bash
# Instalar dependências
pip install flask flask-sqlalchemy python-dotenv werkzeug
```

### **Erro: Banco não conecta**
```bash
# Verificar se as tabelas existem
python setup_db.py status

# Recriar estrutura do banco
python setup_db.py init
```

### **Erro: Permissões de arquivo**
```bash
# Verificar propriedades dos arquivos
ls -la database.db

# Dar permissões se necessário
chmod 664 database.db
```

## 📈 Monitoramento

### **Status do Banco**
```bash
python setup_db.py status

# Mostra:
# - Número de lojas cadastradas
# - Número de veículos cadastrados
# - Número de manutenções realizadas
# - Número de fotos anexadas
```

### **Logs da Aplicação**
O sistema mostra automaticamente:
- ✅ Status das tabelas criadas
- 📊 Contadores de registro
- ⚠️ Avisos de erro
- 🔄 Operações realizadas com sucesso

## ⚡ Desenvolvimento vs Produção

### **Desenvolvimento (Atual)**
- ✅ SQLite (arquivo local)
- ✅ Dados de exemplo incluídos
- ✅ Configuração automática
- ✅ Ideal para testes

### **Produção (Recomendado)**
- 🏗️ PostgreSQL ou MySQL
- 🔐 Variáveis de ambiente
- 🔒 Backup automatizado
- 📡 Ambiente escalável

## 🎯 Próximos Passos

1. **Teste o sistema**: `python app.py`
2. **Acesse**: `http://localhost:5000`
3. **Configure para produção**: Mude `DATABASE_URL`
4. **Faça backups**: Configure `DATABASE_URL` externa

---

⭐ **Pronto para usar!** O sistema estará totalmente funcional após a configuração inicial.
