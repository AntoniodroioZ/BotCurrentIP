import os
import socket
import time
from dotenv import load_dotenv
from datetime import datetime

IP_LOCAL = os.getenv("IP_LOCAL")

def verificar_conexion(ip, puerto, timeout=5):
    """
    Verifica si es posible establecer una conexión con la IP y puerto especificados.
    
    Args:
        ip (str): Dirección IP o nombre de host a verificar
        puerto (int): Puerto a verificar
        timeout (int): Tiempo máximo de espera en segundos (por defecto 5)
    
    Returns:
        bool: True si la conexión fue exitosa, False si falló
    """
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(timeout)
    
    try:
        inicio = time.time()
        resultado = s.connect_ex((ip, puerto))
        tiempo_respuesta = time.time() - inicio
        
        if resultado == 0:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Conexión exitosa a {ip}:{puerto} - Tiempo de respuesta: {tiempo_respuesta:.3f}s")
            return True
        else:
            print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error de conexión a {ip}:{puerto} - Código de error: {resultado}")
            return False
    except socket.timeout:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Timeout al conectar a {ip}:{puerto} (más de {timeout} segundos)")
        return False
    except socket.error as e:
        print(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Error de socket al conectar a {ip}:{puerto} - {str(e)}")
        return False
    finally:
        s.close()

if __name__ == "__main__":
    # Configuración
    IP = IP_LOCAL  # Ejemplo: Google DNS
    PUERTO = 25566      # Puerto DNS común
    # IP = "8.8.8.8"
    # PUERTO = 53
    INTERVALO_VERIFICACION = 10  # Segundos entre verificaciones
    
    print(f"Iniciando monitor de conexión a {IP}:{PUERTO}")
    print(f"Verificando cada {INTERVALO_VERIFICACION} segundos")
    print("Presiona Ctrl+C para detener el script\n")
    
    try:
        while True:
            verificar_conexion(IP, PUERTO)
            time.sleep(INTERVALO_VERIFICACION)
    except KeyboardInterrupt:
        print("\nMonitor detenido por el usuario")