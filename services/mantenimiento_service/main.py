from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List
import asyncpg
import os
from datetime import date

app = FastAPI(title="Mantenimiento Service", version="1.0.0")
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

class MantenimientoCreate(BaseModel):
    equipo_id: int
    tipo: str # preventivo, correctivo
    fecha_programada: date
    descripcion: Optional[str] = None
    prioridad: str = "media"

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "mantenimiento"}

@app.get("/mantenimientos")
async def get_mantenimientos():
    query = """
        SELECT m.*, e.nombre as equipo_nombre, e.codigo_inventario
        FROM mantenimientos m
        LEFT JOIN equipos e ON m.equipo_id = e.id
        ORDER BY m.fecha_programada DESC
    """
    async with pool.acquire() as conn:
        rows = await conn.fetch(query)
        return [dict(row) for row in rows]

@app.post("/mantenimientos")
async def create_mantenimiento(mant: MantenimientoCreate):
    query = """
        INSERT INTO mantenimientos (equipo_id, tipo, fecha_programada, descripcion, estado, prioridad)
        VALUES ($1, $2, $3, $4, 'programado', $5)
        RETURNING id
    """
    async with pool.acquire() as conn:
        try:
            mant_id = await conn.fetchval(
                query, 
                mant.equipo_id, mant.tipo, mant.fecha_programada, 
                mant.descripcion, mant.prioridad
            )
            return {"id": mant_id, "message": "Mantenimiento programado"}
        except asyncpg.ForeignKeyViolationError:
            raise HTTPException(status_code=400, detail="Equipo no existe")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)