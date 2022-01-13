from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

navegador = webdriver.Chrome("chromedriver.exe") 

# Pegar a cotacao do Dolar
navegador.get("https://www.google.com.br/")

navegador.find_element(By.XPATH,
                      '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div[2]/div[2]/input').send_keys("cotação dolar")

navegador.find_element(By.XPATH, 
                       '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[3]/center/input[1]').send_keys(Keys.ENTER)

cotacao_dolar = navegador.find_element(By.XPATH,
                       '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute("data-value")
print(cotacao_dolar)

# Pegar a cotacao euro
navegador.get("https://www.google.com.br/")

navegador.find_element(By.XPATH,
                      '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div[2]/div[2]/input').send_keys("cotação euro")

navegador.find_element(By.XPATH, 
                       '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[3]/center/input[1]').send_keys(Keys.ENTER)

cotacao_euro = navegador.find_element(By.XPATH,
                       '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute("data-value")
print(cotacao_euro)

# Pegar a cotacao do Ouro

navegador.get("https://www.melhorcambio.com/ouro-hoje")

cotacao_ouro = navegador.find_element(By.XPATH,
                      '//*[@id="comercial"]').get_attribute("value")

cotacao_ouro = cotacao_ouro.replace(",", ".")
print(cotacao_ouro)

navegador.quit()

# Importar a base e atualizar as cotacoes na minha base
import pandas as pd
import openpyxl

database = pd.read_excel(r"Produtos.xlsx", engine='openpyxl')

# Atualizar a cotação

# database.loc[linha, coluna] = float(cotacao_tipo)

database.loc[database["Moeda"] == "Dólar", "Cotação"] = float(cotacao_dolar)
database.loc[database["Moeda"] == "Euro", "Cotação"] = float(cotacao_euro)
database.loc[database["Moeda"] == "Ouro", "Cotação"] = float(cotacao_ouro)
             
database["Preço de Compra"] = database["Preço Original"] * database["Cotação"]

database["Preço de Venda"] = database["Preço de Compra"] * database["Margem"]

display(database)


# Exportar a nova base de preços atualizada

database.to_excel("Produtos Novo.xlsx", index=False)

