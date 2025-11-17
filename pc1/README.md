# Gestión Automatizada de Máquinas Virtuales
**Práctica de la asignatura Centros de Datos y Provisión de Servicios (CDPS)**

Este proyecto implementa una herramienta en Python para la creación, despliegue y destrucción de una infraestructura virtual sencilla. El objetivo es automatizar la provisión de máquinas virtuales y redes virtuales como parte de un entorno de laboratorio para prácticas de centros de datos.

El script principal, `manage-p2.py`, utiliza una biblioteca auxiliar (`lib_vm.py`) que proporciona las abstracciones necesarias para gestionar máquinas virtuales (VM) y redes virtuales (NET). El resultado es una utilidad simple, reproducible y fácilmente ampliable para prácticas de automatización y despliegue.

---

## Funcionalidad

El programa permite ejecutar tres operaciones principales:

### Crear la infraestructura
- Creación de dos máquinas virtuales:
  - `c1`
  - `lb` (balanceador)
- Creación de dos redes virtuales:
  - `LAN1`
  - `LAN2`
- Asociación de cada máquina a su red correspondiente.
- Preparación de las imágenes base necesarias para el laboratorio.

### Desplegar servicios
- Arranque de todas las máquinas virtuales.
- Ejecución remota de comandos en cada VM.
- Posibilidad de instalar software, copiar archivos o habilitar servicios.
- Configuración de la máquina `lb` como balanceador.

### Destruir la infraestructura
- Apagado y eliminación de las máquinas virtuales.
- Eliminación de las redes virtuales creadas.
- Limpieza completa del entorno.

---

## Estructura del repositorio

```
/
├── manage-p2.py        # Script principal de gestión de la infraestructura
├── lib_vm.py           # Biblioteca con las clases VM y NET (no incluida en este repositorio)
└── README.md
```

---

## Uso del script

El programa se ejecuta desde terminal y acepta un comando principal:

### Crear
```
python3 manage-p2.py create
```

### Desplegar
```
python3 manage-p2.py deploy
```

### Destruir
```
python3 manage-p2.py destroy
```

Modo detallado (debug):
```
python3 manage-p2.py create debug
```

---

## Dependencias

- Python 3.x
- Infraestructura de virtualización utilizada en la asignatura CDPS
- Archivo `lib_vm.py` con las clases `VM` y `NET`
- Módulos estándar de Python:
  - subprocess
  - logging
  - sys

---

## Autores

- Mateo Sarria Franco de Sarabia  
- Rafael Bueno Castro  
- Jacobo España-Heredia Beteta
