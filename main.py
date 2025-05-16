import os
import requests
import time
import socket
from dotenv import load_dotenv
from mcstatus.server import JavaServer
from telegram import Update, InputMediaPhoto
from telegram.ext import Application, CommandHandler, CallbackContext

# Cargar las variables de entorno del archivo .env
load_dotenv()
# Obtener las variables de entorno
TOKEN = os.getenv("TOKEN")
IP_LOCAL = os.getenv("IP_LOCAL")
PORT = os.getenv("PORT")
CHAT_ID = os.getenv("CHAT_ID")
USE_LOCAL = os.getenv("USE_LOCAL", "False")  # Default a "False" si no está definida

# Parsea valores
CHAT_ID = int(CHAT_ID)
USE_LOCAL = USE_LOCAL.lower() == "true"

# Ahora USE_LOCAL será un valor booleano
print(USE_LOCAL)

# Obtener la IP pública
def obtener_ip():
    return requests.get("https://api.ipify.org").text

# Comando para enviar la IP actual
async def ip(update: Update, context: CallbackContext):
    ip = obtener_ip()
    await update.message.reply_text(f"Tu IP actual es: {ip}:25566")

# Enviar la IP de manera automática cada día
async def enviar_ip_diaria(context: CallbackContext):
    ip = obtener_ip()
    chat_id = context.job.context['chat_id']
    await context.bot.send_message(chat_id=chat_id, text=f"IP diaria actualizada: {ip+":25565"}")

# Comando /start
async def start(update: Update, context: CallbackContext):
    user = update.message.from_user
    username = user.username
    print(username)

    welcome_message = f"""
    ¡Hola {username}! Soy tu bot del servidor de Minecraft. 😄
    Mi función principal es proporcionarte la IP actualizada de tu servidor y verificar su estado. Aquí tienes una lista de los comandos disponibles:

    🔹 **/ip**  
    Obtén la **IP actualizada** de tu servidor de Minecraft.

    🔹 **/checkServer**  
    Verifica el **estado del servidor** y te indicaré si está activo o no.

    🌍 Estoy aquí para ayudarte a mantener todo funcionando correctamente. Si necesitas algo más, no dudes en preguntar. ¡Que disfrutes jugando! 🎮
    """
    
    await update.message.reply_text(welcome_message, parse_mode="Markdown")


    # context.job_queue.run_daily(enviar_ip_diaria, time=time.time(), context={'chat_id': chat_id})
    
    # print(IP_LOCAL+":"+PORT)
async def status_internal_server(update: Update, context: CallbackContext):
    # Definir el puerto directamente
    ip_servidor = IP_LOCAL  # Cambia la IP local según tu configuración
    puerto = PORT  # Puerto por defecto de Minecraft (puedes cambiarlo si es necesario)
    
    # Usar MCServer.lookup con la IP y el puerto especificado
    server = JavaServer.lookup(f"{ip_servidor}")

     # Obtener el estado del servidor
    try:
        status = server.status()  # Asegúrate de llamar a status correctamente
        players = status.players.sample  # Obtener la lista de jugadores conectados
        player_names = [player.name for player in players] # Extraer el nombre de cada jugador
        # uuids = [player.id for player in players] # Extraer el UUID de cada jugador
        await update.message.reply_text(f"Jugadores conectados: {', '.join(player_names)}")
        media = []
        for player in players:
            link = ""
            if len(players) < 1:
                link = f"https://crafatar.com/avatars/{player.id}?&overlay&size=100"
            else:
                link = f"https://crafatar.com/avatars/{player.id}?&overlay"
            response = requests.get(link)
            if response.status_code == 200:
                # Enviar la imagen al usuario
                media.append(InputMediaPhoto(response.content))
                # await update.message.reply_text(f"{player.name}")
                # await update.message.reply_photo(photo=response.content) 
            # Enviar la lista de jugadores al usuario
            # await update.message.reply_text(f"Jugadores conectados: {', '.join(player_names)}")
        
        if media:
            await update.message.reply_media_group(media=media)
             
        
        # await update.message.reply_text(f"Jugadores conectados: {', '.join(player_names)}")
    except Exception as e:
        await update.message.reply_text("No se pudo obtener el estado del servidor.")
        print(f"Error: {e}")
        
async def getSkin(update: Update, context: CallbackContext):
    # response = requests.get("https://crafatar.com/renders/body/6442e378-f659-478e-b94d-1590fe7b8b0c?&overlay&scale=2")
    response = requests.get("https://crafatar.com/avatars/6442e378-f659-478e-b94d-1590fe7b8b0c?&overlay")
    # print(skin)
    if response.status_code == 200:
        # Enviar la imagen al usuario
        await update.message.reply_photo(photo=response.content)
    else:
        await update.message.reply_text("No se pudo obtener la skin.")
    
async def check_server(update: Update, context: CallbackContext):
    ip_servidor = ""
    if USE_LOCAL:
        ip_servidor = IP_LOCAL 
        print(ip_servidor)
    else:
        ip_servidor = obtener_ip()
        print(ip_servidor)
        
    puerto = PORT

    try:
        # Intentar conectarse al servidor
        with socket.create_connection((ip_servidor, puerto), timeout=5):
            status_message = f"¡El servidor de Minecraft está activo y funcionando en el puerto {PORT}!"
    except (socket.timeout, socket.error):
        status_message = f"El servidor de Minecraft no está respondiendo en el puerto {PORT}. Puede que esté apagado o haya un problema de red, notifica al mediocre del administrador con: /notifyStatus"

    # Enviar el mensaje de estado
    await update.message.reply_text(status_message)

# Función para enviar el estado a un usuario específico
async def notify_status(update: Update, context: CallbackContext):
    ip_servidor = ""
    if USE_LOCAL:
        ip_servidor = IP_LOCAL 
        print(ip_servidor)
    else:
        ip_servidor = obtener_ip()
        print(ip_servidor)
    puerto = PORT

    try:
        # Intentar conectarse al servidor
        with socket.create_connection((ip_servidor, puerto), timeout=5):
            status_message = f"¡El servidor de Minecraft está activo y funcionando en el puerto {PORT}!"
    except (socket.timeout, socket.error):
        status_message = f"El servidor de Minecraft no está respondiendo en el puerto {PORT}. Puede que esté apagado o haya un problema de red."

    # Enviar el mensaje a un chat_id específico
    await context.bot.send_message(chat_id=CHAT_ID, text=status_message)
    await update.message.reply_text("Notificación enviada al administrador mediocre correctamente.")
    
async def jourada(update: Update, context: CallbackContext):
    # Ruta del archivo de la imagen
    image_path = "img/sticker.webp"
    
    # Enviar la imagen al usuario
    await update.message.reply_photo(photo=open(image_path, 'rb'))
 

def main():


    # Crea la aplicación
    application = Application.builder().token(TOKEN).build()

    # Registra los comandos
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("ip", ip))
    application.add_handler(CommandHandler("checkServer", check_server))
    application.add_handler(CommandHandler("notifyStatus", notify_status))
    application.add_handler(CommandHandler("listPlayers", status_internal_server))
    application.add_handler(CommandHandler("jourada", jourada))
    application.add_handler(CommandHandler("getSkin", getSkin))


    # Inicia el bot
    application.run_polling()
    
    if KeyboardInterrupt:
        print("\Bot detenido por el usuario")

if __name__ == '__main__':
    main()





