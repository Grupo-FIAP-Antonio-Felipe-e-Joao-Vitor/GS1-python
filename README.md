# 🌧️ Sistema de Previsão de Enchentes no Brasil

Este é um sistema de linha de comando que permite consultar a previsão de chuvas e estimar o risco de enchentes em localidades do Brasil com base em CEP ou nome da cidade. Ele utiliza dados da API [Open-Meteo](https://open-meteo.com/) para previsão do tempo e a API [Nominatim (OpenStreetMap)](https://nominatim.org/) para geocodificação (conversão de localização em coordenadas).

---

## 📦 Funcionalidades

- Consulta por **CEP** ou **nome completo da cidade**.
- Conversão automática da localização em coordenadas geográficas.
- Previsão diária de precipitação (chuvas) para os próximos dias.
- Cálculo e exibição do **nível de risco de enchente** com base na quantidade de chuva:
  - Abaixo de 20 mm → Risco Baixo
  - Entre 20 mm e 49 mm → Risco Moderado
  - Entre 50 mm e 80 mm → Risco Alto
  - Acima de 80 mm → Alerta Grave

---

## 🛠️ Tecnologias Utilizadas

- Python
- Bibliotecas:
  - `requests` – Para requisições HTTP às APIs.
  - `os` – Para comandos no terminal (como limpar tela).
  - `time` – Para pausas e mensagens temporizadas.

---
