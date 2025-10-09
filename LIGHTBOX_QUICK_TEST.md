# 🧪 Guia Rápido de Teste - Lightbox

## Como Testar a Nova Funcionalidade

### 1️⃣ Acesse uma Manutenção com Fotos

```bash
# Inicie o servidor
python app.py

# Acesse no navegador
http://localhost:5000/manutencoes
```

### 2️⃣ Clique em Qualquer Manutenção

Você será redirecionado para a página de detalhes (ex: `/manutencoes/1`)

### 3️⃣ Teste as Funcionalidades

#### ✅ Desktop
- [ ] Clique em uma foto → Lightbox abre
- [ ] Clique na seta direita → Vai para próxima foto
- [ ] Pressione `←` e `→` no teclado → Navega entre fotos
- [ ] Pressione `Esc` → Fecha o lightbox
- [ ] Clique no botão 🔍+ → Zoom aumenta
- [ ] Pressione `+` no teclado → Zoom aumenta
- [ ] Arraste a imagem com zoom aplicado → Imagem move
- [ ] Clique em uma miniatura → Vai para aquela foto
- [ ] Clique no botão ⬇ → Download da foto
- [ ] Clique fora da imagem → Fecha o lightbox

#### ✅ Mobile (ou use DevTools)
- [ ] Toque em uma foto → Lightbox abre
- [ ] Swipe esquerda → Próxima foto
- [ ] Swipe direita → Foto anterior
- [ ] Toque no X → Fecha o lightbox
- [ ] Toque em 🔍+ → Zoom aumenta

### 4️⃣ Verifique o Console

Abra o DevTools (F12) e veja os logs:

```
🖼️ Inicializando Lightbox...
✅ Lightbox inicializado com X foto(s)
📷 Lightbox aberto - Foto 1/X
✅ Foto 1 carregada
```

### 5️⃣ Teste de Responsividade

No DevTools, teste diferentes tamanhos:
- Desktop (1920x1080)
- Tablet (768x1024)
- Mobile (375x667)

Verifique se:
- Botões ficam menores em mobile
- Miniaturas desaparecem em telas < 480px
- Toolbar se adapta

---

## 🎨 O Que Você Deve Ver

### Antes (Hover na Foto)
- Imagem eleva levemente
- Overlay aparece com ícone 🔍
- Texto "Clique para ampliar"
- Borda azul

### Durante (Lightbox Aberto)
- Fundo preto 95% com blur
- Contador no topo (1/5)
- Setas laterais grandes
- Toolbar inferior com 4 botões
- Miniaturas na parte inferior
- Animação suave de entrada

### Navegação
- Setas ficam disabled nos extremos
- Miniatura ativa tem borda azul
- Scroll automático para miniatura ativa
- Transições suaves entre fotos

---

## 🐛 Problemas Comuns

### ❌ Lightbox não abre
**Solução**: Verifique se há fotos na manutenção. O lightbox só funciona se `manutencao.fotos` não estiver vazio.

### ❌ Fotos não aparecem
**Solução**: Verifique se `foto.get_url()` retorna uma URL válida. Abra o Network tab e veja se as imagens estão carregando.

### ❌ Navegação não funciona
**Solução**: Abra o console e veja se há erros JavaScript. Verifique se `data-photo-index` está presente nos elementos.

### ❌ Zoom não funciona
**Solução**: Certifique-se de que está clicando nos botões da toolbar e não na imagem diretamente.

---

## 📊 Teste de Performance

### Console Performance Test

```javascript
// Cole no console do browser
console.time('lightbox-init');
lightbox.init();
console.timeEnd('lightbox-init');
// Deve ser < 50ms
```

### Verificar FPS das Animações

1. Abra DevTools → Performance
2. Clique em Record
3. Navegue entre fotos
4. Stop recording
5. Verifique se FPS fica em ~60fps

---

## ✨ Funcionalidades Interativas para Demonstrar

### Demo Rápida (2 minutos)

1. **Abrir Lightbox**: Clique em foto
2. **Navegar**: Use setas do teclado ← →
3. **Zoom**: Pressione + algumas vezes
4. **Drag**: Arraste a imagem com zoom
5. **Miniatura**: Clique em outra miniatura
6. **Download**: Clique no botão ⬇
7. **Fechar**: Pressione Esc

### Demo Mobile (DevTools)

1. Ative modo responsivo (Ctrl+Shift+M)
2. Selecione iPhone 12 Pro
3. Clique em foto
4. Simule swipe (clique e arraste)
5. Teste botões touch

---

## 🎯 Casos de Teste

### Caso 1: Uma Foto Apenas
- Botões prev/next devem ficar disabled
- Contador mostra "1/1"
- Miniaturas mostram apenas 1 item

### Caso 2: Múltiplas Fotos (5+)
- Todas funcionalidades habilitadas
- Navegação fluida
- Miniaturas com scroll

### Caso 3: Sem Fotos
- Lightbox não é inicializado
- Sem erros no console
- Grid de fotos não aparece

---

## 📝 Checklist de Aceitação

Antes de considerar completo, verifique:

- [ ] Lightbox abre ao clicar em foto
- [ ] Navegação com setas funciona
- [ ] Navegação com teclado funciona
- [ ] Contador atualiza corretamente
- [ ] Miniaturas sincronizam com foto atual
- [ ] Zoom aumenta/diminui
- [ ] Drag funciona com zoom
- [ ] Download funciona
- [ ] Fechar com Esc funciona
- [ ] Fechar ao clicar fora funciona
- [ ] Animações são suaves
- [ ] Responsivo em mobile
- [ ] Touch gestures funcionam
- [ ] Console sem erros
- [ ] Acessível por teclado

---

**Tempo Estimado de Teste**: 10-15 minutos  
**Prioridade**: Alta (funcionalidade principal)  
**Status**: ✅ Pronto para Teste

