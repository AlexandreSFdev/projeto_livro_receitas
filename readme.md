# 🍳 Guia Completo - Livro de Receitas Django

## 📋 Resumo das Funcionalidades

### ✅ Já Implementado:
1. **Sistema de Receitas** - CRUD completo
2. **Ingredientes com dados nutricionais** - Calorias, proteínas, etc.
3. **Sistema de Autenticação** - Login, logout, registro
4. **Busca e Filtros Avançados** - Por texto, dificuldade, tempo
5. **Avaliações com Estrelas** - Sistema de notas e comentários
6. **Favoritos** - Salvar receitas favoritas
7. **Categorias** - Organizar receitas por tipo
8. **Comentários** - Interação entre usuários
9. **Contador de Visualizações** - Rastrear popularidade
10. **Compartilhamento** - WhatsApp e copiar link
11. **Upload de Fotos** - Imagens das receitas
12. **Design Responsivo** - Mobile, tablet, desktop

---

## 🚀 Passo a Passo para Setup Completo

### 1️⃣ Criar Ambiente Virtual e Instalar Dependências

```bash
# Criar pasta do projeto
mkdir livro_receitas_projeto
cd livro_receitas_projeto

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente (Linux/Mac)
source venv/bin/activate

# Ativar ambiente (Windows)
venv\Scripts\activate

# Instalar pacotes
pip install django pillow requests
```

### 2️⃣ Criar Projeto Django

```bash
# Criar projeto
django-admin startproject livro_receitas
cd livro_receitas

# Criar app
python manage.py startapp receitas
```

### 3️⃣ Configurar Settings

Editar `livro_receitas/settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'receitas',  # ← ADICIONAR
]

# No final do arquivo:
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
```

### 4️⃣ Configurar URLs Principais

Editar `livro_receitas/urls.py`:

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('receitas.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### 5️⃣ Criar Estrutura de Pastas no App

```bash
cd receitas

# Criar pastas para templates
mkdir -p templates/receitas

# Criar pastas para comandos de gerenciamento
mkdir -p management/commands

# Criar arquivos __init__.py
touch management/__init__.py
touch management/commands/__init__.py
```

### 6️⃣ Criar Arquivos do App

Criar/editar os seguintes arquivos na pasta `receitas/`:

- ✅ `models.py` - Copiar do artefato de funcionalidades extras
- ✅ `views.py` - Copiar do artefato de funcionalidades extras
- ✅ `forms.py` - Copiar do artefato de formulários melhorado
- ✅ `urls.py` - Copiar do artefato de rotas
- ✅ `admin.py` - Copiar do artefato de admin

### 7️⃣ Criar Templates

Criar os seguintes arquivos em `receitas/templates/receitas/`:

- ✅ `base.html`
- ✅ `lista.html`
- ✅ `detalhe.html`
- ✅ `form.html`
- ✅ `login.html`
- ✅ `registro.html`
- ✅ `minhas_receitas.html`
- ✅ `favoritas.html`
- ✅ `categorias.html`
- ✅ `por_categoria.html`

### 8️⃣ Criar Comandos de Gerenciamento

**Arquivo**: `receitas/management/commands/popular_ingredientes.py`
- Copiar do artefato "Cadastrar Ingredientes"

**Arquivo**: `receitas/management/commands/popular_categorias.py`
- Copiar do artefato "Funcionalidades Extras"

### 9️⃣ Rodar Migrações

```bash
# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Se der erro, tentar:
python manage.py makemigrations receitas
python manage.py migrate receitas
```

### 🔟 Criar Superusuário

```bash
python manage.py createsuperuser
# Digite: username, email, senha
```

### 1️⃣1️⃣ Popular Banco de Dados

```bash
# Popular ingredientes
python manage.py popular_ingredientes

# Popular categorias
python manage.py popular_categorias
```

### 1️⃣2️⃣ Rodar o Servidor

```bash
python manage.py runserver
```

Acesse: `http://127.0.0.1:8000/`

---

## 🔧 Resolver Problema dos Ingredientes Vazios

### Método 1: Via Admin (Mais Fácil)
1. Acesse `http://127.0.0.1:8000/admin/`
2. Faça login
3. Clique em "Ingredientes"
4. Adicione ingredientes manualmente

### Método 2: Via Comando (Recomendado)
```bash
python manage.py popular_ingredientes
```

### Método 3: Via Shell Django
```bash
python manage.py shell
```

```python
from receitas.models import Ingrediente

Ingrediente.objects.create(
    nome='Arroz',
    calorias_por_100g=130,
    proteinas_por_100g=2.7,
    carboidratos_por_100g=28,
    gorduras_por_100g=0.3
)
```

---

## 📊 Estrutura Final do Projeto

```
projeto_livro_receitas/
├── venv/
├── livro_receitas/
│   ├── settings.py
│   ├── urls.py
│   └── ...
├── manage.py
├── db.sqlite3
├── media/
├── receitas/
│    ├── models.py
│    ├── views.py
│    ├── forms.py
│    ├── urls.py
│    ├── admin.py
│    ├── management/
│    │   ├── __init__.py
│    │   └── commands/
│    │       ├── __init__.py
│    │       ├── popular_ingredientes.py
│    │       └── popular_categorias.py
│    └── templates/
│        └── receitas/
│            ├── base.html
│            ├── lista.html
│            ├── detalhe.html
│            ├── form.html
│            ├── login.html
│            ├── registro.html
│            ├── minhas_receitas.html
│            ├── favoritas.html
│            ├── populares.html
│            ├── categorias.html
│            └── por_categoria.html
└──requirements.txt
```

---

## 🎯 Checklist de Funcionalidades

### Core
- ✅ Cadastro de receitas
- ✅ Upload de fotos
- ✅ Ingredientes com dados nutricionais
- ✅ Cálculo automático de calorias
- ✅ Modo de preparo
- ✅ Tempo e dificuldade

### Usuários
- ✅ Login/Logout
- ✅ Registro
- ✅ Minhas Receitas
- ✅ Favoritos
- ✅ Avaliações
- ✅ Comentários

### Busca e Filtros
- ✅ Busca por texto
- ✅ Filtro por dificuldade
- ✅ Filtro por tempo
- ✅ Ordenação (recentes, populares, etc)
- ✅ Filtro por categoria

### Social
- ✅ Sistema de avaliação (estrelas)
- ✅ Comentários
- ✅ Contador de visualizações
- ✅ Favoritos/Curtidas
- ✅ Compartilhamento (WhatsApp, copiar link)

### Organização
- ✅ Categorias
- ✅ Tags
- ✅ Receitas populares
- ✅ Minhas receitas
- ✅ Favoritas

---

## 🐛 Problemas Comuns e Soluções

### Problema: Lista de ingredientes vazia
**Solução**: Rodar `python manage.py popular_ingredientes`

### Problema: Erro ao fazer upload de imagem
**Solução**: Instalar Pillow: `pip install pillow`

### Problema: Erro 404 nas imagens
**Solução**: Adicionar no `urls.py` principal:
```python
from django.conf.urls.static import static
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### Problema: Migrations não funcionam
**Solução**: 
```bash
python manage.py migrate --run-syncdb
# ou
python manage.py makemigrations --empty receitas
```

---

## 📱 Funcionalidades Extras Possíveis

### Já implementado:
- ✅ Favoritos
- ✅ Categorias
- ✅ Comentários
- ✅ Compartilhamento
- ✅ Contador de visualizações

### Próximas melhorias possíveis:
- 📸 Galeria múltipla de fotos
- 🔔 Sistema de notificações
- 👥 Seguir outros usuários
- 📊 Painel de estatísticas
- 🖨️ Imprimir receita
- 📧 Enviar por email
- 🌐 API REST
- 📱 PWA (Progressive Web App)

---

## 🔐 Segurança

Lembre-se de:
1. Mudar `SECRET_KEY` em produção
2. Definir `DEBUG = False` em produção
3. Configurar `ALLOWED_HOSTS`
4. Usar banco de dados PostgreSQL em produção
5. Configurar HTTPS

---

## 📝 Comandos Úteis

```bash
# Criar superusuário
python manage.py createsuperuser

# Rodar servidor
python manage.py runserver

# Popular ingredientes
python manage.py popular_ingredientes

# Popular categorias
python manage.py popular_categorias

# Shell interativo
python manage.py shell

# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Coletar arquivos estáticos
python manage.py collectstatic
```

---

## 🎉 Pronto!

Agora você tem um sistema completo de receitas com:
- Busca avançada
- Categorias
- Favoritos
- Avaliações
- Comentários
- Compartilhamento
- E muito mais!

Bom desenvolvimento! 🚀
