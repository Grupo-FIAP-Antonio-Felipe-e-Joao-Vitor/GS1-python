import requests

def converterCEP(local):
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
    print("=" * 65)
    print("🌧️  Bem-vindo ao Sistema de Previsão de Enchentes do Brasil!  🌊")
    print("-" * 65)

def mostrarMenu ():
    print("[1] Procurar risco por CEP")
    print("[2] Procurar risco por Cidade")

def menu ():
    escolha = int(input("Deseja especificar a localização como: "))
    while True:
        if escolha == 1:
            localizacao = input("Insira o CEP: ")
            return localizacao
        elif escolha == 2:
            localizacao = input("Insira a cidade com o nome completo (ex: São Paulo, Minas Gerais): ")
            return localizacao
        else:
            print("Digite uma opção válida.")
            escolha = int(input("Deseja especificar a localização como: "))

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

    for dia, mm in zip(dias, precipitacoes):
        print(f"{dia}: {mm} mm")





mostrarBoasVindas()
mostrarMenu()
local = menu()
converterCEP()
coord = converterCEP()
precipitacao(coord[0], coord[1])