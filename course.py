from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Configuração do Chrome com a opção de manter o navegador aberto
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)

# URL do site
website = "https://www.adamchoi.co.uk/overs/detailed"
driver = webdriver.Chrome(options=options)
driver.get(website)

try:
    # Esperar até que o botão "All Matches" esteja clicável
    all_matches = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//*[@id='page-wrapper']/div/home-away-selector/div/div/div/div/label[2]"))
    )
    all_matches.click()
    
    dropdown  = Select(driver.find_element(By.ID, value="country"))
    dropdown.select_by_visible_text('Brazil')
    
    time.sleep(3)

    # Esperar até que as linhas da tabela estejam carregadas
    matches = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.TAG_NAME, "tr"))
    )

    # Listas para armazenar os dados
    date = []
    home_team = []
    score = []
    away_team = []

    # Iterar sobre os jogos e coletar os dados
    for match in matches:
        try:
            # Verifica se a linha contém elementos <td>
            cells = match.find_elements(By.TAG_NAME, "td")
            if len(cells) < 4:  # Ignorar linhas que não possuem as 4 colunas esperadas
                continue

            # Coleta os dados de cada célula
            date.append(cells[0].text)
            home_team.append(cells[1].text)
            score.append(cells[2].text)
            away_team.append(cells[3].text)

            print(f"Data: {cells[0].text}, Time da casa: {cells[1].text}, Placar: {cells[2].text}, Time visitante: {cells[3].text}")
        except Exception as e:
            print(f"Erro ao processar linha: {e}")

finally:
    # Fechar o navegador (remova esta linha se quiser manter o navegador aberto)
    driver.quit()

df = pd.DataFrame({'date': date, 'home_team': home_team, 'score': score, 'away_team': away_team})
df.to_csv('football_data.csv', index=True)
print(df)
