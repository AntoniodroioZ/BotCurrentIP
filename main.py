import os
import requests
import time
import socket
from dotenv import load_dotenv
from telegram import Update
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackContext, CallbackQueryHandler

# Cargar las variables de entorno del archivo .env
load_dotenv()
# Obtener las variables de entorno
TOKEN = os.getenv("TOKEN")
IP_LOCAL = os.getenv("IP_LOCAL")
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
    await context.bot.send_message(chat_id=chat_id, text=f"IP diaria actualizada: {ip+":25566"}")

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

    🌍 Estoy aquí para ayudarte a mantener todo funcionando correctamente. Si necesitas algo más, no dudes en preguntar (al admin XD). ¡Que disfrutes jugando! 🎮
    """
    keyboard = [
        [InlineKeyboardButton("Comando 1", callback_data='command_1')],
        [InlineKeyboardButton("Comando 2", callback_data='command_2')],
        [InlineKeyboardButton("Comando 3", callback_data='command_3')]
    ]
    # Crear el teclado
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_message = welcome_message
    
    await update.message.reply_text(welcome_message, parse_mode="Markdown", reply_markup=reply_markup)


    # context.job_queue.run_daily(enviar_ip_diaria, time=time.time(), context={'chat_id': chat_id})
    
    # Función para manejar el callback de los botones
async def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    # Aquí manejas los callbacks de los botones
    if query.data == 'command_1':
        await update.message.reply_text("Has seleccionado Comando 1.")
    elif query.data == 'command_2':
        await update.message.reply_text("Has seleccionado Comando 2.")
    elif query.data == 'command_3':
        await update.message.reply_text("Has seleccionado Comando 3.")

async def check_server(update: Update, context: CallbackContext):
    ip_servidor = ""
    if USE_LOCAL:
        ip_servidor = IP_LOCAL 
        print(ip_servidor)
    else:
        ip_servidor = obtener_ip()
        print(ip_servidor)
        
    puerto = 25566

    try:
        # Intentar conectarse al servidor
        with socket.create_connection((ip_servidor, puerto), timeout=5):
            status_message = "¡El servidor de Minecraft está activo y funcionando en el puerto 25566!"
    except (socket.timeout, socket.error):
        status_message = "El servidor de Minecraft no está respondiendo en el puerto 25566. Puede que esté apagado o haya un problema de red, notifica al mediocre del administrador con: /notifyStatus"

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
    puerto = 25566

    try:
        # Intentar conectarse al servidor
        with socket.create_connection((ip_servidor, puerto), timeout=5):
            status_message = "¡El servidor de Minecraft está activo y funcionando en el puerto 25566!"
    except (socket.timeout, socket.error):
        status_message = "El servidor de Minecraft no está respondiendo en el puerto 25566. Puede que esté apagado o haya un problema de red."

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
    application.add_handler(CommandHandler("jourada", jourada))

    # Agregar el manejador de los botones
    application.add_handler(CallbackQueryHandler(button_callback))  
    # Inicia el bot
    application.run_polling()
    
    if KeyboardInterrupt:
        print("\Bot detenido por el usuario")

if __name__ == '__main__':
    main()





