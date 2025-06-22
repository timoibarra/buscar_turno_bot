from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import telegram

# CONFIG
URL = "https://www.citaconsular.es/es/hosteds/widgetdefault/24dc3ade850068f20d7c19845f023121c"
BOT_TOKEN = "7802510567:AAHcOAeQW53YJE_yWJMkcUURjBn6C9E3JfU"
CHAT_ID = "7619836951"

bot = telegram.Bot(token=BOT_TOKEN)

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

try:
    driver.get(URL)
    time.sleep(3)

    alert = driver.switch_to.alert
    alert.accept()
    time.sleep(2)

    continuar = driver.find_element(By.ID, "idCaptchaButton")
    continuar.click()
    time.sleep(5)

    # Notificación de funcionamiento
    bot.send_message(chat_id=CHAT_ID, text="🔁 Bot ejecutado correctamente. Revisando turnos...")

    # Si hay turnos disponibles
    if "No hay horas disponibles" not in driver.page_source:
        bot.send_message(chat_id=CHAT_ID, text="✅ ¡Turno disponible! Revisá: " + URL)

except Exception as e:
    bot.send_message(chat_id=CHAT_ID, text="⚠️ Error al revisar turnos: " + str(e))

finally:
    driver.quit()
