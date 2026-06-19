import os
import shutil
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


#Definimos las rutas que utilizaremos 
ruta_descargas = os.path.join(os.path.expanduser("~"), "Downloads") #Ruta descargas para mirar
ruta_documentos = os.path.join(os.path.expanduser("~"), "Documents") #Ruta documentos para guardar los archivos que hay en descarga 

#Clasificamos las extensiones que vamos a mirar para poder organizar
clasificacion = {
    "Documentos": [".pdf", ".docx", ".txt", ".xlsx"],
    "Imagenes": [".jpg", ".jpeg", ".png", ".gif"],
    "Comprimidos": [".zip", ".rar", ".7z"],
    "Cuarentena_Seguridad": [".exe", ".bat", ".sh", ".msi"]
}


#Creamos la funcion mover_archivo
def mover_archivo(ruta_archivo_nuevo):
    nombre, extension = os.path.splitext(ruta_archivo_nuevo) #Nos separa el nombre del archivo de la extension
    extension = extension.lower()

    #Hacemos un bucle para poder revisar si las extensiones estan dentro lo previsto
    for carpeta_destino, extensiones_validas in clasificacion.items():
        if extension in extensiones_validas:
            #en caso de que la extension exista la movemos hacia la carpeta de destino
            ruta_carpeta = os.path.join(ruta_documentos, carpeta_destino)
            #Si la carpeta destino no existe la creamos
            if not os.path.exists(ruta_carpeta):
                os.makedirs(ruta_carpeta)
              
            nombre_archivo = os.path.basename(ruta_archivo_nuevo)#Cogemos unicamente el nombre del archivo  
            ruta_final = os.path.join(ruta_carpeta, nombre_archivo)#Para poder mover el archivo cogemos la ruta de la carpeta + el nombre del archivo 
            
            time.sleep(1) #Le damos tiempo para que le tiempo a descargar
            
            try:
                shutil.move(ruta_archivo_nuevo, ruta_final) #intentamos mover el archivo
                print(f"✅ Movido: {nombre_archivo} -> {carpeta_destino}")
            except Exception as e:
                print(f"⚠️ Error al mover {nombre_archivo}: {e}") #si no se puede salta un error
            break

def organizar_descargas_existentes():
    #Revisamos el directorio de 'Descargas' 
    print("🧹 Escaneando archivos antiguos en Descargas...")
    archivos = os.listdir(ruta_descargas)
    
    for archivo in archivos:
        ruta_archivo = os.path.join(ruta_descargas, archivo) #sacamos la ruta del archivo
        
        if os.path.isfile(ruta_archivo):
            mover_archivo(ruta_archivo)#si es un archivo lo llebamos a la funcion anterior (mover_archivo)
            
    print("✨ Limpieza inicial completada.\n")#Lanzamos el mensaje de que ha acabado
class GestorDescargas(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            mover_archivo(event.src_path)#si no es un directorio lo enviamos la ruta hacia la funcion mover_archivo


#Esto se activa si ejecutamos el archivo
if __name__ == "__main__":
    organizar_descargas_existentes()#Primero miramos si hay algo en descargas

    #Damos instrucciones al usuario
    print(f"👁️ Iniciando vigilancia continua en: {ruta_descargas}")
    print("Pulsa 'Ctrl + C' en la terminal para detenerlo.\n")
    
    event_handler = GestorDescargas()
    observer = Observer()
    observer.schedule(event_handler, ruta_descargas, recursive=False)#
    
    observer.start()#Empezamos a vigilar
    
    try:
        while True:
            time.sleep(1) 
    except KeyboardInterrupt:#si hacemos Ctrl + c 
        observer.stop() #paramos la vigilancia
        print("\n🛑 Vigilancia terminada.")
    
    observer.join()#Esperamos a que el proceso en segundo plano se cierre limpiamente.
