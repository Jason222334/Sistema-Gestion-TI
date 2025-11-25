# Sistema de Gestión de Equipos de TI - Universidad

Sistema integral para la gestión de equipos de tecnología en universidades públicas, implementado con una arquitectura de microservicios moderna y escalable. Este proyecto permite administrar el ciclo de vida completo de los activos de TI, desde la compra hasta la baja, incluyendo gestión de proveedores, mantenimientos y reportes avanzados.

🏗️ Arquitectura

El sistema está construido sobre una arquitectura de microservicios contenerizados:

# Microservicios

API Gateway (Puerto 8000): Punto de entrada único y enrutador de peticiones.

Equipos Service (Puerto 8001): Gestión de inventario, ubicaciones y movimientos.

Proveedores Service (Puerto 8002): Gestión de proveedores y contratos.

Mantenimiento Service (Puerto 8003): Programación y control de mantenimientos.

Reportes Service (Puerto 8004): Dashboard, análisis de datos y exportación (PDF/Excel).

Agent Service (Puerto 8005): Agentes inteligentes para automatización y alertas en segundo plano.

Frontend Streamlit (Puerto 8501): Interfaz de usuario interactiva.

PostgreSQL (Puerto 5432): Base de datos centralizada.

# 🚀 Instalación y Despliegue

Prerrequisitos

Docker Engine 20.10+

Docker Compose 2.0+

Git

Pasos de Instalación

Clonar el repositorio

git clone [https://github.com/TU_USUARIO/sistema-gestion-ti.git](https://github.com/TU_USUARIO/sistema-gestion-ti.git)
cd sistema-gestion-ti


Configurar variables de entorno
El archivo .env ya viene preconfigurado para el entorno Docker local. Asegúrate de que exista:

Si no existe, crea uno nuevo con:
cp .env.example .env


Construir y levantar servicios

docker-compose up -d --build


Cargar datos de prueba (Seed Data)
Para que el dashboard no aparezca vacío, carga los datos semilla incluidos:

cat database/datos_semilla.sql | docker-compose exec -T postgres psql -U postgres -d ti_management


# Acceder a la aplicación

Frontend (Web App): http://localhost:8501

Documentación API (Swagger): http://localhost:8000/docs

📊 Estructura del Proyecto

sistema-gestion-ti/
├── frontend/                 # Interfaz de Usuario (Streamlit)
│   ├── pages/
│   │   ├── 1_📦_Equipos.py
│   │   ├── 2_🏢_Proveedores.py
│   │   ├── 3_🔧_Mantenimiento.py
│   │   └── 4_📊_Reportes.py
│   └── app.py
├── services/                 # Microservicios Backend (FastAPI)
│   ├── api_gateway/
│   ├── equipos_service/
│   ├── proveedores_service/
│   ├── mantenimiento_service/
│   ├── reportes_service/
│   └── agent_service/
├── database/                 # Scripts SQL
│   ├── schema.sql
│   └── datos_semilla.sql
├── docker-compose.yml        # Orquestación
└── README.md


# 🗄️ Modelo de Datos

El sistema utiliza PostgreSQL con las siguientes entidades principales:

proveedores: Registro de empresas proveedoras.

equipos: Inventario principal con especificaciones JSONB.

ubicaciones: Catálogo de edificios y oficinas.

movimientos_equipos: Trazabilidad de cambios de ubicación.

mantenimientos: Historial preventivo y correctivo.

contratos: Acuerdos legales y garantías.

notificaciones: Alertas generadas por los agentes inteligentes.

# 🔧 Funcionalidades

1. Gestión de Proveedores

✅ Registro, actualización y validación de RUC.

✅ Historial de compras y estadísticas.

✅ Gestión de contratos y vigencias.

2. Gestión de Equipos

✅ Inventario detallado con estados (Operativo, En Reparación, Obsoleto).

✅ Historial de asignaciones a usuarios.

✅ Trazabilidad de ubicaciones físicas.

✅ Categorización dinámica.

3. Gestión de Mantenimiento

✅ Programación de mantenimientos preventivos y correctivos.

✅ Calendario y priorización (Baja, Media, Alta, Urgente).

✅ Registro de costos y diagnósticos.

4. Reportes y Análisis

✅ Dashboard interactivo con KPIs en tiempo real.

✅ Gráficos estadísticos (Plotly) de distribución y costos.

✅ Exportación de reportes a PDF y Excel.

5. Agentes Inteligentes (Automatización)

🤖 Detector de Mantenimientos: Alerta sobre mantenimientos próximos (7 días).

📅 Monitor de Obsolescencia: Identifica equipos que superaron su vida útil.

⚠️ Monitor de Garantías: Notifica garantías por vencer (<60 días).

🛠️ Mantenimiento y Comandos Útiles

# Ver logs de un servicio:

docker-compose logs -f api-gateway


Reiniciar todos los servicios:

docker-compose restart


Detener el sistema:

docker-compose down


📝 Documentación API

Una vez levantado el sistema, la documentación interactiva (Swagger UI) está disponible en:

URL: http://localhost:8000/docs

👥 Contacto

Desarrollado por: [Galvez Luna Jason Anderson]
Curso: Desarrollo de Aplicaciones Distribuidas
Universidad: Universidad [UNT]

© 2025 Sistema de Gestión TI
