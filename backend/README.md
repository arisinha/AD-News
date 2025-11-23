# API de Noticias AD 📰

Una API de agregación y personalización de noticias basada en FastAPI con MongoDB y Redis.

## 🚀 Inicio Rápido

### Opción 1: Usando el Script de Inicio (Recomendado)

```bash
./start.sh
```

Esto hará lo siguiente:
- Creará un entorno virtual
- Instalará las dependencias
- Iniciará el servidor en http://localhost:8000

### Opción 2: Configuración Manual

```bash
# Crear y activar el entorno virtual
python3 -m venv venv
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Configurar variables de entorno
cp .env.example .env
# Edita .env con tus credenciales

# Iniciar el servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## 📋 Requisitos Previos

Antes de comenzar, necesitas:

1.  **Cuenta de MongoDB Atlas** (el nivel gratuito funciona)
    -   Obtén la cadena de conexión de https://www.mongodb.com/cloud/atlas
    -   Agrégala a `.env` como `MONGODB_URL`

2.  **Clave de API de NewsAPI** (nivel gratuito: 100 solicitudes/día)
    -   Obténla de https://newsapi.org/
    -   Agrégala a `.env` como `NEWS_API_KEY`

3.  **Clave de API de OpenAI** (opcional, para funciones de IA)
    -   Obténla de https://platform.openai.com/
    -   Agrégala a `.env` como `OPENAI_API_KEY`

4.  **Redis** (opcional, para caché)
    -   Instálalo localmente: `brew install redis && brew services start redis`
    -   O sáltatelo, la API funcionará sin Redis

## 🧪 Pruebas

### Pruebas Automatizadas

```bash
./test_api.sh
```

### Pruebas Manuales

1.  **Verificación de Salud (Health Check)**
    ```bash
    curl http://localhost:8000/health
    ```

2.  **Documentación Interactiva**
    -   Swagger UI: http://localhost:8000/docs
    -   ReDoc: http://localhost:8000/redoc

3.  **Registrar un Usuario**
    ```bash
    curl -X POST "http://localhost:8000/v1/auth/register" \
      -H "Content-Type: application/json" \
      -d '{
        "email": "usuario@ejemplo.com",
        "password": "password123",
        "full_name": "Juan Pérez"
      }'
    ```

4.  **Iniciar Sesión**
    ```bash
    curl -X POST "http://localhost:8000/v1/auth/login" \
      -H "Content-Type: application/json" \
      -d '{
        "email": "usuario@ejemplo.com",
        "password": "password123"
      }'
    ```

## 📁 Estructura del Proyecto

```
backend/
├── app/
│   ├── api/v1/endpoints/    # Manejadores de rutas de la API
│   ├── core/                # Configuración
│   ├── crud/                # Operaciones de base de datos
│   ├── db/                  # Conexiones a la base de datos
│   ├── middleware/          # Middleware personalizado
│   ├── models/              # Modelos de base de datos
│   ├── schemas/             # Esquemas Pydantic
│   ├── services/            # Lógica de negocio
│   └── utils/               # Utilidades
├── tests/                   # Archivos de prueba
├── .env                     # Variables de entorno (no en git)
├── .env.example            # Archivo .env de ejemplo
├── requirements.txt         # Dependencias de Python
├── start.sh                # Script de inicio rápido
└── test_api.sh             # Script de prueba de la API
```

## 🔧 Configuración

Edita el archivo `.env` con tus credenciales:

```env
# Requerido
MONGODB_URL=mongodb+srv://usuario:contraseña@cluster.mongodb.net/
NEWS_API_KEY=tu-clave-newsapi

# Opcional
OPENAI_API_KEY=tu-clave-openai
REDIS_URL=redis://localhost:6379
SECRET_KEY=tu-clave-secreta
```

## 📊 Puntos de Acceso de la API (Endpoints)

### Autenticación
- `POST /v1/auth/register` - Registrar nuevo usuario
- `POST /v1/auth/login` - Iniciar sesión de usuario

### Usuarios
- `GET /v1/user/me` - Obtener usuario actual
- `PUT /v1/user/preferences` - Actualizar preferencias

### Artículos
- `GET /v1/articles` - Listar artículos
- `GET /v1/articles/{id}` - Obtener detalles del artículo

### Feed
- `GET /v1/feed` - Obtener feed de noticias personalizado

### Temas
- `GET /v1/topics` - Listar temas
- `GET /v1/topics/{id}` - Obtener detalles del tema

### Búsqueda
- `GET /v1/search` - Buscar artículos

### Favoritos
- `GET /v1/user/favorites` - Obtener favoritos del usuario
- `POST /v1/user/favorites` - Añadir a favoritos
- `DELETE /v1/user/favorites/{id}` - Eliminar de favoritos

## 🐛 Solución de Problemas

### "ModuleNotFoundError"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "MongoDB connection failed" (Fallo de conexión a MongoDB)
- Verifica `MONGODB_URL` en `.env`
- Verifica la lista blanca de IP en MongoDB Atlas
- Prueba las credenciales

### "Redis connection error" (Error de conexión a Redis)
- Redis es opcional, la API continuará sin él
- Para usar Redis: `brew install redis && brew services start redis`

### "NEWS_API_KEY not found" (NEWS_API_KEY no encontrada)
- Obtén una clave gratuita de https://newsapi.org/
- Agrégala al archivo `.env`

## 📚 Documentación

-   **Guía de Configuración**: Consulta `SETUP_GUIDE.md` para instrucciones detalladas
-   **Documentación de la API**: http://localhost:8000/docs (cuando esté en ejecución)
-   **Documentación Alternativa**: http://localhost:8000/redoc

## 🎯 Próximos Pasos

1.  ✅ Configura `.env` con tus credenciales
2.  ✅ Ejecuta `./start.sh` para iniciar el servidor
3.  ✅ Prueba con `./test_api.sh` o visita `/docs`
4.  🔄 Implementa características adicionales
5.  🔄 Escribe pruebas unitarias
6.  🔄 Despliega a producción

## 📝 Licencia

Este proyecto es para fines educativos.
