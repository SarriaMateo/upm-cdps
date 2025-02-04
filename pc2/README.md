# Segunda Práctica Creativa de CDPS

Los bloques 1, 2 y 3 se realizan desde una instancia VM en Google Cloud. El bloque 4 se lleva a cabo desde la consola de GKE.

## Parte 1: Despliegue de la aplicación en máquina virtual pesada

La idea es desplegar la aplicación como si fuera un monolito en una máquina virtual pesada en Google Cloud. Para ello, hemos creado el script `bloque1.py` dentro de la carpeta `Bloque1`.

Para probarlo, hemos creado una MV en Google Cloud y abierto su consola SSH en un nuevo navegador. Además, hemos instalado `git` para poder clonar la carpeta con los scripts. A continuación, nos cambiamos al directorio de la carpeta de esta parte (`pc2/Bloque1`).

Ejecutamos el script con el comando:

```bash
python3 bloque1.py
```

Este script:
- Clona la carpeta `practica_creativa2` del GitHub de la asignatura (`https://github.com/CDPS-ETSIT/practica_creativa2.git`).
- Instala `python` y `pip` en la máquina virtual.
- Modifica `requirements.txt` e instala las dependencias con `pip3`.
- Crea la variable de entorno `GROUP_NUMBER` y le asigna nuestro número de grupo (`37`).
- Modifica `productpage.html` para cambiar el título de la app por la variable de entorno.
- Llama a `productpage_monolith.py` (script de la app) con el puerto `9080`.

A continuación, introducimos en el navegador la IP pública de la instancia (MV) con el puerto `9080`: `http://<ip-publica>:9080/productpage`, obteniendo el resultado esperado.

![part1](https://user-images.githubusercontent.com/99333138/215883219-1bb003a2-832d-484c-8e55-79cff79fae8a.png)

Como podemos observar, la conexión se establece correctamente y el título de la aplicación es `37`. Dicha aplicación está compuesta por dos servicios: uno para la página de productos (`productpage`) y otro para la descripción de los productos (`details`).

---

## Parte 2: Despliegue de una aplicación monolítica usando Docker

Ahora se quiere desplegar la misma aplicación monolítica pero usando Docker. Para ello, hemos creado el script `bloque2.py`  dentro de la carpeta `Bloque2`, que automatiza la creación de las imágenes y contenedores Docker. Además, se incluyen:
- El fichero `Dockerfile`.
- Un script que se ejecuta al crear la imagen Docker (`rename.py`).
- Un script `delete.py` que eliminará los contenedores e imágenes creadas en Docker.

Para desplegar esta parte, nos situamos en el directorio `pc2/Bloque2` y ejecutamos el script:

```bash
python3 bloque2.py
```

Este script:
- Construye la imagen de Docker `product-page/37`.
- Arranca el contenedor de Docker `productpage-37`.

La imagen (y por consiguiente el contenedor) se construye según el contenido del `Dockerfile`. Este fichero:
- Contiene la variable de entorno `GROUP_NUMBER` con el valor `37`.
- Clona la carpeta `practica_creativa2` del GitHub de la asignatura.
- Instala `python` y `pip` en el contenedor e instala las dependencias con `pip3`.
- Copia y ejecuta el script `rename.py`.
- Expone el puerto `9080`.
- Ejecuta `productpage_monolith.py` con `python3` en el puerto `9080`.

El script `rename.py`:
- Extrae la variable de entorno `GROUP_NUMBER`.
- Modifica `productpage.html` para cambiar el título de la app.
- Modifica `requirements.txt` para corregir las versiones de las dependencias.

El script `delete.py`:
- Borra el contenedor `productpage-37`.
- Borra la imagen `product-page/37`.

Después de haber ejecutado `bloque2.py`, accedemos al navegador con `http://<ip-publica>:9080/productpage`, obteniendo el resultado esperado.

![part2](https://user-images.githubusercontent.com/99333138/215883277-412077cb-b366-459e-833b-5fcb442bd0b2.png)

---

## Parte 3: Segmentación de una aplicación monolítica en microservicios con Docker Compose

Ahora se segmenta la aplicación en microservicios independientes con `docker-compose`. Además de los servicios `productpage` y `details`, se añaden `reviews` y `ratings`.

El script `bloque3.py`, dentro de `Bloque3`, automatiza la creación y lanzamiento de `docker-compose`. También se incluyen:
- `docker-compose.yaml`.
- `Dockerfile` de cada servicio.
- `rename.py` (para `productpage`).
- `delete.py` (para eliminar contenedores e imágenes).

Ejecutamos:

```bash
python3 bloque3.py vX
```

Sustituyendo `vX` por `v1`, `v2` o `v3`.

La construcción de las imágenes de los servicios se realiza mediante sus respectivos Dockerfiles. A continuación, se detalla la configuración de cada uno:

#### Servicio `productpage`
La imagen del servicio `productpage` se construye con su Dockerfile, que hace uso del script `rename.py`. Ambos archivos están ubicados en la carpeta `productPage`. 

Estos archivos son iguales a los utilizados en el Bloque 2, salvo que ya no se ejecuta `productpage_monolith.py`, sino `productpage.py`.

#### Servicio `details`
La imagen del servicio `details` se construye con su Dockerfile, que:
- Copia el archivo `details.rb` en la ruta `/opt/microservices/` dentro del contenedor.
- Define dos variables de entorno:
  - `SERVICE_VERSION` con el valor `v1`.
  - `ENABLE_EXTERNAL_BOOK_SERVICE` con el valor `true`.
- Expone el puerto `9080`, a través del cual se accede al servicio.
- Ejecuta `details.rb` con Ruby en el puerto `9080`, tras haber inicializado el contenedor.

#### Servicio `ratings`
La imagen del servicio `ratings` se construye con su Dockerfile, que:
- Copia los archivos `package.json` y `ratings.js` en la ruta `/opt/microservices/` dentro del contenedor.
- Define la variable de entorno `SERVICE_VERSION` con el valor `v1`.
- Instala las dependencias especificadas en `package.json` mediante `npm install`.
- Expone el puerto `9080`, a través del cual se accede al servicio.
- Ejecuta `ratings.js` con Node.js en el puerto `9080`, tras haber inicializado el contenedor.

#### Servicio `reviews`
La imagen del servicio `reviews` se construye con su Dockerfile ubicado en la ruta `practica_creativa2/bookinfo/src/reviews/reviews-wlpcfg`. La construcción se realiza ejecutando el siguiente comando:
```bash
docker run --rm -u root -v "$(pwd)":/home/gradle/project -w /home/gradle/project gradle:4.8.1 gradle clean build
```

#### Configuración en `docker-compose.yaml`
El fichero `docker-compose.yaml` establece para cada servicio:
- La imagen que se utilizará para crear el contenedor.
- El nombre del contenedor que se creará.
- Las variables de entorno definidas en su Dockerfile con sus valores correspondientes.
- En el caso del servicio `productpage`, los puertos `9080:9080`.
- Las dependencias entre servicios:
  - `details` y `reviews` dependen de `productpage`.
  - `ratings` depende de `reviews`.


Después de ejecutar `bloque3.py`, accedemos al navegador con `http://<ip-publica>:9080/productpage`.

**Versiones:**
- **v1** ![part3-v1](https://user-images.githubusercontent.com/99333138/215883363-24619338-15b2-41d1-a586-bf355789b8ed.png)
- **v2** ![part3-v2](https://user-images.githubusercontent.com/99333138/215883431-93dec63c-eb26-40ff-b974-45d11d7b507f.png)
- **v3** ![part3-v3](https://user-images.githubusercontent.com/99333138/215883477-f06f351b-06e2-471c-8549-cddf7dbb4c84.png)

---

## Parte 4: Despliegue de una aplicación basada en microservicios utilizando Kubernetes

Ahora se despliega la aplicación con Kubernetes en lugar de `docker-compose`.

El script `bloque4.py`, dentro de `Bloque4`, automatiza la creación y lanzamiento de los servicios con Kubernetes. También se incluye el script `delete.py` (para eliminar pods y servicios) y los ficheros YAML en sus correspondientes directorios:
- `productpage.yaml`
- `details.yaml`
- `ratings.yaml`
- `reviews-service.yaml`
- `reviews-v1-deployment.yaml`, `reviews-v2-deployment.yaml`, `reviews-v3-deployment.yaml`

Las imágenes están subidas a Docker Hub bajo `mateosarria/pc2:<servicio>`. Luego, creamos un clúster GKE con 3 nodos, nos conectamos desde Google Shell y ejecutamos:

```bash
python3 bloque3.py vX
```

Sustituyendo `vX` por `v1`, `v2` o `v3`.

Después de ejecutar el script, obtenemos la ip pública de `productpage-external` ejecutando:
```bash
kubectl get services
```
Accedemos al navegador con `http://<ip-publica>:9080/productpage`.

**Versiones:**
- **v1** ![part4-v1](https://user-images.githubusercontent.com/99333138/215883363-24619338-15b2-41d1-a586-bf355789b8ed.png)
- **v2** ![part4-v2](https://user-images.githubusercontent.com/99333138/215883431-93dec63c-eb26-40ff-b974-45d11d7b507f.png)
- **v3** ![part4-v3](https://user-images.githubusercontent.com/99333138/215883477-f06f351b-06e2-471c-8549-cddf7dbb4c84.png)