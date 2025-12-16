# ✅ Checklist de Segurança para Deploy

## Antes de fazer Push para GitHub

- [ ] ✅ Removeu senha da `MONGO_URI` do código (`app-mongo.py`)
- [ ] ✅ Criou `.env.example` com template sem credenciais
- [ ] ✅ Criou `.gitignore` que bloqueia `.env`
- [ ] ✅ Não há `.env` versionado no Git (`git status` deve mostrar vazio)
- [ ] ✅ README.md documenta como configurar `.env`

## No GitHub

- [ ] ✅ Repositório privado ou público sem credenciais expostas
- [ ] ✅ Verificou commits anteriores (`git log --oneline`)
- [ ] ✅ Se expôs senha antes: regenere imediatamente no MongoDB Atlas

## Antes de Deploy no Render

- [ ] ✅ Criou Web Service conectado ao repositório
- [ ] ✅ Adicionou variáveis de ambiente no painel do Render:
  - `MONGO_URI`
  - `MONGO_DB`
  - `MONGO_COLLECTION`
- [ ] ✅ Build Command: `pip install -r requirements.txt`
- [ ] ✅ Start Command: `gunicorn app-mongo:app`
- [ ] ✅ `Procfile` existe e está correto

## Após Deploy

- [ ] ✅ Acesse a URL pública e teste captura
- [ ] ✅ Verifique logs do Render (`Logs` no dashboard)
- [ ] ✅ Confirme que dados estão sendo salvos no MongoDB
- [ ] ✅ HTTPS está ativo (Render faz automaticamente)

## Segurança MongoDB Atlas

- [ ] ✅ IP Whitelist configurado (opcional mas recomendado)
  - Adicione `0.0.0.0/0` para aceitar qualquer IP (menos seguro)
  - Ou adicione IP específico do Render
- [ ] ✅ Usuário MongoDB com permissões mínimas (apenas da coleção usada)

## Monitoramento Contínuo

- [ ] ✅ Monitore uso da API (Render mostra no dashboard)
- [ ] ✅ Verifique regularmente logs por erros
- [ ] ✅ Alertas no MongoDB Atlas se uso estranho
