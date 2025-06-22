from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import telegram
import asyncio

# CONFIG
URL = "https://www.citaconsular.es/es/hosteds/widgetdefault/24dc3ade850068f20d7c19845f023121c"
BOT_TOKEN = "7802510567:AAHcOAeQW53YJE_yWJMkcUURjBn6C9E3JfU"
CHAT_ID = "7619836951"

bot = telegram.Bot(token=BOT_TOKEN)

options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

async def main():
    try:
        print("🟡 Abriendo sitio...")
        driver.get(URL)
        time.sleep(2)  # dejar que cargue el modal

        print("🟡 Esperando botón de continuar...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "idCaptchaButton"))
        )

        continuar = driver.find_element(By.ID, "idCaptchaButton")
        continuar.click()
        print("🟢 Botón clickeado")

        time.sleep(5)  # esperar que cargue siguiente pantalla

        await bot.send_message(chat_id=CHAT_ID, text="🔁 Bot ejecutado correctamente. Revisando turnos...")

        if "No hay horas disponibles" not in driver.page_source:
            await bot.send_message(chat_id=CHAT_ID, text="✅ ¡Turno disponible! Revisá: " + URL)

    except Exception as e:
        print("🔴 Error:", e)
        await bot.send_message(chat_id=CHAT_ID, text="⚠️ Error al revisar turnos: " + str(e))

    finally:
        driver.quit()

asyncio.run(main())
