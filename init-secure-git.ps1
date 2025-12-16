# Script para inicializar repositório Git com segurança (Windows PowerShell)

Write-Host "🔐 Inicializando repositório Git com segurança..." -ForegroundColor Cyan

# Criar arquivo .env local (não será versionado)
if (-not (Test-Path ".env")) {
    Write-Host "📝 Criando .env com template de variáveis..." -ForegroundColor Yellow
    Copy-Item ".env.example" ".env"
    Write-Host "⚠️  EDITE .env COM SUAS CREDENCIAIS REAIS!" -ForegroundColor Red
}

# Inicializar git
git init
git add -A
# Remover .env se foi adicionado acidentalmente
git rm --cached .env -q 2>&1 | Out-Null

# Committar
git commit -m "Initial commit - Georeferenciamento MongoDB"

Write-Host ""
Write-Host "✅ Repositório inicializado!" -ForegroundColor Green
Write-Host ""
Write-Host "📋 Próximos passos:" -ForegroundColor Cyan
Write-Host "1. Edite .env com suas credenciais reais:"
Write-Host "   notepad .env" -ForegroundColor Yellow
Write-Host ""
Write-Host "2. Crie repositório vazio no GitHub (https://github.com/new)"
Write-Host ""
Write-Host "3. Adicione remote:"
Write-Host "   git remote add origin https://github.com/seu-usuario/seu-repo.git" -ForegroundColor Yellow
Write-Host ""
Write-Host "4. Faça push:"
Write-Host "   git branch -M main" -ForegroundColor Yellow
Write-Host "   git push -u origin main" -ForegroundColor Yellow
Write-Host ""
Write-Host "⚠️  NUNCA commite o arquivo .env!" -ForegroundColor Red
