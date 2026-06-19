# 🛠️ SysAdmin & Automation Toolkit

Este repositorio contiene una colección de herramientas y scripts de automatización desarrollados en Python. El objetivo final del proyecto es unificar todas estas herramientas independientes bajo una única Interfaz Gráfica de Usuario (GUI) para crear un panel de control integral.

---

## 🚀 Herramientas Disponibles

### 1. 🧹 El Limpiador (`limpiador.py`)
Un servicio en segundo plano (demonio) que monitoriza el sistema de archivos en tiempo real. Organiza automáticamente cualquier archivo nuevo que entra en la carpeta de *Descargas* y lo clasifica en *Documentos* basándose en su extensión.

* **Características principales:**
  * Procesamiento por eventos en tiempo real.
  * Aislamiento de ejecutables (`.exe`, `.bat`) en una carpeta de cuarentena por seguridad.
  * Procesamiento por lotes para limpiar el historial acumulado.
* **Tecnologías utilizadas:** `Python`, `watchdog`, `os`, `shutil`.

### 2. [Próxima herramienta...]
*En desarrollo...*

---
