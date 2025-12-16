#!/bin/bash
# Script para inicializar repositório Git com segurança

echo "🔐 Inicializando repositório Git com segurança..."

# Criar arquivo .env local (não será versionado)
if [ ! -f .env ]; then
    echo "📝 Criando .env com template de variáveis..."
    cp .env.example .env
    echo "⚠️  EDITE .env COM SUAS CREDENCIAIS REAIS!"
fi

# Inicializar git
git init
git add -A
# Remover .env se foi adicionado acidentalmente
git rm --cached .env 2>/dev/null || true

# Committar
git commit -m "Initial commit - Georeferenciamento MongoDB"

echo ""
echo "✅ Repositório inicializado!"
echo ""
echo "📋 Próximos passos:"
echo "1. Edite .env com suas credenciais reais:"
echo "   nano .env"
echo ""
echo "2. Crie repositório vazio no GitHub (https://github.com/new)"
echo ""
echo "3. Adicione remote:"
echo "   git remote add origin https://github.com/seu-usuario/seu-repo.git"
echo ""
echo "4. Faça push:"
echo "   git branch -M main"
echo "   git push -u origin main"
echo ""
echo "⚠️  NUNCA commite o arquivo .env!"
