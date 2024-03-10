from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from twilio.rest import Client
import os
import time
from datetime import datetime, timedelta

def main():
    # Defina a data e horário de início da automação
    start_date = input("Digite a data de início (DD/MM/YYYY): ")
    start_time = input("Digite o horário de início (HH:MM): ")
    
    # Converter a data e o horário para um objeto datetime
    start_datetime = datetime.strptime(start_date + " " + start_time, "%d/%m/%Y %H:%M")

    # Solicitação de input do usuário para o período de tempo (em minutos)
    duration = int(input("Digite a duração da automação (em minutos): "))

    # Configurações do ChromeDriver
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--start-maximized")
   # chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    try:
        # URL do site de login
        url_login = "https://www.medicalsoft.com.br/imageserver/irdf/"

        # Preencha suas credenciais aqui
        usuario = "medical"
        senha = "medico"

        # Configurações da Twilio
        twilio_account_sid = "AC7b8bbaf2978bb0b96d560509a32e9ab1"
        twilio_auth_token = "fdd2b83e9709295f4e3e3203379250ee"
        twilio_phone_number = "+17622635635"
        seu_numero_destino = "+5562996295252"

        # Abre a página de login
        driver.get(url_login)

        # Preenche as credenciais de login usando os atributos de id
        campo_usuario = driver.find_element(By.ID, "usuario")
        campo_usuario.send_keys(usuario)

        campo_senha = driver.find_element(By.ID, "senha")
        campo_senha.send_keys(senha)

        # Realiza o login
        campo_senha.send_keys(Keys.RETURN)

        # Aguarda alguns segundos para garantir que o login seja concluído
        time.sleep(5)

        while datetime.now() < start_datetime:
            time.sleep(5)  # Aguarda 1 minuto até que o horário de início seja atingido

        end_datetime = start_datetime + timedelta(minutes=duration)
        
        while datetime.now() <= end_datetime:
            # Clique no elemento com a classe "ri-filter-line" e título "Filtrar Estudos"
            elemento_filtrar_estudos = driver.find_element(By.CSS_SELECTOR, "i.ri-filter-line[data-original-title='Filtrar estudos']")
            elemento_filtrar_estudos.click()

            # Aguarde um tempo para que a ação seja concluída
            time.sleep(5)

            # Clique na opção "Urgencia" diretamente pelo atributo value
            opcao_urgencia = driver.find_element(By.CSS_SELECTOR, "option[value='1']")
            opcao_urgencia.click()

            # Aguarde um tempo para que a ação seja concluída
            time.sleep(5)

            # Marcar as opções "RAIOS X-ID:1" e "TOMOGRAFIA-ID:31"
            opcao_raios_x = driver.find_element(By.XPATH, "//label[@data-original-title='RAIOS X-ID:1']")
            opcao_raios_x.click()

            opcao_tomografia = driver.find_element(By.XPATH, "//label[@data-original-title='TOMOGRAFIA-ID:31']")
            opcao_tomografia.click()

            # Aguarde um tempo para que a ação seja concluída
            time.sleep(5)

            # Clique no botão de "Realizar pesquisa"
            botao_pesquisa = driver.find_element(By.XPATH, "//a[@data-original-title='Realizar pesquisa']")
            botao_pesquisa.click()

            # Aguarde um tempo para que a pesquisa seja concluída
            time.sleep(5)

            # Verifique se existe registro
            registros = driver.find_elements(By.CSS_SELECTOR, "td.dataTables_empty")
            if registros:
                print("Não existe registro")
            else:
                print("Existe registro")
                # Inicie a chamada telefônica usando a biblioteca Twilio
                client = Client(twilio_account_sid, twilio_auth_token)
                call = client.calls.create(
                    to=seu_numero_destino,
                    from_=twilio_phone_number,
                    url="http://demo.twilio.com/docs/voice.xml"  # Substitua pelo URL do XML de instruções da chamada
                )
                print("Chamada telefônica iniciada:", call.sid)

            # Aguarda minuto em segundos
            time.sleep(1200)

    except Exception as e:
        print("Ocorreu um erro durante a automação:", e)
        # Aqui você pode adicionar ações específicas que deseja executar em caso de erro
        # Por exemplo, enviar uma mensagem ou notificação sobre o erro
    

if __name__ == "__main__":
    main()
#(pyinstaller --onefile Italo.py) PARA DEIXAR O PROGRAMA AUTO EXECUTAVEL