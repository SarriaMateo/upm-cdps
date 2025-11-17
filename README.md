# upm-cdps
**Prácticas de la asignatura Centros de Datos y Provisión de Servicios (CDPS)**

Este repositorio reúne dos proyectos independientes, organizados por carpetas, cada uno enfocado en distintos aspectos de virtualización, automatización y despliegue de aplicaciones en entornos cloud y de contenedores.

## Contenido del repositorio

### pc1 – Automatización de infraestructura virtual con Python

Práctica centrada en la gestión automatizada de máquinas virtuales dentro del entorno docente CDPS.

Incluye un script en Python capaz de:
- Crear, iniciar, detener y destruir máquinas virtuales y redes virtuales
- Configurar dinámicamente el número de servidores a partir de un archivo JSON
- Ejecutar acciones selectivas o globales sobre las VMs
- Gestionar imágenes base y plantillas del laboratorio CDPS

Este proyecto refleja competencias en automatización, gestión de entornos virtualizados y scripting avanzado.

---

### pc2 – Despliegue de aplicaciones: de monolítico a microservicios y Kubernetes

Práctica orientada a la evolución progresiva del despliegue de una aplicación, integrando virtualización, contenedores, orquestación y cloud computing.

Se divide en cuatro bloques, cada uno ejecutado con su propio script en Python:

**Bloque 1 — Despliegue en máquina virtual pesada**
- La aplicación se despliega manualmente en una VM tradicional
- Ejecución desde una instancia en Google Cloud VM

**Bloque 2 — Despliegue de una aplicación monolítica con Docker**
- Empaquetado y despliegue de la misma aplicación en un contenedor Docker
- Ejecutado desde Google Cloud VM

**Bloque 3 — Segmentación en microservicios con Docker Compose**
- La aplicación se divide en servicios independientes y se despliega mediante Docker Compose
- Ejecutado desde Google Cloud VM

**Bloque 4 — Despliegue en Kubernetes (GKE)**
- La aplicación basada en microservicios se despliega y gestiona mediante Google Kubernetes Engine (GKE) desde la consola de Kubernetes

Este proyecto demuestra experiencia práctica en contenedores, microservicios, automatización en cloud y orquestación con Kubernetes.


## Uso del repositorio

Clonar el repositorio:
```
git clone https://github.com/SarriaMateo/upm-cdps.git
```

Cada práctica está encapsulada en su carpeta (`pc1/` y `pc2/`) y contiene sus propios scripts y archivos de apoyo.

Consultar el README específico dentro de cada directorio para instrucciones detalladas.


## Autores
- Mateo Sarria Franco de Sarabia
- Rafael Bueno Castro
- Jacobo España-Heredia Beteta