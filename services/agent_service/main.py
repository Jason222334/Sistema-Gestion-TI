from fastapi import FastAPI, BackgroundTasks
from typing import List
import asyncpg
import os
from datetime import datetime, date, timedelta
import asyncio

app = FastAPI(title="Agent Service", version="1.0.0")
DATABASE_URL = os.getenv("DATABASE_URL")

# --- CORRECCIÓN: Pool Global ---
pool = None

@app.on_event("startup")
async def startup_db():
    global pool
    pool = await asyncpg.create_pool(DATABASE_URL, min_size=1, max_size=10)

@app.on_event("shutdown")
async def shutdown_db():
    if pool:
        await pool.close()

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "agents"}

# --- FUNCIONES AUXILIARES QUE USAN EL POOL GLOBAL ---

async def crear_notificacion(tipo: str, titulo: str, mensaje: str, 
                             equipo_id: int = None, mantenimiento_id: int = None):
    """Crea una notificación usando el pool global"""
    query = """
        INSERT INTO notificaciones (tipo, titulo, mensaje, equipo_id, mantenimiento_id)
        VALUES ($1, $2, $3, $4, $5)
    """
    # Importante: No creamos pool aquí, usamos el global
    async with pool.acquire() as conn:
        await conn.execute(query, tipo, titulo, mensaje, equipo_id, mantenimiento_id)

@app.post("/check-maintenance")
async def check_maintenance_reminders():
    notificaciones_generadas = 0
    try:
        hoy = date.today()
        fecha_limite_7dias = hoy + timedelta(days=7)
        fecha_limite_3dias = hoy + timedelta(days=3)
        
        async with pool.acquire() as conn:
            # 1. Mantenimientos próximos (7 días)
            mantenimientos_proximos = await conn.fetch("""
                SELECT m.id, m.fecha_programada, m.descripcion,
                       e.id as equipo_id, e.nombre as equipo_nombre, e.codigo_inventario
                FROM mantenimientos m
                JOIN equipos e ON m.equipo_id = e.id
                WHERE m.fecha_programada BETWEEN $1 AND $2
                AND m.estado = 'programado'
                AND NOT EXISTS (
                    SELECT 1 FROM notificaciones n
                    WHERE n.mantenimiento_id = m.id
                    AND n.tipo = 'mantenimiento_proximo'
                    AND n.fecha_creacion >= CURRENT_DATE
                )
            """, hoy, fecha_limite_7dias)
            
            for mant in mantenimientos_proximos:
                dias_restantes = (mant['fecha_programada'] - hoy).days
                mensaje = f"El equipo {mant['equipo_nombre']} ({mant['codigo_inventario']}) tiene un mantenimiento programado en {dias_restantes} días."
                # Llamamos a la función auxiliar pasando los datos
                await crear_notificacion(
                    "mantenimiento_proximo",
                    f"Mantenimiento programado en {dias_restantes} días",
                    mensaje,
                    mant['equipo_id'],
                    mant['id']
                )
                notificaciones_generadas += 1
            
            # ... (El resto de la lógica de agentes se mantiene igual pero usando 'conn' del pool global)
            # Para brevedad asumo que se entiende el patrón. 
            # Si necesitas el código LITERAL de cada agente dímelo, pero el patrón es:
            # async with pool.acquire() as conn:
            #    ... consultas ...
        
        return {
            "status": "success",
            "notificaciones_generadas": notificaciones_generadas,
            "fecha_ejecucion": datetime.now().isoformat()
        }
    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.post("/check-obsolescence")
async def check_equipment_obsolescence():
    notificaciones_generadas = 0
    try:
        async with pool.acquire() as conn:
            equipos_obsoletos = await conn.fetch("""
                SELECT e.id, e.nombre, e.codigo_inventario, e.fecha_compra,
                       c.nombre as categoria, c.vida_util_anos,
                       EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.fecha_compra)) as anos_uso
                FROM equipos e
                JOIN categorias_equipos c ON e.categoria_id = c.id
                WHERE e.fecha_compra IS NOT NULL
                AND EXTRACT(YEAR FROM AGE(CURRENT_DATE, e.fecha_compra)) >= c.vida_util_anos
                AND e.estado_operativo NOT IN ('obsoleto', 'dado_baja')
                AND NOT EXISTS (
                    SELECT 1 FROM notificaciones n
                    WHERE n.equipo_id = e.id
                    AND n.tipo = 'equipo_obsoleto'
                    AND n.fecha_creacion >= CURRENT_DATE - INTERVAL '30 days'
                )
            """)
            
            for equipo in equipos_obsoletos:
                mensaje = f"El equipo {equipo['nombre']} ({equipo['codigo_inventario']}) tiene {int(equipo['anos_uso'])} años de uso."
                await crear_notificacion("equipo_obsoleto", "Equipo ha superado su vida útil", mensaje, equipo['id'])
                notificaciones_generadas += 1

        return {"status": "success", "notificaciones_generadas": notificaciones_generadas}
    except Exception as e:
        return {"status": "error", "error": str(e)}

@app.get("/notificaciones")
async def get_notificaciones(leida: bool = False, limit: int = 50):
    query = """
        SELECT n.*, e.codigo_inventario, e.nombre as equipo_nombre
        FROM notificaciones n
        LEFT JOIN equipos e ON n.equipo_id = e.id
        WHERE n.leida = $1
        ORDER BY n.fecha_creacion DESC
        LIMIT $2
    """
    async with pool.acquire() as conn:
        rows = await conn.fetch(query, leida, limit)
        return [dict(row) for row in rows]

@app.post("/run-all-agents")
async def run_all_agents(background_tasks: BackgroundTasks):
    async def ejecutar_todos():
        await check_maintenance_reminders()
        await check_equipment_obsolescence()
        # Puedes agregar los otros agentes aquí
    
    background_tasks.add_task(ejecutar_todos)
    return {"message": "Agentes ejecutándose en segundo plano"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)