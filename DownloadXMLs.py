import tkinter as tk
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os
import time
import pyautogui

################## ALTERAR #######################################
LoginUusario = #Defina o login                                   
LoginSenha= #Defina sua senha                                    
LinkSite = #Define o link do site                                
chromedriver_path = #Defina o caminho onde está o chromedriver   
XpathUsuario = #Inserir o Xpah do campo usuário                  
XpathSenha = #Inserir o Xpah do campo senha                      
XpathClique = #Inserir o Xpah do campo de Entrar no login 
LinkNovaPagina = #Inserir link da nova página dentr do navegador
XpathData = #Inserir campo da data
XpathNumerosNF = #Inserir onde vai ser inserido os numeros solicitados na interface
xpathpesquisar = #Inserir onde vai ser clicado para a pesquisa
xpathXML = #Botão que vai abrir o XML
DiretorioSalvar = #Inserir diretório onde será salvo os XMLs
##################################################################


# Verificar se o ChromeDriver existe
if not os.path.isfile(chromedriver_path):
    raise FileNotFoundError(f'O ChromeDriver não foi encontrado em {chromedriver_path}')

# Função para baixar NFE 
def baixar_nfes(nfe_numbers):
    service = Service(chromedriver_path)
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-infobars")
    chrome_options.add_argument("--start-maximized")

    driver = webdriver.Chrome(service=service, options=chrome_options)

    try:
        driver.get(LinkSite)
        original_tab = driver.current_window_handle

        wait = WebDriverWait(driver, 10)
        time.sleep(2)

        email_field = wait.until(EC.visibility_of_element_located((By.XPATH, XpathUsuario)))
        email_field.send_keys(LoginUusario)

        password_field = wait.until(EC.visibility_of_element_located((By.XPATH, XpathSenha)))
        password_field.send_keys(LoginSenha)

        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, XpathClique)))
        login_button.click()
        
        time.sleep(5)

        for nfe_number in nfe_numbers:
            if not nfe_number: 
                continue
            
            driver.execute_script("window.open('');")
            new_tab = driver.window_handles[-1]
            driver.switch_to.window(new_tab)
            driver.get(LinkNovaPagina)

            date_field = wait.until(EC.visibility_of_element_located((By.XPATH, XpathData)))
            date_field.clear()
            date_field.send_keys("30/05/2024")

            nfe_initial_field = wait.until(EC.visibility_of_element_located((By.XPATH, XpathNumerosNF)))
            nfe_initial_field.clear()
            nfe_initial_field.send_keys(nfe_number)

            search_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpathpesquisar)))
            search_button.click()

            time.sleep(5)

            xml_link_button = wait.until(EC.element_to_be_clickable((By.XPATH, xpathXML)))
            xml_link_button.click()
            
            time.sleep(3)
            #salvar como
            pyautogui.hotkey('ctrl', 's')
            time.sleep(3)
#salvar como
            path = DiretorioSalvar
            pyautogui.typewrite(path)
            pyautogui.press('enter')

            time.sleep(10)

            driver.close()
            driver.switch_to.window(original_tab)

    finally:
        time.sleep(10)
        driver.quit()

# Função para obter os números de NFE da interface gráfica e iniciar o download
def iniciar_download():
    nfe_numbers = entry.get().split(",")  # Obter números de NFE da entrada e separar por vírgula
    baixar_nfes(nfe_numbers)

# Criar a interface gráfica
root = tk.Tk()
root.title("Baixar NFEs")


label = tk.Label(root, text="Insira os números das NFEs separados por vírgula:")
label.pack(pady=5)

entry = tk.Entry(root, width=50)
entry.pack(pady=5)

button = tk.Button(root, text="Baixar NFEs", command=iniciar_download)
button.pack(pady=20)

root.mainloop()
