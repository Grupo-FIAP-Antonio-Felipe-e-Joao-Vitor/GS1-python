import requests
import os
import time

def limparTerminal ():
    os.system('cls' if os.name == 'nt' else 'clear')

def converterCEP (local):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": f"{local}, Brazil",
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "MeuAppExemplo/1.0 (meuemail@exemplo.com)"
    }

    resposta = requests.get(url, params=params, headers=headers)
    dados = resposta.json()

    if dados:
        lat = dados[0]['lat']
        lon = dados[0]['lon']
        return lat, lon
    else:
        return None

def mostrarBoasVindas ():
    print("=" * 45)
    print("🌧️ Sistema de Previsão de Enchentes no Brasil!  🌊")
    print("-" * 45)

def mostrarMenu ():
    print("[1] Procurar risco por CEP")
    print("[2] Procurar risco por Cidade")

def menu ():
    escolha = str(input("Deseja especificar a localização como: "))
    while True:
        if escolha == "1":
            limparTerminal()
            mostrarBoasVindas()
            print("Para voltar digite 'voltar'")
            localizacao = input("Insira o CEP: ").lower()
            if localizacao == "voltar":
                limparTerminal()
                mostrarBoasVindas()
                mostrarMenu()
                menu()
            else:
                return localizacao
        elif escolha == "2":
            limparTerminal()
            mostrarBoasVindas()
            print("Para voltar digite 'voltar'")
            localizacao = input("Insira a cidade com o nome completo (ex: São Paulo, Minas Gerais): ").lower()
            if localizacao == "voltar":
                limparTerminal()
                mostrarBoasVindas()
                mostrarMenu()
                menu()
            else:
                return localizacao
        else:
            print("Opção inválida.")
            time.sleep(2)
            limparTerminal()
            mostrarBoasVindas()
            mostrarMenu()
            menu()

def calcularRisco (mm):
    if mm > 80:
        return "Alerta grave"
    elif mm >= 50 and mm <= 80:
        return "Risco alto"
    elif mm < 50 and mm >= 20:
        return "Risco moderado"
    elif mm < 20:
        return "Risco baixo"

def precipitacao(lat, lon):

    # Parâmetros da requisição
    params = {
        "latitude": lat,
        "longitude": lon,
        "daily": "precipitation_sum",
        "timezone": "auto"
    }

    # Endpoint da API
    url = "https://api.open-meteo.com/v1/forecast"

    # Faz a requisição
    resposta = requests.get(url, params=params)
    dados = resposta.json()

    dias = dados['daily']['time']
    precipitacoes = dados['daily']['precipitation_sum']

    print("📅 Previsão de precipitação e risco de enchente 📅")
    for dia, mm in zip(dias, precipitacoes):
        risco = calcularRisco(mm)
        print(f"{dia}: {mm} mm → {risco}")




while True:
    limparTerminal()
    mostrarBoasVindas()
    mostrarMenu()
    local = menu()
    coord = converterCEP(local)

    if coord:
        precipitacao(coord[0], coord[1])
    else:
        print("❌ Localização inválida.")