# 🔧 FIX DE BUILD COMMAND - RENDER DASHBOARD

## ❌ **Problema Detectado:**
- O Render está executando `pip install -r requirements.txt && python populate_data.py` 
- Mas o arquivo `populate_data.py` foi removido
- Isso causa o erro: `python: can't open file 'populate_data.py': No such file or directory`

## ✅ **SOLUÇÕES IMEDIATAS:**

### **Opção 1: Update via Dashboard Render (MANUAL)**
1. Vá para [Render Dashboard](https://dashboard.render.com)
2. Selected your **Web Service** → **sistema-manutencao-supermais** 
3. Click **"Settings"** tab
4. Scroll down to **"Build Command"**
5. Change: `pip install -r requirements.txt && python populate_data.py`
   **to:** `pip install -r requirements.txt`
6. Click **"Save Changes"**  
7. Click **"Manual Deploy"** to trigger new build

### **Opção 2: Environment Variable (OVERIDE)**
No Render Dashboard → Environment Variables → Add:
```
Key: BUILD_COMMAND
Value: pip install -r requirements.txt
```

### **Opção 3: Git Fix (this code publish is ready)**
Current changes committed + pushed:
- ✅ `render.yaml` → `buildCommand: pip install -r requirements.txt`
- ✅ `populate_data.py` deleted
- ✅ Dependencies upgraded

**Next step:** Wait for automatic redeploy ou manual trigger

## ⏭️ **AFTER APPLYING FIX (Qualquer uma das 3 opções acima):**

### ✅ **Build Success Logs should become:**
```
✅ Installing dependencies...
Successfully built psycopg2-binary-2.9.9
Installing collected packages: typing-extensions, python-dotenv, psycopg2-binary...
==> Build succeeded!
==> Running 'gunicorn app:app'
🌐 Conectando ao PostgreSQL (Render)...
📊 PostgreSQL detectado - criando tabelas...
✅ Schema PostgreSQL configurado!
Service started...
✅ Your service is live at https://sistema-manutencao-supermais.onrender.com
```

### 🚨 **CRITICAL IF PROBLEM CONTINUES:**
Se ainda persiste o problema após ajuste manual:

- Cache do Render pode estar usando build configuration anterior
- **Solution EXTREMA:** Delete and recreate service (reset all env vars)
- This é the fastest route porque limpa any configs cached
- Redeploy será required to reset |⇒ Banco PostgreSQL seria needed again

**BOM SUCESSO COM BUILD COMMAND FIX!** 🔧 ⚡   
After sorting, function end-to-end including databases, GUI and persisting data into cloud Render PostgreSQL.
