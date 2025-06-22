from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from telegram import Bot
import time

# CONFIG
URL = "https://www.citaconsular.es/es/hosteds/widgetdefault/24dc3ade850068f20d7c19845f023121c"
BOT_TOKEN = "7802510567:AAHcOAeQW53YJE_yWJMkcUURjBn6C9E3JfU"
CHAT_ID = "7619836951"

bot = Bot(token=BOT_TOKEN)

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

try:
    print("🟡 Abriendo sitio...")
    driver.get(URL)
    time.sleep(2)

    # Aceptar popup si aparece
    try:
        WebDriverWait(driver, 5).until(EC.alert_is_present())
        alert = driver.switch_to.alert
        alert.accept()
        print("🟡 Aceptando alerta...")
    except:
        print("🟢 No había alerta.")

    # Esperar a que el botón esté presente
    try:
        continuar = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "idCaptchaButton"))
        )
        continuar.click()
        print("🟢 Botón 'Continuar' clickeado.")
    except:
        print("🔴 Botón no encontrado.")
        bot.send_message(chat_id=CHAT_ID, text="⚠️ No se encontró el botón de continuar (`idCaptchaButton`)")
        driver.quit()
        exit()

    time.sleep(4)

    # Notificación de funcionamiento
    bot.send_message(chat_id=CHAT_ID, text="🔁 Bot ejecutado correctamente. Revisando turnos...")

    # Verificar disponibilidad
    if "No hay horas disponibles" not in driver.page_source:
        bot.send_message(chat_id=CHAT_ID, text="✅ ¡Turno disponible! Revisá: " + URL)

except Exception as e:
    bot.send_message(chat_id=CHAT_ID, text="⚠️ Error al revisar turnos: " + str(e))

finally:
    driver.quit()
