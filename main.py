from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import asyncio
from telegram import Bot

# CONFIG
URL = "https://www.citaconsular.es/es/hosteds/widgetdefault/24dc3ade850068f20d7c19845f023121c"
BOT_TOKEN = "7802510567:AAHcOAeQW53YJE_yWJMkcUURjBn6C9E3JfU"
CHAT_ID = "7619836951"

async def main():
    bot = Bot(token=BOT_TOKEN)

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)

    try:
        print("🟡 Abriendo sitio...")
        driver.get(URL)
        time.sleep(3)

        # Intentamos aceptar alert solo si existe
        try:
            print("🟡 Intentando aceptar alerta (si hay)...")
            alert = driver.switch_to.alert
            alert.accept()
            print("🟢 Alerta aceptada.")
            time.sleep(2)
        except:
            print("🟡 No hay alerta que aceptar.")

        print("🟡 Buscando botón Continuar...")
        continuar = driver.find_element(By.ID, "idCaptchaButton")
        continuar.click()
        time.sleep(5)

        print("🟢 Enviando mensaje: bot funcionando.")
        await bot.send_message(chat_id=CHAT_ID, text="🔁 Bot ejecutado correctamente. Revisando turnos...")

        if "No hay horas disponibles" not in driver.page_source:
            print("🟢 ¡Turnos disponibles!")
            await bot.send_message(chat_id=CHAT_ID, text="✅ ¡Turno disponible! Revisá: " + URL)
        else:
            print("🔒 No hay turnos disponibles.")

    except Exception as e:
        print("🔴 Error:", str(e))
        await bot.send_message(chat_id=CHAT_ID, text="⚠️ Error al revisar turnos: " + str(e))

    finally:
        driver.quit()

# Ejecutar función asíncrona
asyncio.run(main())
