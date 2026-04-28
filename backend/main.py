from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from risco import router, calcular_risco, calcular_hora
from pydantic import BaseModel
from datetime import datetime
from math import radians, cos, sin, sqrt, atan2
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)

# ----------------------
# MODELO
# ----------------------
class Ocorrencia(BaseModel):
    tipo: str
    lat: float
    lon: float
    descricao: str
    cidade: str


# ----------------------
# MEMÓRIA (SEM BANCO)
# ----------------------
ocorrencias = []


# ----------------------
# HOME
# ----------------------
@app.get("/")
def home():
    return {"message": "API de Segurança rodando!"}


# ----------------------
# POST OCORRÊNCIA (SEM QUEBRAR MAIS)
# ----------------------
def pegar_endereco(lat, lon):
    try:
        headers = {
            "User-Agent": "UrbanSenseApp/1.0"
        }

        res = requests.get(
            f"https://nominatim.openstreetmap.org/reverse?lat={lat}&lon={lon}&format=json",
            headers=headers,
            timeout=3
        )

        if res.status_code != 200:
            return "Rua desconhecida", "Bairro desconhecido"

        data = res.json()

        rua = (
            data.get("address", {}).get("road") or
            data.get("address", {}).get("pedestrian") or
            data.get("address", {}).get("residential") or
            "Rua desconhecida"
        )

        bairro = (
            data.get("address", {}).get("suburb") or
            data.get("address", {}).get("neighbourhood") or
            data.get("address", {}).get("city_district") or
            "Bairro desconhecido"
        )

        return rua, bairro

    except:
        return "Rua desconhecida", "Bairro desconhecido"


@app.post("/ocorrencia")
def criar_ocorrencia(ocorrencia: Ocorrencia):

    # NÃO deixa o backend quebrar mais
    rua, bairro = pegar_endereco(ocorrencia.lat, ocorrencia.lon)

    nova = {
        "tipo": ocorrencia.tipo,
        "lat": ocorrencia.lat,
        "lon": ocorrencia.lon,
        "hora": datetime.now().isoformat(),
        "descricao": ocorrencia.descricao,
        "cidade": ocorrencia.cidade,
        "rua": rua,
        "bairro": bairro
    }

    ocorrencias.append(nova)

    return {
        "message": "Ocorrência registrada com sucesso!",
        "ocorrencia": nova
    }


# ----------------------
# LISTAGEM POR CIDADE
# ----------------------
@app.get("/ocorrencias")
def listar_ocorrencias(cidade: str = None):
    if cidade:
        return [o for o in ocorrencias if o["cidade"].lower() == cidade.lower()]
    return ocorrencias


# ----------------------
# DISTÂNCIA (HAVERSINE)
# ----------------------
def distancia(lat1, lon1, lat2, lon2):
    R = 6371.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


# ----------------------
# OCORRÊNCIAS PRÓXIMAS
# ----------------------
@app.get("/ocorrencias-proximas")
def ocorrencias_proximas(lat: float, lon: float, raio: float = 50):
    proximas = []

    for o in ocorrencias:
        d = distancia(lat, lon, o["lat"], o["lon"])
        if d <= raio:
            o_copy = o.copy()
            o_copy["distancia"] = round(d, 2)
            proximas.append(o_copy)

    return proximas


# ----------------------
# DADOS DO MAPA
# ----------------------
@app.get("/dados-mapa")
def dados_mapa(lat: float, lon: float, raio: float = 100):

    proximas = []

    for o in ocorrencias:
        d = distancia(lat, lon, o["lat"], o["lon"])
        if d <= raio:
            proximas.append({
                **o,
                "distancia": round(d, 2),
            })

    risco = calcular_risco(proximas)

    return {
        "usuario": {
            "lat": lat,
            "lon": lon
        },
        "total_ocorrencias": len(ocorrencias),
        "ocorrencias_proximas": proximas,
        "resumo": {
            "proximas": len(proximas),
        },
        "risco": risco
    }


# ----------------------
# HORA
# ----------------------
@app.get("/hora")
def pegar_hora():
    return {"hora": datetime.now().hour}