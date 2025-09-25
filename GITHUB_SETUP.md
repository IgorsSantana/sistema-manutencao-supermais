# 🚀 Configuração do GitHub

## Passos para Conectar ao GitHub

### 1. Criar Repositório no GitHub
1. Acesse: https://github.com
2. Clique em "New" ou "+" → "New repository"
3. Configure:
   - **Nome**: `sistema-manutencao-supermais`
   - **Descrição**: `Sistema de Manutenção - Supermercado Santo Antonio Super Mais`
   - **Visibilidade**: Public ou Private
   - **NÃO marque** nenhuma opção adicional
4. Clique em "Create repository"

### 2. Conectar Repositório Local
Execute os comandos abaixo (substitua `SEU_USUARIO` pelo seu username do GitHub):

```bash
# Adicionar o repositório remoto
git remote add origin https://github.com/SEU_USUARIO/sistema-manutencao-supermais.git

# Fazer push do código
git push -u origin main
```

### 3. Verificar Upload
- Acesse seu repositório no GitHub
- Verifique se todos os arquivos foram enviados
- O README.md será exibido automaticamente

## 📁 Estrutura do Projeto no GitHub

```
sistema-manutencao-supermais/
├── README.md                    # Documentação principal
├── INSTRUCOES_USO.md           # Manual de uso
├── GITHUB_SETUP.md             # Este arquivo
├── requirements.txt             # Dependências Python
├── app.py                      # Aplicação principal
├── config.py                   # Configurações
├── populate_data.py            # Dados iniciais
├── start.bat                   # Script Windows
├── start.sh                    # Script Linux/Mac
├── .gitignore                  # Arquivos ignorados
├── templates/                  # Templates HTML
│   ├── base.html
│   ├── index.html
│   └── ...
└── static/
    └── uploads/
        └── .gitkeep
```

## 🔧 Próximos Passos

1. **Clone** o repositório em outros computadores
2. **Colabore** com outros desenvolvedores
3. **Crie issues** para bugs e melhorias
4. **Use branches** para novas funcionalidades
5. **Faça releases** para versões estáveis

## 📝 Comandos Git Úteis

```bash
# Ver status
git status

# Adicionar mudanças
git add .

# Fazer commit
git commit -m "Descrição da mudança"

# Fazer push
git push

# Fazer pull
git pull

# Ver histórico
git log --oneline
```

## 🎯 Benefícios do GitHub

- ✅ **Backup** do código
- ✅ **Versionamento** completo
- ✅ **Colaboração** em equipe
- ✅ **Histórico** de mudanças
- ✅ **Issues** e **Pull Requests**
- ✅ **Deploy** automático (futuro)
- ✅ **Documentação** online
