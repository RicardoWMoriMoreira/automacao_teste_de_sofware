import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def configurar_driver():
    """Configura e retorna uma instância do WebDriver do Chrome."""
    print("Configurando o WebDriver...")
    try:
        servico = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=servico)
        driver.implicitly_wait(10)
        driver.maximize_window()
        return driver
    except Exception as e:
        print(f"Erro ao configurar o WebDriver: {e}")
        return None

def verificar_sessao_driver(driver):
    """Verifica se a sessão do driver ainda está válida."""
    try:
        driver.current_url
        return True
    except Exception:
        return False

# --- Funções de Teste (a lógica interna não muda) ---

def teste_saucedemo_valido(driver):
    """(SUCESSO ESPERADO) Testa o login válido no saucedemo.com."""
    print("\n--- Iniciando Teste 1.1: Sauce Demo (Login Válido) ---")
    try:
        # Verifica se a sessão do driver ainda está válida
        if not verificar_sessao_driver(driver):
            print(">>> Teste 1.1 (Válido): ERRO - Sessão do driver inválida. Reiniciando...")
            return False
            
        driver.get("https://www.saucedemo.com")
        time.sleep(2)  # Aguarda a página carregar
        
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("secret_sauce")
        driver.find_element(By.ID, "login-button").click()
        
        time.sleep(3)  # Aguarda o redirecionamento

        if "inventory.html" in driver.current_url:
            print(">>> Teste 1.1 (Válido): SUCESSO. Login realizado e página de produtos carregada.")
        else:
            print(">>> Teste 1.1 (Válido): FALHA. Não redirecionou para a página correta.")
    except Exception as e:
        print(f">>> Teste 1.1 (Válido): Ocorreu um erro inesperado. -> {e}")
        # Se for erro de sessão inválida, tenta recriar o driver
        if "invalid session id" in str(e).lower():
            print(">>> Detectado erro de sessão inválida. Reiniciando driver...")
            return False
    finally:
        time.sleep(1)

def teste_saucedemo_invalido(driver):
    """(SUCESSO ESPERADO) Testa o login inválido e a exibição de erro no saucedemo.com."""
    print("\n--- Iniciando Teste 1.2: Sauce Demo (Login Inválido) ---")
    try:
        driver.get("https://www.saucedemo.com")
        driver.find_element(By.ID, "user-name").send_keys("standard_user")
        driver.find_element(By.ID, "password").send_keys("senha_errada")
        driver.find_element(By.ID, "login-button").click()
        
        mensagem_erro = driver.find_element(By.CSS_SELECTOR, "h3[data-test='error']")
        if mensagem_erro.is_displayed():
            print(">>> Teste 1.2 (Inválido): SUCESSO. Mensagem de erro foi exibida como esperado.")
        else:
            print(">>> Teste 1.2 (Inválido): FALHA. Mensagem de erro não foi encontrada.")
    except Exception as e:
        print(f">>> Teste 1.2 (Inválido): Ocorreu um erro inesperado. -> {e}")
    finally:
        time.sleep(1)

def teste_practicetestautomation_valido(driver):
    """(SUCESSO ESPERADO) Testa o login válido no practicetestautomation.com."""
    print("\n--- Iniciando Teste 2.1: Practice Automation (Login Válido) ---")
    try:
        driver.get("https://practicetestautomation.com/practice-test-login/")
        driver.find_element(By.ID, "username").send_keys("student")
        driver.find_element(By.ID, "password").send_keys("Password123")
        driver.find_element(By.ID, "submit").click()
        
        if "logged-in-successfully" in driver.current_url and driver.find_element(By.LINK_TEXT, "Log out").is_displayed():
             print(">>> Teste 2.1 (Válido): SUCESSO. Login realizado e botão 'Log out' visível.")
        else:
            print(">>> Teste 2.1 (Válido): FALHA no login.")
    except Exception as e:
        print(f">>> Teste 2.1 (Válido): Ocorreu um erro inesperado. -> {e}")
    finally:
        time.sleep(1)

def teste_practicetestautomation_invalido(driver):
    """(SUCESSO ESPERADO) Testa o login inválido no practicetestautomation.com."""
    print("\n--- Iniciando Teste 2.2: Practice Automation (Login Inválido) ---")
    try:
        driver.get("https://practicetestautomation.com/practice-test-login/")
        driver.find_element(By.ID, "username").send_keys("student")
        driver.find_element(By.ID, "password").send_keys("SenhaErrada123")
        driver.find_element(By.ID, "submit").click()
        
        mensagem_erro = driver.find_element(By.ID, "error")
        if mensagem_erro.is_displayed():
             print(">>> Teste 2.2 (Inválido): SUCESSO. Mensagem de erro foi exibida como esperado.")
        else:
            print(">>> Teste 2.2 (Inválido): FALHA. Mensagem de erro não foi encontrada.")
    except Exception as e:
        print(f">>> Teste 2.2 (Inválido): Ocorreu um erro inesperado. -> {e}")
    finally:
        time.sleep(1)

def teste_theinternet_valido(driver):
    """(SUCESSO ESPERADO) Testa o login válido no the-internet.herokuapp.com."""
    print("\n--- Iniciando Teste 2.3: The Internet (Login Válido) ---")
    try:
        # Verifica se a sessão do driver ainda está válida
        if not verificar_sessao_driver(driver):
            print(">>> Teste 2.3 (Válido): ERRO - Sessão do driver inválida.")
            return False
            
        driver.get("https://the-internet.herokuapp.com/login")
        time.sleep(2)  # Aguarda a página carregar
        
        driver.find_element(By.ID, "username").send_keys("tomsmith")
        driver.find_element(By.ID, "password").send_keys("SuperSecretPassword!")
        driver.find_element(By.TAG_NAME, "button").click()
        
        time.sleep(3)  # Aguarda o redirecionamento

        # Verifica se foi redirecionado para a página segura
        if "/secure" in driver.current_url:
            print(">>> Teste 2.3 (Válido): SUCESSO. Login realizado e redirecionado para área segura.")
        else:
            print(">>> Teste 2.3 (Válido): FALHA. Não redirecionou para a área segura.")
    except Exception as e:
        print(f">>> Teste 2.3 (Válido): Ocorreu um erro inesperado. -> {e}")
        if "invalid session id" in str(e).lower():
            print(">>> Detectado erro de sessão inválida.")
            return False
    finally:
        time.sleep(1)

def teste_theinternet_invalido(driver):
    """(SUCESSO ESPERADO) Testa o login inválido no the-internet.herokuapp.com."""
    print("\n--- Iniciando Teste 2.4: The Internet (Login Inválido) ---")
    try:
        driver.get("https://the-internet.herokuapp.com/login")
        time.sleep(2)
        
        driver.find_element(By.ID, "username").send_keys("tomsmith")
        driver.find_element(By.ID, "password").send_keys("senha_errada")
        driver.find_element(By.TAG_NAME, "button").click()
        
        time.sleep(2)
        
        # Verifica se a mensagem de erro foi exibida
        mensagem_erro = driver.find_element(By.ID, "flash")
        if mensagem_erro.is_displayed() and "Your password is invalid!" in mensagem_erro.text:
            print(">>> Teste 2.4 (Inválido): SUCESSO. Mensagem de erro foi exibida como esperado.")
        else:
            print(">>> Teste 2.4 (Inválido): FALHA. Mensagem de erro não foi encontrada ou incorreta.")
    except Exception as e:
        print(f">>> Teste 2.4 (Inválido): Ocorreu um erro inesperado. -> {e}")
    finally:
        time.sleep(1)

def teste_orangehrm_valido(driver):
    """(SUCESSO ESPERADO) Testa o login válido no OrangeHRM."""
    print("\n--- Iniciando Teste 3.1: OrangeHRM (Login Válido) ---")
    try:
        driver.get("https://opensource-demo.orangehrmlive.com/")
        time.sleep(2)
        driver.find_element(By.NAME, "username").send_keys("Admin")
        driver.find_element(By.NAME, "password").send_keys("admin123")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()

        if driver.find_element(By.CLASS_NAME, "oxd-topbar-header-breadcrumb").is_displayed():
            print(">>> Teste 3.1 (Válido): SUCESSO. Login realizado e dashboard carregado.")
        else:
            print(">>> Teste 3.1 (Válido): FALHA no login.")
    except Exception as e:
        print(f">>> Teste 3.1 (Válido): Ocorreu um erro inesperado. -> {e}")
    finally:
        time.sleep(1)
        
def teste_orangehrm_invalido(driver):
    """(SUCESSO ESPERADO) Testa o login inválido no OrangeHRM."""
    print("\n--- Iniciando Teste 3.2: OrangeHRM (Login Inválido) ---")
    try:
        driver.get("https://opensource-demo.orangehrmlive.com/")
        time.sleep(2)
        driver.find_element(By.NAME, "username").send_keys("Admin")
        driver.find_element(By.NAME, "password").send_keys("senha_incorreta")
        driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
        
        mensagem_erro = driver.find_element(By.CSS_SELECTOR, ".oxd-alert--error")
        if mensagem_erro.is_displayed():
            print(">>> Teste 3.2 (Inválido): SUCESSO. Mensagem de 'Invalid credentials' foi exibida.")
        else:
            print(">>> Teste 3.2 (Inválido): FALHA. Mensagem de erro não foi encontrada.")
    except Exception as e:
        print(f">>> Teste 3.2 (Inválido): Ocorreu um erro inesperado. -> {e}")
    finally:
        time.sleep(1)

# --- Bloco de Execução Principal (ORDEM ALTERADA) ---
if __name__ == "__main__":
    driver = None
    try:
        driver = configurar_driver()
        
        if driver is None:
            print("ERRO: Não foi possível configurar o WebDriver. Encerrando testes.")
            exit(1)

        # Bloco 1: Executando todos os testes com situações INVÁLIDAS primeiro
        print("\n=======================================================")
        print("--- INICIANDO BATERIA DE TESTES COM SITUAÇÕES INVÁLIDAS ---")
        print("=======================================================")
        
        teste_saucedemo_invalido(driver)
        teste_practicetestautomation_invalido(driver)
        teste_theinternet_invalido(driver)
        teste_orangehrm_invalido(driver)

        # Verifica se o driver ainda está válido antes dos testes válidos
        if not verificar_sessao_driver(driver):
            print("\n⚠️ Driver perdeu a sessão. Reiniciando para testes válidos...")
            driver.quit()
            driver = configurar_driver()
            if driver is None:
                print("ERRO: Não foi possível reiniciar o WebDriver.")
                exit(1)

        # Bloco 2: Executando todos os testes com situações VÁLIDAS
        print("\n\n=====================================================")
        print("--- INICIANDO BATERIA DE TESTES COM SITUAÇÕES VÁLIDAS ---")
        print("=====================================================")

        teste_saucedemo_valido(driver)
        teste_practicetestautomation_valido(driver)
        teste_theinternet_valido(driver)
        teste_orangehrm_valido(driver)

        print("\n--- Todos os testes foram concluídos. ---")

    except Exception as e:
        print(f"\nOcorreu um erro geral na execução dos testes: {e}")

    finally:
        if driver:
            try:
                driver.quit()
                print("WebDriver fechado com sucesso.")
            except Exception as e:
                print(f"Erro ao fechar o WebDriver: {e}") 

