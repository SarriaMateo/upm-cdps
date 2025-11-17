# Gestión Automatizada de Máquinas Virtuales
**Práctica de la asignatura Centros de Datos y Provisión de Servicios (CDPS)**

Este proyecto implementa una herramienta en Python para la creación, despliegue, gestión y destrucción de una infraestructura virtual utilizada en el laboratorio de CDPS. El sistema permite automatizar la provisión de máquinas virtuales, redes virtuales y servicios asociados mediante un único punto de control.

El script principal, `manage-p2.py`, trabaja junto a:
- `lib_vm.py`, que contiene las clases auxiliares para gestionar máquinas virtuales (VM) y redes (NET).
- `manage-p2.json`, que almacena parámetros de configuración como:
  - Si el modo *debug* está activado.
  - El número de servidores que deben crearse dinámicamente.

---

## Funcionalidad

El programa permite ejecutar varias operaciones principales sobre la infraestructura:

### Crear la infraestructura
- Creación de las máquinas virtuales base:
  - `c1`
  - `lb` (balanceador)
- Creación dinámica de hasta 5 servidores adicionales (`s1`, `s2`, `s3`, …), según el número indicado en `manage-p2.json`.
- Creación de redes virtuales:
  - `LAN1`
  - `LAN2`
- Conexión de cada máquina a su red correspondiente.
- Preparación de las imágenes base necesarias para el entorno.

### Gestión de máquinas: start, stop y destroy
Una vez creada la infraestructura, las operaciones se realizan sobre máquinas específicas o sobre todas a la vez.

**Acción sobre máquinas concretas**:
```
python3 manage-p2.py start c1 lb s1 s3
```

**Acción sobre todas las máquinas**:
```
python3 manage-p2.py stop
```

Las órdenes disponibles son: 
- `create`
- `start`
- `stop`
- `destroy`

---

## Archivos necesarios en la carpeta

Para que el programa funcione correctamente, es obligatorio añadir en el directorio del proyecto los siguientes archivos del laboratorio CDPS:

- `cdps-vm-base-pc1.qcow2`
- `plantilla-vm-pc1.xml`

Estos archivos no están incluidos porque pertenecen al material docente del laboratorio.

---

## Estructura del repositorio

```
/
├── manage-p2.py              # Script principal de gestión de la infraestructura
├── manage-p2.json            # Archivo de configuración del modo debug y número de servidores
├── lib_vm.py                 # Biblioteca auxiliar
├── cdps-vm-base-pc1.qcow2    # (Debe añadirse manualmente)
├── plantilla-vm-pc1.xml      # (Debe añadirse manualmente)
└── README.md
```

---

## Uso del script

### Crear la infraestructura
```
python3 manage-p2.py create
```

### Arrancar máquinas específicas
```
python3 manage-p2.py start c1 lb s1 s3
```

### Arrancar todas las máquinas
```
python3 manage-p2.py start
```

### Detener máquinas específicas
```
python3 manage-p2.py stop s2 s3
```

### Detener todas las máquinas
```
python3 manage-p2.py stop
```

### Destruir máquinas específicas
```
python3 manage-p2.py destroy c1 s1
```

### Destruir toda la infraestructura
```
python3 manage-p2.py destroy
```

---

## Dependencias

- Python 3.x
- Infraestructura de virtualización del laboratorio CDPS
- Archivo `lib_vm.py` con las clases `VM` y `NET`
- Archivos:
  - `cdps-vm-base-pc1.qcow2`
  - `plantilla-vm-pc1.xml`
- Módulos estándar de Python:
  - subprocess
  - logging
  - sys
  - json

---

## Autores

- Mateo Sarria Franco de Sarabia
- Rafael Bueno Castro
- Jacobo España-Heredia Beteta
