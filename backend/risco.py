from fastapi import APIRouter
from datetime import datetime
router = APIRouter()

def calcular_hora(hora=None):
    if hora is None:
        hora = datetime.now().hour
    return hora

def parse_hora(hora_str):
    try:
        return datetime.fromisoformat(hora_str)
    except:
        return None

def calcular_risco(ocorrencias_proximas):
    risco = 0
    agora = datetime.now()
    hora_atual = calcular_hora()
   
    #quantidade de ocorrências próximas
    qtd = len(ocorrencias_proximas)
    if qtd <= 3:
        risco += 2
    elif qtd <= 6:
        risco += 4
    else:
        risco += 6

    #Frequência das ocorrências (últimos 2 dias)
    recentes = 0
    ultimas_48h = 0
    anteriores = 0

    for o in ocorrencias_proximas:
        hora_ocorrencia = parse_hora(o['hora'])
        if not hora_ocorrencia:
            continue
        diff = (agora-hora_ocorrencia).total_seconds() / 3600
        if diff <= 48:
            recentes += 1
            ultimas_48h += 1
        else:
            anteriores += 1
    risco += recentes * 1

    #Tendencia
    if ultimas_48h > anteriores:
        risco += 3
    elif ultimas_48h < anteriores:
        risco -= 1

    #Hora atual
    if 23 <= hora_atual or hora_atual < 6:
        risco += 5
    elif 18 <= hora_atual < 23:
        risco += 3
    elif 12 <= hora_atual < 18:
        risco += 1
    else:
        risco += 0

    #Nivel de risco
    if risco < 5:
        nivel = "Baixo"
    elif risco < 14:
        nivel = "Médio"
    else:
        nivel = "Alto"
    
    return {
        "risco": risco,
        "nivel": nivel
    }