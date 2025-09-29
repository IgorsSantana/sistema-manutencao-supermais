# Configuração do Cloudinary para Armazenamento de Imagens

## 🎯 Problema Resolvido

O Render tem um sistema de arquivos **efêmero**, ou seja, quando você faz deploy, todos os arquivos de upload são perdidos. Esta configuração resolve o problema usando Cloudinary para armazenar as imagens permanentemente.

## ☁️ O que é Cloudinary?

Cloudinary é um serviço de gerenciamento de mídia na nuvem que oferece:
- ✅ **Armazenamento permanente** de imagens
- ✅ **Redimensionamento automático** e otimização
- ✅ **CDN global** para carregamento rápido
- ✅ **Plano gratuito** com 25GB de armazenamento
- ✅ **Transformações** de imagem em tempo real

## 🔧 Configuração no Render

### 1. Criar Conta no Cloudinary

1. Acesse [cloudinary.com](https://cloudinary.com)
2. Clique em "Sign Up For Free"
3. Preencha os dados e confirme o email
4. Acesse o Dashboard

### 2. Obter Credenciais

No Dashboard do Cloudinary, você encontrará:
- **Cloud Name**: Nome da sua conta
- **API Key**: Chave de API
- **API Secret**: Segredo da API

### 3. Configurar no Render

No painel do Render, vá para seu serviço e adicione as seguintes variáveis de ambiente:

```
CLOUDINARY_CLOUD_NAME=seu_cloud_name_aqui
CLOUDINARY_API_KEY=sua_api_key_aqui
CLOUDINARY_API_SECRET=seu_api_secret_aqui
```

### 4. Deploy

Após configurar as variáveis, faça o deploy. O app detectará automaticamente o Cloudinary e usará para armazenar as imagens.

## 🔄 Como Funciona

### Modo Híbrido (Automático)

O app detecta automaticamente se o Cloudinary está configurado:

- **Com Cloudinary**: Imagens são enviadas para a nuvem
- **Sem Cloudinary**: Imagens são salvas localmente (desenvolvimento)

### Fluxo de Upload

```
1. Usuário seleciona foto
2. App verifica se Cloudinary está configurado
3. Se SIM: Upload para Cloudinary + salva URLs no banco
4. Se NÃO: Salva localmente + salva caminho no banco
5. Templates usam foto.get_url() para exibir
```

## 📊 Benefícios

### Para o Render
- ✅ **Sem perda de imagens** em deploys
- ✅ **Menos uso de espaço** no servidor
- ✅ **Performance melhorada** (CDN)

### Para o Usuário
- ✅ **Carregamento mais rápido** das imagens
- ✅ **Imagens sempre disponíveis**
- ✅ **Qualidade otimizada** automaticamente

## 🛠️ Desenvolvimento Local

Para desenvolvimento local, você pode:

1. **Usar Cloudinary**: Configure as variáveis no `.env`
2. **Usar Local**: Não configure as variáveis (padrão)

## 📝 Exemplo de Uso

```python
# O app detecta automaticamente
if is_cloudinary_configured():
    # Upload para Cloudinary
    result = upload_to_cloudinary(file)
else:
    # Upload local
    result = save_locally(file)
```

## 🔍 Verificação

Para verificar se está funcionando:

1. Acesse o app no Render
2. Cadastre uma manutenção com foto
3. Verifique se a foto aparece corretamente
4. Faça um novo deploy
5. Verifique se a foto ainda aparece (não deve sumir!)

## 🆘 Troubleshooting

### Imagens não aparecem
- Verifique se as variáveis de ambiente estão corretas
- Verifique os logs do Render para erros
- Teste as credenciais no Dashboard do Cloudinary

### Erro de upload
- Verifique se a conta Cloudinary está ativa
- Verifique se não excedeu o limite gratuito
- Verifique a conectividade com a internet

## 💰 Custos

- **Plano Gratuito**: 25GB de armazenamento
- **Transformações**: 25.000 por mês
- **Bandwidth**: 25GB por mês
- **Suficiente para**: Milhares de manutenções com fotos

## 🎉 Resultado

Após a configuração:
- ✅ Imagens **nunca mais** serão perdidas em deploys
- ✅ Carregamento **mais rápido** das imagens
- ✅ Armazenamento **permanente** e confiável
- ✅ **Zero configuração** adicional no código
