import subprocess
import time
import requests
import telebot
import csv
import threading # <-- NUEVO: Para poder hacer dos cosas a la vez

# ⚠️ Recuerda usar un token nuevo tras el incidente de seguridad anterior
TOKEN = "TU_TOKEN_OCULTO"
CHAT_ID = "1358554744"

bot = telebot.TeleBot(TOKEN)

# --- VARIABLES GLOBALES ---
servidores = {} 
vigilando = False # Interruptor para encender o apagar los pings

# --- (AQUÍ VAN TUS COMANDOS /start y /config IGUAL QUE LOS TENÍAS) ---
@bot.message_handler(commands=['start','ayuda'])
def comando_bienvenida(mensaje):
    texto=(
        "Hola soy el vigia, tu asistente de red.\n\n"
        "Comandos disponibles:\n"
        "·  /config - Permite configurar los servidores mediante un csv.\n"
        "·  /iniciar - Arranca la monitorización en segundo plano.\n"
        "·  /parar - Detiene la monitorización."
    )
    bot.reply_to(mensaje, texto)

@bot.message_handler(commands=['config'])
def activar_modo_configuracion(mensaje):
    texto = "⚙️ **Modo Configuración**\nEnvíame el archivo `.csv` (Formato: Nombre;IP)"
    respuesta = bot.reply_to(mensaje, texto, parse_mode="Markdown")
    bot.register_next_step_handler(respuesta, procesar_csv_servidores)

def procesar_csv_servidores(mensaje):
    try:
        nombre_archivo = mensaje.document.file_name
        if not nombre_archivo.endswith('.csv'):
            bot.reply_to(mensaje, "⛔ Error: Solo acepto archivos .csv")
            return 

        info_archivo = bot.get_file(mensaje.document.file_id)
        archivo_descargado = bot.download_file(info_archivo.file_path)
        
        with open(nombre_archivo, 'wb') as nuevo_archivo:
            nuevo_archivo.write(archivo_descargado)

        servidores.clear() 
        
        with open(nombre_archivo, newline='', encoding='utf-8') as csvfile:
            # Tu CSV usa punto y coma, así que está perfecto
            lector = csv.reader(csvfile, delimiter=';') 
            for fila in lector:
                if len(fila) >= 2:
                    nombre = fila[0].strip() 
                    ip = fila[1].strip()
                    servidores[nombre] = ip # Actualiza la variable global

        bot.send_message(mensaje.chat.id, f"✅ Configuración cargada con éxito. Ahora tengo {len(servidores)} servidores en memoria.")

    except Exception as e:
        bot.reply_to(mensaje, f"⚠️ Error fatal: {e}")

# --- EL MOTOR DE PINGS (Se ejecuta en segundo plano) ---
def motor_de_pings():
    global vigilando # Le decimos que use el interruptor global
    
    while vigilando: # Mientras el interruptor esté en True, repite:
        for nombre, ip in servidores.items():
            print(f"Comprobando {nombre} ({ip})...", end=" ")
            
            if hacer_ping(ip):
                print("OK")
            else:
                print("CAÍDO")
                enviar_alerta(f"🚨 Alerta Crítica\nEl equipo '{nombre}' ({ip}) ha caído.")
                
        print("\nEsperando 10 segundos para el siguiente escaneo...\n")
        time.sleep(10)

# --- COMANDOS DE CONTROL ---
@bot.message_handler(commands=['iniciar'])
def iniciar_vigilancia(mensaje): # <-- ¡SOLO recibe el mensaje!
    global vigilando
    
    # 1. Comprobamos si nos han pasado el CSV antes de arrancar
    if len(servidores) == 0:
        bot.reply_to(mensaje, "⚠️ No hay servidores. Usa el comando /config primero.")
        return
        
    # 2. Comprobamos si ya estaba encendido para no arrancarlo dos veces
    if vigilando:
        bot.reply_to(mensaje, "⚠️ El Vigía ya está haciendo pings actualmente.")
        return

    # 3. Encendemos el interruptor y arrancamos el hilo secundario
    vigilando = True
    bot.reply_to(mensaje, "🛡️ Iniciando El Vigía en segundo plano...")
    enviar_alerta("🟢 El sistema de monitorización 'El Vigía' ha arrancado.")
    
    # MAGIA: Esto ejecuta los pings de forma independiente sin bloquear al bot
    hilo = threading.Thread(target=motor_de_pings)
    hilo.start()

@bot.message_handler(commands=['parar'])
def parar(mensaje):
    global vigilando
    # Apagamos el interruptor (esto romperá el bucle while del motor de pings)
    vigilando = False 
    bot.send_message(mensaje.chat.id, "🛑 Vigía se ha ido a descansar. Monitorización detenida.")

# --- HERRAMIENTAS INTERNAS ---
def enviar_alerta(texto_alerta):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": texto_alerta}
    try:
        requests.post(url, data=payload)
    except Exception as e:
        print (f"Error de conexion con Telegram: {e}")

def hacer_ping(ip):
    comando= ["ping","-n","1",ip]
    resultado= subprocess.run(comando, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return resultado.returncode==0

if __name__ == "__main__":
    print("🤖 Bot listo. Esperando comandos de Telegram...")
    bot.infinity_polling()