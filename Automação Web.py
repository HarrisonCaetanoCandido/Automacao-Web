#!/usr/bin/env python
# coding: utf-8

# # Automação Web e Busca de Informações com Python
# 
# #### Desafio: 
# 
# Trabalhamos em uma importadora e o preço dos nossos produtos é vinculado a cotação de:
# - Dólar
# - Euro
# - Ouro
# 
# Precisamos pegar na internet, de forma automática, a cotação desses 3 itens e saber quanto devemos cobrar pelos nossos produtos, considerando uma margem de contribuição que temos na nossa base de dados.
# 
# Base de Dados: https://drive.google.com/drive/folders/1KmAdo593nD8J9QBaZxPOG1yxHZua4Rtv?usp=sharing
# 
# Para isso, vamos criar uma automação web:
# 
# - Usaremos o selenium
# - Importante: baixar o webdriver

# In[27]:


# web driver -> chrome -> chromedriver
# Firefox -> geckodriver
from selenium import webdriver #O CRIADOR RECOMENDA PEGAR SO UMA PARTE DA BIBLIOTECA E NAO ELA TODA
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

navegador = webdriver.Chrome("chromedriver.exe") #navegador =  webdriver.Chrome("chromedriver.exe") #-> quando o chromedriver tiver no mesmo local

# Passo 1: Pegar a cotacao do Dolar
navegador.get("https://www.google.com.br/")

# ESCREVER send_keys()
# CLICAR é .click()
# PEGAR info é get_attribute()

navegador.find_element(By.XPATH,
                      '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div[2]/div[2]/input').send_keys("cotação dolar")
#SEMPRE QUE FOR PASSAR XPATH PASSE ELE EM ASPAS SIMPLES PQ AS VEZES PODE HAVER UMA ASPAS DUPLAS DENTRO DO XPATH
navegador.find_element(By.XPATH, 
                       '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[3]/center/input[1]').send_keys(Keys.ENTER)

cotacao_dolar = navegador.find_element(By.XPATH,
                       '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute("data-value")
print(cotacao_dolar)


# In[28]:


# Passo 2: Pegar a cotacao euro
navegador.get("https://www.google.com.br/")

navegador.find_element(By.XPATH,
                      '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[1]/div[2]/div[2]/input').send_keys("cotação euro")
#SEMPRE QUE FOR PASSAR XPATH PASSE ELE EM ASPAS SIMPLES PQ AS VEZES PODE HAVER UMA ASPAS DUPLAS DENTRO DO XPATH
navegador.find_element(By.XPATH, 
                       '/html/body/div[1]/div[3]/form/div[1]/div[1]/div[3]/center/input[1]').send_keys(Keys.ENTER)

cotacao_euro = navegador.find_element(By.XPATH,
                       '//*[@id="knowledge-currency__updatable-data-column"]/div[1]/div[2]/span[1]').get_attribute("data-value")
print(cotacao_euro)


# In[29]:


# Passo 3: Pegar a cotacao do Ouro

navegador.get("https://www.melhorcambio.com/ouro-hoje")

cotacao_ouro = navegador.find_element(By.XPATH,
                      '//*[@id="comercial"]').get_attribute("value")
#SEMPRE QUE FOR PASSAR XPATH PASSE ELE EM ASPAS SIMPLES PQ AS VEZES PODE HAVER UMA ASPAS DUPLAS DENTRO DO XPATH

cotacao_ouro = cotacao_ouro.replace(",", ".")
print(cotacao_ouro)

navegador.quit() #PARA FECHAR O NAVEGADOR


# ### Agora vamos atualiza a nossa base de preços com as novas cotações

# - Importando a base de dados

# In[30]:


# Passo 4: Importar a base e atualizar as cotacoes na minha base
import pandas as pd
import openpyxl

database = pd.read_excel(r"Produtos.xlsx", engine='openpyxl')
                         #r serve para dizer para o python nao ler caracter especial

display(database)


# - Atualizando os preços e o cálculo do Preço Final

# In[31]:


# Passo 5: Calcular os novos preços e salvar/reportar a base de dados
# atualizar a cotação
# nas linhas onde na coluna "Moeda" = Dólar

#database.loc[linha, coluna] = float(cotacao_dolar)

database.loc[database["Moeda"] == "Dólar", "Cotação"] = float(cotacao_dolar)
database.loc[database["Moeda"] == "Euro", "Cotação"] = float(cotacao_euro)
database.loc[database["Moeda"] == "Ouro", "Cotação"] = float(cotacao_ouro)

# ATUALIZAR AS COLUNAS
             
# PREÇO de compra = Preço Original * Cotação
database["Preço de Compra"] = database["Preço Original"] * database["Cotação"]
 
# PREÇO de Venda = Preço de Compra * Margem
database["Preço de Venda"] = database["Preço de Compra"] * database["Margem"]

display(database)


# ### Agora vamos exportar a nova base de preços atualizada

# In[32]:


database.to_excel("Produtos Novo.xlsx", index=False) #PARA EXCEL SEMPRE PASSE DUAS INFOS (NOME, OPCIONAL: Tirar o INDEX (QUE TEM OS NUMEROS E TAL NA TABELA))

