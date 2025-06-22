from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import asyncio
from telegram import Bot
import traceback
import time

# CONFIG
URL = "https://www.citaconsular.es/es/hosteds/widgetdefault/24dc3ade850068f20d7c19845f023121c"
BOT_TOKEN = "7802510567:AAHcOAeQW53YJE_yWJMkcUURjBn6C9E3JfU"
CHAT_ID = "7619836951"

bot = Bot(token=BOT_TOKEN)

async def revisar_turnos():
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        print("🟡 Abriendo sitio...")
        driver.get(URL)
        time.sleep(3)

        print("🟡 Aceptando alerta...")
        try:
            alert = driver.switch_to.alert
            alert.accept()
            time.sleep(2)
        except:
            print("🔵 No apareció alerta (posiblemente ya fue aceptada automáticamente)")

        print("🟡 Buscando botón de continuar...")
        try:
            continuar = driver.find_element(By.ID, "idCaptchaButton")
            continuar.click()
            time.sleep(5)
        except:
            await bot.send_message(chat_id=CHAT_ID, text="⚠️ No se encontró el botón de continuar (`idCaptchaButton`)")
            return

        await bot.send_message(chat_id=CHAT_ID, text="🔁 Bot ejecutado correctamente. Revisando turnos...")

        if "No hay horas disponibles" not in driver.page_source:
            await bot.send_message(chat_id=CHAT_ID, text="✅ ¡Turno disponible! Revisá: " + URL)

    except Exception as e:
        error_details = traceback.format_exc()
        print("🔴 Error:", error_details)
        await bot.send_message(chat_id=CHAT_ID, text="⚠️ Error al revisar turnos:\n" + error_details)

    finally:
        driver.quit()

if __name__ == "__main__":
    asyncio.run(revisar_turnos())
