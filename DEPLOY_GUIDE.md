# 🚀 Guia de Deploy Seguro - GitHub + Render

## ✅ Pré-requisitos Concluídos

- ✅ Código sem credenciais expostas
- ✅ `.env.example` criado (template sem senhas)
- ✅ `.gitignore` criado (bloqueia `.env`)
- ✅ `Procfile` criado (para Render)
- ✅ `requirements.txt` atualizado com `gunicorn` e `python-dotenv`

---

## 📝 Passo 1: Preparar Ambiente Local

### Windows PowerShell:
```powershell
cd C:\Users\dirceu.gerardi\Desktop\2025-superacao\GeoreferenciamentoMongoDB

# Criar arquivo .env com suas credenciais (NUNCA versione!)
Copy-Item ".env.example" ".env"

# Editar .env com suas credenciais reais
notepad .env
```

**No arquivo `.env`, adicione:**
```
MONGO_URI=mongodb+srv://seu-usuario:sua-senha@seu-cluster.mongodb.net/?appName=lat-long-superacao
MONGO_DB=lat-long-superacao
MONGO_COLLECTION=locations
PORT=5000
FLASK_DEBUG=0
FLASK_SECRET_KEY=<gerado acima>
```

---

## 🔐 Passo 2: Verificar Segurança

### Confirmar que `.env` não será versionado:
```powershell
# Listar arquivos que serão commitados
git status

# .env NÃO deve aparecer na lista!
# Deve estar em "Ignored files"
```

---

## 📤 Passo 3: Inicializar Git e Fazer Push

### Windows PowerShell:
```powershell
# Ir para a pasta do projeto
cd C:\Users\dirceu.gerardi\Desktop\2025-superacao\GeoreferenciamentoMongoDB

# Inicializar repositório
git init
git add .
git commit -m "Initial commit: Georeferenciamento MongoDB com Flask"

# Adicionar repositório remoto
git remote add origin https://github.com/andregerardi/lat-long-mongo.git

# Renomear branch para main (padrão GitHub)
git branch -M main

# Fazer push
git push -u origin main
```

### Se receber erro de autenticação:
```powershell
# Opção 1: Usar GitHub CLI
gh auth login
# Siga as instruções e escolha "HTTPS" + "Token de acesso pessoal"

# Opção 2: Gerar token no GitHub
# https://github.com/settings/tokens (Personal access tokens → Tokens (classic))
# Permissões: repo (completo)
# Use o token como senha no prompt do Git
```

---

## 🌐 Passo 4: Deploy no Render.com

### 1️⃣ Criar Web Service no Render:
- Acesse https://render.com
- Clique em **New** → **Web Service**
- Selecione **GitHub** e conecte sua conta
- Escolha repositório `lat-long-mongo`

### 2️⃣ Configurar Build e Start:

| Campo | Valor |
|-------|-------|
| **Name** | `lat-long-mongo` (ou seu nome) |
| **Runtime** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `gunicorn app-mongo:app` |

### 3️⃣ Adicionar Variáveis de Ambiente:

Clique em **Environment** e adicione:

```
MONGO_URI=mongodb+srv://seu-usuario:sua-senha@seu-cluster.mongodb.net/?appName=lat-long-superacao
MONGO_DB=lat-long-superacao
MONGO_COLLECTION=locations
FLASK_DEBUG=0
FLASK_SECRET_KEY=<seu-secret-key>
PORT=5000
```

### 4️⃣ Deploy:
- Clique em **Create Web Service**
- Aguarde ~5 minutos enquanto o Render faz build e deploy
- URL estará disponível em `https://seu-app.onrender.com`

---

## ✅ Validação Pós-Deploy

### Testar se tudo está funcionando:

```bash
# 1. Acesse a URL pública
https://seu-app.onrender.com

# 2. Verifique logs no Render
# Dashboard → seu-app → Logs

# 3. Teste capturar uma localização
# Clique em "📍 Capturar Localização"
# Deve aparecer no histórico

# 4. Verifique se dados estão no MongoDB
# MongoDB Atlas → seu-cluster → collections → locations
```

---

## 🔒 Segurança - Checklist Final

- ✅ `.env` está em `.gitignore` (não vai para GitHub)
- ✅ Senha do MongoDB NÃO está no código
- ✅ `git status` mostra apenas arquivos públicos
- ✅ Render tem variáveis de ambiente configuradas
- ✅ HTTPS está ativo na URL do Render
- ✅ IP whitelist no MongoDB Atlas (opcional)

---

## ⚠️ SE JÁ COMMITOU A SENHA

Se acidentalmente commitou a senha:

```powershell
# 1. REGENERAR SENHA NO MONGODB ATLAS IMEDIATAMENTE
# https://cloud.mongodb.com → seu-cluster → Database Access

# 2. Remover arquivo do histórico Git (usar BFG Repo-Cleaner ou git-filter-branch)
# Isso é complexo, melhor prevenir!

# 3. Atualizar variáveis no Render com nova senha
```

---

## 📞 Próximas Melhorias (Opcional)

- [ ] Adicionar autenticação de usuários
- [ ] Rate limiting na API
- [ ] Logs mais detalhados
- [ ] Dashboard de administração
- [ ] Backup automático do MongoDB
- [ ] Alertas em caso de erro

---

**Status:** ✅ Pronto para produção
**Segurança:** ✅ Credenciais protegidas
**Deploy:** ✅ Automatizado via GitHub + Render
