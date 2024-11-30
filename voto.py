from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

# Caminho do WebDriver
driver_path = r"C:\Users\Diego\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"  # Atualize com o caminho correto
service = Service(driver_path)

planilha_path = r"D:\Projects\vote\leads.xlsx"  # Substitua pelo caminho correto

emails = pd.read_excel(planilha_path, usecols=[0], skiprows=1).squeeze().tolist()

driver = webdriver.Chrome(service=service)

site_url = "https://forms.gle/NCxVebXSquJtTUGg7"  # Substitua pelo URL correto

def votar(email):
    try:
        driver.get(site_url)
        wait = WebDriverWait(driver, 10)

        email_field = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@type='email']")))
        email_field.clear()
        email_field.send_keys(email)
        print(f"Preenchendo o email: {email}")

        opcao_especifica = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@role='radio' and @data-value='Luis Leão']")))
        opcao_especifica.click()
        print(f"Selecionada a opção 'Luis Leão' para o email: {email}")

        enviar_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[text()='Enviar']")))
        enviar_button.click()

        print(f"Voto enviado para o email: {email}")
        time.sleep(60)  

    except Exception as e:
        print(f"Erro ao votar com o email {email}: {e}")


try:
    for email in emails:
        votar(email)
finally:
    driver.quit()
