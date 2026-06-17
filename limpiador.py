import os
import shutil

ruta_descarga = os.path.join(os.path.expanduser("~"), "Downloads")

clasificacion = {
    "Documentos": [".pdf", ".docx", ".txt", ".xlsx"],
    "Imagenes": [".jpg", ".jpeg", ".png", ".gif"],
    "Comprimidos":[".zip", ".rar", ".7z"],
    "Cuarentena_Seguridad":[".exe", ".bat", ".sh", ".msi"]
}

def organizar_descargas():
    print(f"Iniciando escaneo en: {ruta_descarga}\n")

    archivos = os.listdir(ruta_descarga)

    for archivo in archivos:
        ruta_archivo = os.path.join(ruta_descarga, archivo)

        if os.path.isdir(ruta_archivo):
            continue

        nombre, extension = os.path.splitext(archivo)

        extension = extension.lower()
        
        movido = False

        for carpeta_destino, extensiones_validas in clasificacion.items():
            if extension in extensiones_validas:
                ruta_carpeta= os.path.join(ruta_descarga, carpeta_destino)

                if not os.path.exists(ruta_carpeta):
                    os.makedirs(ruta_carpeta)

                ruta_final = os.path.join(ruta_carpeta, archivo)
                shutil.move(ruta_archivo, ruta_final)
                
                print(f"Movido: {archivo} -> {carpeta_destino}")

                movido = True
                break

            if not movido:
                print(f"Ignorado (extension no registrada): {archivo}")


organizar_descargas()

print("\n¡Limpieza completada!")