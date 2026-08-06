from biblioteca_protheus import *
import json
import os
import sys
from tratamento_datas import verificar_datas

from datetime import date
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from loop_f import loop_filiais, ajusta_dados_arquivo_inicial
import keyring

# keyring.set_password("Robo_User", "robo", "Abc123!@#")
# NOVO (auto driver)
entrada = sys.stdin.read().strip()
dados = json.loads(entrada)

datas_a_validar = ajusta_dados_arquivo_inicial(dados)
datas_validas = verificar_datas(datas_a_validar)
if all(filial.startswith("-") for filial in dados["Filiais"]):
    print("Erro: Selecione pelo menos uma filial", file=sys.stderr)
    sys.exit(0)

if datas_validas == "Erro: insira uma data" or all(data == "" for data in datas_validas):
    print("Erro: necessario informar uma data valida.", file=sys.stderr)
    sys.exit(0)

senha = keyring.get_password("Robo_User", "robo")
hoje = date.today()
nome_log("bloqueio_datas")

#verifica data retroativa
if hoje.day == 0:
    print("iniciar com data retroativa")
    dia = hoje.day - 1
    mes = hoje.month - 1
    ano = hoje.year
    # se janeiro, volta para dezembro do ano anterior
    if mes == 0:
        mes = 12
        ano -= 1
    nova_data = date(ano, mes, dia)
    print("Mês anterior:", nova_data)
    print("Mês anterior ajustado:", nova_data.strftime("%d%m%Y"))
    DataRetroativa =  nova_data.strftime("%d%m%Y")
    print("Data retroativa: ", DataRetroativa)
    DataRetroativaBool = True
else:
    DataRetroativaBool = None
    DataRetroativa = None
    print("segue normal")
    
# =========================
# CORREÇÃO CRÍTICA (AGENDADOR)
# =========================
if getattr(sys, 'frozen', False):
    base_dir = os.path.dirname(sys.executable)
else:
    base_dir = os.path.dirname(os.path.abspath(__file__))

os.chdir(base_dir)

# DEBUG (pode remover depois)
# with open(os.path.join(base_dir, "debug_path.txt"), "w") as f:
#     f.write(f"Rodando em: {os.getcwd()}")
#
# =========================
# CONFIG
# =========================
homologacao = False
teste = 1

chrome_options = Options()

# =========================
# PERFIL
# =========================
profile_path = os.path.join(base_dir, "chrome_profile")
chrome_options.add_argument(f"--user-data-dir={profile_path}")

# =========================
# MODO EXECUÇÃO
# =========================
if not homologacao and teste == 0:
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--window-size=1920,1080")
    credenciais = ["robo", senha]

elif not homologacao and teste == 1:
    chrome_options.add_argument("--start-maximized")
    credenciais = ["robo", senha]

else:
    chrome_options.add_argument("--start-maximized")
    credenciais = ["gustavo.elicker", "123abc"]

# =========================
# ESTABILIDADE
# =========================
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--remote-debugging-port=9222")

# =========================
# CONFIG EXTRA
# =========================
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--disable-popup-blocking")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-infobars")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--allow-insecure-localhost")
chrome_options.add_argument("--use-fake-ui-for-media-stream")

chrome_options.add_argument(
    "--unsafely-treat-insecure-origin-as-secure=http://protheus.dalba.com.br:1239"
)

# =========================
# PREFS
# =========================
prefs = {
    "profile.default_content_setting_values.notifications": 2
}
chrome_options.add_experimental_option("prefs", prefs)

# =========================
# DRIVER (AUTO + FALLBACK)
# =========================
while True: 
    try:
        # tenta baixar automaticamente
        service = Service(ChromeDriverManager().install())
    except Exception as e:
        print("Erro ao baixar driver automático:", e)
        print("Usando driver local...")

        driver_path = os.path.join(base_dir, "chromedriver.exe")
        service = Service(driver_path)

    driver = webdriver.Chrome(service=service, options=chrome_options)
    wait = WebDriverWait(driver, 20)

# =========================
# INÍCIO DO FLUXO
# =========================


    log("INICIANDO AMBIENTE")
    iniciar_ambiente(homologacao, driver)

    log("CONFIRMANDO BASE")
    if confirmaBase(driver, wait):
        break
    else:    
        driver.quit()
        time.sleep(2)

log("REALIZANDO LOGIN")
login(driver, wait, credenciais)

ambiente = "34"
log(f"SELECIONANDO AMBIENTE {ambiente}")
sel_ambiente(driver, wait, ambiente, homologacao, DataRetroativaBool, DataRetroativa)

menus = ["iscelanea","Dalba","Bloqueio"]
for menu in menus: 
    # Scriptfind(driver,tipo="wa-menu-item")
    funcao_tres_e_demais(driver,"wa-menu-item",menu)

resultado = loop_filiais(driver, dados)
if resultado == "INSIRA UMA DATA EM UMA OPÇÂO": 
    print("enviar email inserir data")


log("FINALIZANDO")
time.sleep(5)
driver.quit()
log("FINALIZADO")
lista_filial_sucesso =[]
lista_filial_sucesso = []

for filial in dados["Filiais"]:
    if len(filial) == 6:
        lista_filial_sucesso.append(filial)

print(f"As datas das filiais:{lista_filial_sucesso} foram alteradas com sucesso", file=sys.stderr)
sys.exit(0)