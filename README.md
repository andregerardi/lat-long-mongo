# Georeferenciamento MongoDB

Aplicativo Flask para captura de latitude/longitude em navegadores móveis, salvando os pontos em MongoDB e exibindo histórico em mapa (Leaflet).

## ⚠️ SEGURANÇA - Leia Antes de Fazer Deploy

**NUNCA commite credenciais no GitHub!**

### Configuração Segura

1. **Copie `.env.example` para `.env`:**
   ```bash
   cp .env.example .env
   ```

2. **Edite `.env` com suas credenciais (NÃO versione este arquivo):**
   ```bash
   MONGO_URI=mongodb+srv://seu-user:sua-senha@seu-cluster.mongodb.net/?appName=lat-long-superacao
   ```

3. **O arquivo `.gitignore` já protege `.env` de commits acidentais.**

### No Render.com - Adicione Variáveis de Ambiente

1. Dashboard do Render → seu serviço → **Environment**
2. Adicione:
   - `MONGO_URI` = sua string de conexão MongoDB
   - `MONGO_DB` = `lat-long-superacao`
   - `MONGO_COLLECTION` = `locations`
3. Salve e aguarde redeploy automático

### No GitHub

✅ **Versione:**
- `requirements.txt`, `.env.example`, `.gitignore`, código

❌ **NÃO versione:**
- `.env` (credenciais reais)

---

## Requisitos
- Python 3.10+
- MongoDB Atlas (gratuito em https://www.mongodb.com/cloud/atlas)
- Render.com (gratuito) para deploy

## Configuração Local

1. Clone este repositório.
2. Copie `.env.example` para `.env` e configure `MONGO_URI`.
3. Instale dependências:
   ```bash
   pip install -r requirements.txt
   ```
4. Rode o servidor:
   ```bash
   python app-mongo.py
   ```
5. Acesse em `http://localhost:5000`.

## Funcionalidades
- Captura de localização via `navigator.geolocation` (Android/iOS/desktop com permissão).
- Formulário com município, agente e observações.
- Salvamento em MongoDB com timestamp UTC, precisão, altitude e velocidade (quando disponíveis).
- Histórico em tabela e mapa com marcadores coloridos por agente.
- Deleção de pontos pelo histórico.

## Deploy no Render.com

1. **Criar repositório GitHub** com seu código
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/seu-usuario/seu-repo.git
   git push -u origin main
   ```

2. **Criar Web Service no Render:**
   - Acesse https://render.com
   - New → Web Service
   - Conecte seu repositório GitHub
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app-mongo:app`

3. **Adicionar Variáveis de Ambiente (no dashboard do Render):**
   - Environment → Add Environment Variable
   - `MONGO_URI` = sua string MongoDB
   - `MONGO_DB` = `lat-long-superacao`
   - `MONGO_COLLECTION` = `locations`

4. **Aguarde o deploy automático!**

## Endpoints
- `GET /` — página principal.
- `POST /api/save-location` — salva ponto. Payload:
  ```json
  {
    "latitude": -23.55,
    "longitude": -46.63,
    "accuracy": 12.3,
    "altitude": null,
    "speed": null,
    "agent_name": "Agente",
    "municipio": "Cidade",
    "observacoes": "Anotações"
  }
  ```
- `GET /api/get-locations` — lista pontos (ordenado por timestamp desc).
- `DELETE /api/delete-location/<id>` — remove um ponto.

## Estrutura
- `app-mongo.py` — servidor Flask e rotas API.
- `templates/index.html` — frontend Leaflet + JS de captura.
- `static/municipios_agentes.json` — lista de municípios/agentes para o select.
- `requirements.txt` — dependências Python.
- `.env.example` — template de configuração (sem credenciais).
- `.gitignore` — arquivos ignorados no Git.

## Dicas de Segurança
- **NUNCA commite credenciais** — use `.env` com `.gitignore`.
- Use **HTTPS em produção** (Render faz automaticamente).
- Mantenha credenciais em **variáveis de ambiente**.
- Se expôs a senha: **regenere imediatamente** no MongoDB Atlas.
- Use **IP whitelist no MongoDB Atlas** para maior segurança (opcional).

## Dicas de Performance
- Considere criar índice 2dsphere no MongoDB se usar queries geoespaciais.
- Monitore uso da API no painel do Render (plano gratuito tem limitações).

## Problemas Comuns
- **"MONGO_URI não configurada"**: configure a variável de ambiente no Render ou localmente.
- **"Permissão negada"**: verifique se o navegador tem acesso ao GPS.
- **"Sem mapa histórico"**: confira se MongoDB está acessível e se há dados.
- **"Carregamento de municípios"**: verifique se `static/municipios_agentes.json` está no caminho correto.

