import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

class LoginAutomatico:
    def __init__(self):
        """Inicializa o driver do Chrome"""
        self.service = ChromeService(executable_path=ChromeDriverManager().install())
        self.driver = None
        
    def iniciar_navegador(self):
        """Inicia o navegador Chrome"""
        try:
            self.driver = webdriver.Chrome(service=self.service)
            self.driver.maximize_window()
            print("✅ Navegador iniciado com sucesso!")
            return True
        except Exception as e:
            print(f"❌ Erro ao iniciar navegador: {e}")
            return False
    
    def fazer_login(self, url, username, password, username_field_id=None, password_field_id=None, login_button_id=None):
        """
        Faz login automático na URL especificada
        
        Args:
            url: URL da página de login
            username: Nome de usuário
            password: Senha
            username_field_id: ID do campo de usuário (opcional)
            password_field_id: ID do campo de senha (opcional)
            login_button_id: ID do botão de login (opcional)
        """
        try:
            print(f"\n--- Tentando login em: {url} ---")
            
            # Navega para a URL
            self.driver.get(url)
            print(f"✅ Navegou para: {url}")
            
            # Aguarda a página carregar
            time.sleep(2)
            
            # Tenta encontrar os campos de login automaticamente
            username_field = self._encontrar_campo_usuario(username_field_id)
            password_field = self._encontrar_campo_senha(password_field_id)
            login_button = self._encontrar_botao_login(login_button_id)
            
            if not username_field:
                print("❌ Não foi possível encontrar o campo de usuário")
                return False
                
            if not password_field:
                print("❌ Não foi possível encontrar o campo de senha")
                return False
                
            if not login_button:
                print("❌ Não foi possível encontrar o botão de login")
                return False
            
            # Preenche os campos
            username_field.clear()
            username_field.send_keys(username)
            print(f"✅ Preencheu usuário: {username}")
            
            password_field.clear()
            password_field.send_keys(password)
            print("✅ Preencheu senha")
            
            # Clica no botão de login
            login_button.click()
            print("✅ Clicou no botão de login")
            
            # Aguarda um pouco para ver o resultado
            time.sleep(3)
            
            # Verifica se o login foi bem-sucedido
            if self._verificar_login_sucesso():
                print("✅ Login realizado com sucesso!")
                return True
            else:
                print("❌ Login falhou ou não foi possível verificar o sucesso")
                return False
                
        except Exception as e:
            print(f"❌ Erro durante o login: {e}")
            return False
    
    def _encontrar_campo_usuario(self, field_id=None):
        """Tenta encontrar o campo de usuário"""
        if field_id:
            try:
                return self.driver.find_element(By.ID, field_id)
            except NoSuchElementException:
                pass
        
        # Tenta encontrar por diferentes seletores
        seletores_usuario = [
            (By.ID, "username"),
            (By.ID, "user-name"),
            (By.NAME, "username"),
            (By.NAME, "user"),
            (By.CSS_SELECTOR, "input[type='text'][name*='user']"),
            (By.CSS_SELECTOR, "input[type='email']"),
            (By.XPATH, "//input[@placeholder*='usuário' or @placeholder*='username' or @placeholder*='email']")
        ]
        
        for by, selector in seletores_usuario:
            try:
                return self.driver.find_element(by, selector)
            except NoSuchElementException:
                continue
        
        return None
    
    def _encontrar_campo_senha(self, field_id=None):
        """Tenta encontrar o campo de senha"""
        if field_id:
            try:
                return self.driver.find_element(By.ID, field_id)
            except NoSuchElementException:
                pass
        
        # Tenta encontrar por diferentes seletores
        seletores_senha = [
            (By.ID, "password"),
            (By.NAME, "password"),
            (By.CSS_SELECTOR, "input[type='password']"),
            (By.XPATH, "//input[@placeholder*='senha' or @placeholder*='password']")
        ]
        
        for by, selector in seletores_senha:
            try:
                return self.driver.find_element(by, selector)
            except NoSuchElementException:
                continue
        
        return None
    
    def _encontrar_botao_login(self, button_id=None):
        """Tenta encontrar o botão de login"""
        if button_id:
            try:
                return self.driver.find_element(By.ID, button_id)
            except NoSuchElementException:
                pass
        
        # Tenta encontrar por diferentes seletores
        seletores_botao = [
            (By.ID, "login-button"),
            (By.ID, "submit"),
            (By.CSS_SELECTOR, "button[type='submit']"),
            (By.CSS_SELECTOR, "input[type='submit']"),
            (By.XPATH, "//button[contains(text(), 'Login') or contains(text(), 'Entrar') or contains(text(), 'Sign in')]"),
            (By.XPATH, "//input[@value='Login' or @value='Entrar' or @value='Sign in']"),
            (By.TAG_NAME, "button")
        ]
        
        for by, selector in seletores_botao:
            try:
                elemento = self.driver.find_element(by, selector)
                if elemento.is_displayed() and elemento.is_enabled():
                    return elemento
            except NoSuchElementException:
                continue
        
        return None
    
    def _verificar_login_sucesso(self):
        """Tenta verificar se o login foi bem-sucedido"""
        try:
            # Aguarda um pouco para a página carregar
            time.sleep(2)
            
            # Verifica se a URL mudou (indicando redirecionamento após login)
            current_url = self.driver.current_url
            
            # Verifica por elementos que indicam sucesso
            indicadores_sucesso = [
                "dashboard",
                "home",
                "welcome",
                "profile",
                "account",
                "logout",
                "log out"
            ]
            
            # Verifica na URL
            for indicador in indicadores_sucesso:
                if indicador in current_url.lower():
                    return True
            
            # Verifica por elementos na página
            try:
                # Procura por mensagens de sucesso
                sucesso_elements = self.driver.find_elements(By.XPATH, 
                    "//*[contains(text(), 'Welcome') or contains(text(), 'Bem-vindo') or contains(text(), 'Success') or contains(text(), 'Sucesso')]")
                if sucesso_elements:
                    return True
                
                # Procura por botão de logout
                logout_elements = self.driver.find_elements(By.XPATH,
                    "//*[contains(text(), 'Logout') or contains(text(), 'Log out') or contains(text(), 'Sair')]")
                if logout_elements:
                    return True
                    
            except:
                pass
            
            return False
            
        except Exception:
            return False
    
    def fechar_navegador(self):
        """Fecha o navegador"""
        if self.driver:
            self.driver.quit()
            print("✅ Navegador fechado")

def main():
    """Função principal que interage com o usuário"""
    print("=== PROGRAMA DE LOGIN AUTOMÁTICO ===")
    print("Este programa faz login automático em qualquer site!")
    
    # Inicializa o sistema
    login_system = LoginAutomatico()
    
    if not login_system.iniciar_navegador():
        return
    
    try:
        while True:
            print("\n" + "="*50)
            print("Digite as informações para o login:")
            
            # Solicita informações do usuário
            url = input("URL da página de login: ").strip()
            if not url:
                print("❌ URL é obrigatória!")
                continue
            
            username = input("Nome de usuário: ").strip()
            if not username:
                print("❌ Nome de usuário é obrigatório!")
                continue
            
            password = input("Senha: ").strip()
            if not password:
                print("❌ Senha é obrigatória!")
                continue
            
            # Campos opcionais para casos específicos
            print("\n--- Campos opcionais (deixe em branco para detecção automática) ---")
            username_field_id = input("ID do campo usuário (opcional): ").strip() or None
            password_field_id = input("ID do campo senha (opcional): ").strip() or None
            login_button_id = input("ID do botão login (opcional): ").strip() or None
            
            # Tenta fazer o login
            sucesso = login_system.fazer_login(
                url, username, password, 
                username_field_id, password_field_id, login_button_id
            )
            
            if sucesso:
                print("\n🎉 Login realizado com sucesso!")
            else:
                print("\n⚠️ Login não foi bem-sucedido. Verifique as credenciais e tente novamente.")
            
            # Pergunta se quer continuar
            continuar = input("\nDeseja fazer outro login? (s/n): ").strip().lower()
            if continuar not in ['s', 'sim', 'y', 'yes']:
                break
    
    except KeyboardInterrupt:
        print("\n\nPrograma interrompido pelo usuário.")
    
    finally:
        # Fecha o navegador
        print("\nFechando o programa...")
        login_system.fechar_navegador()

if __name__ == "__main__":
    main()
