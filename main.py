import requests # Importa a biblioteca 'requests' para fazer requisições HTTP (para APIs).
import os       # Importa a biblioteca 'os' para interagir com o sistema operacional (limpar terminal).
import time     # Importa a biblioteca 'time' para pausar a execução (usado para 'sleep').

def limparTerminal():
    # Define uma função para limpar o terminal/console.
    # 'os.system' executa um comando do sistema operacional.
    # 'cls' é o comando para limpar no Windows, 'clear' é para sistemas Unix/Linux/macOS.
    os.system('cls' if os.name == 'nt' else 'clear')

def converterCEP(local):
    # Define uma função para converter um nome de local (CEP ou cidade) em coordenadas geográficas (latitude e longitude).
    url = "https://nominatim.openstreetmap.org/search" # URL base da API Nominatim (OpenStreetMap) para busca.
    params = {
        # Dicionário de parâmetros da requisição.
        "q": f"{local}, Brazil", # 'q' é a consulta de busca, concatenando o 'local' com ", Brazil" para focar no Brasil.
        "format": "json",        # Solicita que a resposta seja em formato JSON.
        "limit": 1               # Limita a resposta a apenas um resultado (o mais relevante).
    }
    headers = {
        # Cabeçalhos da requisição. O 'User-Agent' é obrigatório para muitas APIs, incluindo Nominatim.
        "User-Agent": "MeuAppExemplo/1.0 (meuemail@exemplo.com)" # Identificação do seu aplicativo.
    }

    # Faz a requisição GET para a URL com os parâmetros e cabeçalhos definidos.
    resposta = requests.get(url, params=params, headers=headers)
    # Converte a resposta JSON em um objeto Python (lista de dicionários).
    dados = resposta.json()

    if dados:
        # Verifica se a lista de dados não está vazia (ou seja, se um resultado foi encontrado).
        lat = dados[0]['lat'] # Pega a latitude do primeiro (e único) resultado.
        lon = dados[0]['lon'] # Pega a longitude do primeiro (e único) resultado.
        return lat, lon       # Retorna a latitude e longitude.
    else:
        # Se nenhum dado for encontrado, retorna None.
        return None

def mostrarBoasVindas():
    # Define uma função para exibir uma mensagem de boas-vindas.
    print("=" * 50) # Imprime uma linha de 45 caracteres '=' para formatação.
    print("🌧️  Sistema de Previsão de Enchentes no Brasil! 🌧️") # Mensagem principal.
    print("-" * 50) # Imprime uma linha de 45 caracteres '-' para formatação.

def mostrarMenu():
    # Define uma função para exibir as opções do menu principal.
    print("[1] Procurar risco por CEP")   # Opção para buscar por CEP.
    print("[2] Procurar risco por Cidade") # Opção para buscar por cidade.
    print("[3] Sair do sistema") # Opção para sair do sistema.

def menu():
    # Define a função que gerencia o menu de seleção do usuário.
    escolha = str(input("Deseja especificar a localização como: ")) # Pergunta ao usuário como deseja especificar a localização.
    while True: # Inicia um loop infinito que continua até que uma opção válida seja escolhida ou 'voltar' seja digitado.
        if escolha == "1":
            # Se a escolha for '1' (CEP).
            limparTerminal()       # Limpa o terminal.
            mostrarBoasVindas()    # Mostra a mensagem de boas-vindas.
            print("Para voltar digite 'voltar'") # Instrução para o usuário voltar.
            localizacao = input("Insira o CEP: ").lower() # Pede o CEP e converte para minúsculas.
            if localizacao == "voltar":
                # Se o usuário digitar 'voltar'.
                limparTerminal()    # Limpa o terminal.
                mostrarBoasVindas() # Mostra as boas-vindas.
                mostrarMenu()       # Mostra o menu novamente.
                menu()              # Chama a função menu recursivamente para que o usuário possa escolher novamente.
            else:
                return localizacao # Retorna o CEP inserido.
        elif escolha == "2":
            # Se a escolha for '2' (Cidade).
            limparTerminal()       # Limpa o terminal.
            mostrarBoasVindas()    # Mostra a mensagem de boas-vindas.
            print("Para voltar digite 'voltar'") # Instrução para o usuário voltar.
            # Pede a cidade completa e converte para minúsculas.
            localizacao = input("Insira a cidade com o nome completo (ex: São Paulo, Minas Gerais): ").lower()
            if localizacao == "voltar":
                # Se o usuário digitar 'voltar'.
                limparTerminal()    # Limpa o terminal.
                mostrarBoasVindas() # Mostra as boas-vindas.
                mostrarMenu()       # Mostra o menu novamente.
                menu()              # Chama a função menu recursivamente.
            else:
                return localizacao # Retorna o nome da cidade.
        elif escolha == "3":
            # Se a escolha for '3' (Sair).
            print("Saindo do sistema...") # Mostra a mensagem de saída.
            time.sleep(2) # Pausa 2 segundos para o usuário ler a mensagem.
            quit() # Encerra o programa
        else:
            return None # Se a escolha não for '1' nem '2' nem '3', retorna None (opção inválida).

def calcularRisco(mm):
    # Define uma função para calcular o nível de risco de enchente baseado na precipitação em milímetros (mm).
    if mm > 80:
        return "Alerta grave"     # Acima de 80 mm é alerta grave.
    elif mm >= 50 and mm <= 80:
        return "Risco alto"       # Entre 50 e 80 mm é risco alto.
    elif mm < 50 and mm >= 20:
        return "Risco moderado"   # Entre 20 e 50 mm é risco moderado.
    elif mm < 20:
        return "Risco baixo"      # Abaixo de 20 mm é risco baixo.

def precipitacao(lat, lon):
    # Define uma função para obter e exibir a previsão de precipitação usando a API Open-Meteo.

    # Parâmetros da requisição para a API Open-Meteo.
    params = {
        "latitude": lat,                   # Latitude da localização.
        "longitude": lon,                  # Longitude da localização.
        "daily": "precipitation_sum",      # Solicita a soma diária da precipitação.
        "timezone": "auto"                 # Define o fuso horário automaticamente com base nas coordenadas.
    }

    url = "https://api.open-meteo.com/v1/forecast" # Endpoint da API Open-Meteo para previsão.

    # Faz a requisição GET para a API Open-Meteo com os parâmetros.
    resposta = requests.get(url, params=params)
    # Converte a resposta JSON em um objeto Python.
    dados = resposta.json()

    dias = dados['daily']['time']             # Extrai a lista de datas da previsão.
    precipitacoes = dados['daily']['precipitation_sum'] # Extrai a lista de somas de precipitação.

    print("\n📅 Previsão de precipitação e risco de enchente 📅") # Título da seção de previsão.
    # Itera sobre os dias e as precipitações simultaneamente usando 'zip'.
    for dia, mm in zip(dias, precipitacoes):
        risco = calcularRisco(mm) # Calcula o risco de enchente para a precipitação do dia.
        # Imprime a data, a precipitação em mm e o nível de risco.
        print(f"{dia}: {mm} mm → {risco}")


# --- Início do fluxo principal do programa ---
while True: # Loop principal do programa para permitir múltiplas consultas.
    limparTerminal()    # Limpa o terminal a cada nova iteração.
    mostrarBoasVindas() # Mostra a mensagem de boas-vindas.
    mostrarMenu()       # Exibe as opções do menu.
    local = menu()      # Chama a função menu para obter a localização (CEP ou cidade).

    if local == None:
        # Se 'menu()' retornar None, significa que o usuário digitou uma opção inválida.
        print("Opção inválida.") # Informa ao usuário.
        time.sleep(2)           # Pausa por 2 segundos para o usuário ler a mensagem.
        # O loop 'while True' continuará e mostrará o menu novamente após a pausa.
    else:
        # Se uma localização válida foi obtida.
        # Converte o CEP/cidade em coordenadas de latitude e longitude.
        coord = converterCEP(local)

        if coord:
            # Se as coordenadas foram obtidas com sucesso.
            # Chama a função 'precipitacao' para exibir a previsão do tempo e risco de enchente.
            precipitacao(coord[0], coord[1])
            # Pergunta ao usuário se deseja voltar ao menu principal.
            voltar = str(input("\nPara voltar digite 'voltar': ")).lower()
            if voltar == "voltar":
                # Se o usuário digitar 'voltar', o loop principal continuará, limpando a tela e mostrando o menu novamente.
                pass # 'pass' não faz nada, apenas permite que o 'if' termine e o loop continue.
            else:
                # Se o usuário digitar qualquer outra coisa, exibe uma mensagem e sai do programa.
                print("Saindo do sistema. Até logo!")
                time.sleep(2)
                break # Sai do loop principal, encerrando o programa.
        else:
            # Se as coordenadas não puderam ser obtidas (localização inválida).
            print("❌ Localização inválida. Não foi possível encontrar coordenadas para o CEP/Cidade.")
            time.sleep(3) # Pausa para o usuário ler a mensagem antes de voltar ao menu.
