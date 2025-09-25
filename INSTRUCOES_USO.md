# 📋 Instruções de Uso - Sistema de Manutenção

## 🚀 Como Iniciar o Sistema

### Opção 1: Script Automático (Recomendado)
1. **Windows**: Execute `start.bat`
2. **Linux/Mac**: Execute `./start.sh`

### Opção 2: Manual
1. Abra o terminal/prompt de comando
2. Navegue até a pasta do projeto
3. Ative o ambiente virtual:
   - Windows: `venv\Scripts\activate`
   - Linux/Mac: `source venv/bin/activate`
4. Execute: `python app.py`
5. Acesse: http://localhost:5000

## 📱 Acesso ao Sistema

### Para o Chefe de Manutenção (Mobile)
- **URL**: http://localhost:5000
- **Dispositivo**: Smartphone ou tablet
- **Navegador**: Chrome, Safari, Firefox (qualquer navegador moderno)

### Para o Dono das Lojas (Desktop/Mobile)
- **URL**: http://localhost:5000
- **Dispositivo**: Computador, tablet ou smartphone
- **Navegador**: Qualquer navegador moderno

## 🏪 Cadastro de Lojas

1. Acesse **"🏪 Lojas"** no menu
2. Clique em **"➕ Nova Loja"**
3. Preencha os dados:
   - Nome da loja (obrigatório)
   - Endereço (opcional)
   - Telefone (opcional)
4. Clique em **"💾 Salvar Loja"**

## 🚗 Cadastro de Veículos

1. Acesse **"🚗 Frota"** no menu
2. Clique em **"➕ Novo Veículo"**
3. Preencha os dados:
   - Placa (obrigatório)
   - Modelo (obrigatório)
   - Marca (opcional)
   - Ano (opcional)
   - Cor (opcional)
4. Clique em **"💾 Salvar Veículo"**

## 🔧 Cadastro de Manutenções

1. Acesse **"🔧 Manutenções"** no menu
2. Clique em **"➕ Nova Manutenção"**
3. Preencha os dados:
   - **Tipo**: Escolha entre Loja ou Veículo
   - **Título**: Nome da manutenção
   - **Descrição**: Detalhes do serviço
   - **Preço Total**: Valor gasto
   - **Data**: Data da manutenção
   - **Loja/Veículo**: Selecione o item
   - **Fotos**: Anexe fotos (opcional)
4. Clique em **"💾 Salvar Manutenção"**

## 📊 Dashboard Principal

O dashboard mostra:
- **Estatísticas Gerais**: Total de lojas, veículos, manutenções e gastos
- **Ações Rápidas**: Botões para cadastros rápidos
- **Lojas Cadastradas**: Lista com informações básicas
- **Frota de Veículos**: Lista com informações básicas
- **Manutenções Recentes**: Últimas manutenções realizadas

## 📱 Interface Mobile

### Navegação
- Menu horizontal na parte superior
- Botões grandes e acessíveis
- Layout adaptativo para telas pequenas

### Funcionalidades
- Todas as funcionalidades disponíveis
- Upload de fotos otimizado
- Formulários responsivos

## 🖥️ Interface Desktop

### Navegação
- Menu completo com todas as opções
- Layout em grid responsivo
- Visualização otimizada

### Funcionalidades
- Todas as funcionalidades disponíveis
- Visualização de estatísticas em tempo real
- Relatórios detalhados

## 📷 Upload de Fotos

### Formatos Suportados
- PNG, JPG, JPEG, GIF, WEBP
- Tamanho máximo: 16MB por arquivo

### Como Fazer Upload
1. No cadastro de manutenção, clique em **"Escolher arquivos"**
2. Selecione uma ou múltiplas fotos
3. Visualize as fotos na pré-visualização
4. Salve a manutenção

### Visualização
- Galeria de fotos em grid
- Clique na foto para ampliar
- Modal com visualização em tamanho real

## 🔍 Visualização de Dados

### Lojas
- Lista com informações básicas
- Clique em **"Ver Detalhes"** para:
  - Informações completas
  - Histórico de manutenções
  - Estatísticas de gastos

### Veículos
- Lista com informações básicas
- Clique em **"Ver Detalhes"** para:
  - Informações completas
  - Histórico de manutenções
  - Estatísticas de gastos

### Manutenções
- Lista com filtros por tipo
- Clique em **"Ver Detalhes"** para:
  - Informações completas
  - Fotos anexadas
  - Links para loja/veículo

## 📊 Relatórios e Estatísticas

### Dashboard
- Total de lojas cadastradas
- Total de veículos na frota
- Total de manutenções realizadas
- Total de gastos (atualizado em tempo real)

### Por Loja
- Número de manutenções
- Total gasto na loja
- Histórico completo

### Por Veículo
- Número de manutenções
- Total gasto no veículo
- Histórico completo

## 🛠️ Manutenção do Sistema

### Backup
- O banco de dados está em `database.db`
- Faça backup regular deste arquivo
- As fotos estão em `static/uploads/`

### Atualizações
- Para atualizar, pare o sistema (Ctrl+C)
- Substitua os arquivos necessários
- Reinicie o sistema

## ❓ Solução de Problemas

### Erro de Módulo não Encontrado
- Ative o ambiente virtual: `venv\Scripts\activate` (Windows)
- Instale as dependências: `pip install -r requirements.txt`

### Erro de Banco de Dados
- Delete o arquivo `database.db`
- Execute `python populate_data.py` para recriar

### Erro de Upload de Fotos
- Verifique se a pasta `static/uploads/` existe
- Verifique as permissões da pasta
- Verifique o tamanho do arquivo (máximo 16MB)

### Sistema Não Inicia
- Verifique se a porta 5000 está livre
- Verifique se o Python está instalado
- Verifique se o ambiente virtual está ativo

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique este arquivo de instruções
2. Consulte o README.md
3. Verifique os logs do sistema
4. Entre em contato com o suporte técnico

---

**Supermercado Santo Antonio Super Mais**  
Sistema de Manutenção v1.0  
© 2024 - Todos os direitos reservados
