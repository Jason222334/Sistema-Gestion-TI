from fastapi import FastAPI, Request, HTTPException
import httpx
import os
import uvicorn

app = FastAPI(title="API Gateway")

# Configuración de URLs de microservicios desde variables de entorno
# Los valores por defecto son para ejecución local, en Docker se sobrescriben con el nombre del servicio
SERVICES = {
    "equipos": os.getenv("EQUIPOS_URL", "http://localhost:8001"),
    "proveedores": os.getenv("PROVEEDORES_URL", "http://localhost:8002"),
    "mantenimientos": os.getenv("MANTENIMIENTO_URL", "http://localhost:8003"),
    "reportes": os.getenv("REPORTES_URL", "http://localhost:8004"),
    "agents": os.getenv("AGENTS_URL", "http://localhost:8005"),
}

client = httpx.AsyncClient()

async def forward_request(service_name: str, path: str, request: Request):
    base_url = SERVICES.get(service_name)
    if not base_url:
        raise HTTPException(status_code=404, detail="Service not found")
    
    # Construcción de la URL destino
    url = f"{base_url}/{path}"
    if request.query_params:
        url += f"?{request.query_params}"

    try:
        # Reenvía el request al microservicio correspondiente
        response = await client.request(
            method=request.method,
            url=url,
            headers=request.headers,
            content=await request.body(),
            timeout=30.0
        )
        # Retorna el JSON directamente
        return response.json()
    except httpx.ConnectError:
        raise HTTPException(status_code=503, detail=f"No se pudo conectar con el servicio {service_name}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno en Gateway: {str(e)}")

# --- PROXIES GENÉRICOS (Capturan cualquier sub-ruta) ---

@app.api_route("/api/equipos/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def equipos_proxy(path: str, request: Request):
    return await forward_request("equipos", f"equipos/{path}" if path else "equipos", request)

@app.api_route("/api/proveedores/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proveedores_proxy(path: str, request: Request):
    return await forward_request("proveedores", f"proveedores/{path}" if path else "proveedores", request)

@app.api_route("/api/mantenimientos/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def mantenimientos_proxy(path: str, request: Request):
    return await forward_request("mantenimientos", f"mantenimientos/{path}" if path else "mantenimientos", request)

# --- RUTAS ESPECÍFICAS / ALIAS (Para asegurar compatibilidad con el frontend) ---

# Mantenimientos (Raíz)
@app.get("/api/mantenimientos")
async def get_mantenimientos_list(request: Request):
    return await forward_request("mantenimientos", "mantenimientos", request)

@app.post("/api/mantenimientos")
async def create_mantenimiento_proxy(request: Request):
    return await forward_request("mantenimientos", "mantenimientos", request)

# Equipos y Auxiliares
@app.get("/api/equipos")
async def get_equipos(request: Request):
    return await forward_request("equipos", "equipos", request)
    
@app.get("/api/categorias")
async def get_categorias(request: Request):
    return await forward_request("equipos", "categorias", request)

@app.get("/api/ubicaciones")
async def get_ubicaciones(request: Request):
    return await forward_request("equipos", "ubicaciones", request)

# Proveedores (Raíz)
@app.get("/api/proveedores")
async def get_proveedores(request: Request):
    return await forward_request("proveedores", "proveedores", request)

# Reportes y Agentes    
@app.get("/api/reportes/dashboard")
async def get_dashboard(request: Request):
    return await forward_request("reportes", "dashboard", request)

@app.post("/api/agents/run-all-agents")
async def run_agents(request: Request):
    return await forward_request("agents", "run-all-agents", request)

@app.get("/api/agents/notificaciones")
async def get_notif(request: Request):
    return await forward_request("agents", "notificaciones", request)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)