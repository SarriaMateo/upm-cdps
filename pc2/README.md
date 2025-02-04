# Segunda práctica creativa de CDPS
Los bloques 1, 2 y 3 se realizan desde una instancia VM en Google Cloud. El bloque 4 se lleva a cabo desde la consola de GKE.

## Parte 1: Despliegue de la aplicación en máquina virtual pesada
La idea es desplegar la aplicación como si fuera un monolito en una máquina virtual pesada en Google Cloud. Para ello, hemos creado el script `bloque1.py` entregado en el zip, dentro de la carpeta `Bloque1`.

Para probarlo, hemos creado una MV en Google Cloud y abierto su consola SSH en un nuevo navegador. Además, hemos instalado git para poder clonar la carpeta con los scripts. A continuación, nos cambiamos al directorio de la carpeta de esta parte (`pc2/Bloque1`).

Ejecutamos el script con el comando
```
python3 bloque1.py
```
Este script:
- Clona la carpeta `practica_creativa2` del github de la asignatura (`https://github.com/CDPS-ETSIT/practica_creativa2.git`)
- Instala pyhton y pip en la maquina virtual
- Modifica `requirements.txt` e instala las dependencias con pip3
- Crea la variable de entorno `GROUP_NUMBER` y le asigna nuestro número de grupo (37)
- Modifica el `productpage.html` para cambiar el título de la app por la variable de entorno
- Llama a `productpage_monolith.py` (script de la app) con el puerto `9080`

A continuación, introducimos en el navegador la ip pública de la instancia (MV) con el puerto `9080`: `http://<ip-publica>:9080/productpage` obteniendo el resultado esperado.
  
<img width="1440" alt="part1" src="https://user-images.githubusercontent.com/99333138/215883219-1bb003a2-832d-484c-8e55-79cff79fae8a.png">

Como podemos observar, la conexión se establece correctamente y el título de la aplicación es 37. Dicha aplicación está compuesta por dos servicios: uno para la página de productos (`productpage`) y otro para la descripción de los productos (`details`).


## Parte 2: Despliegue de una aplicación monolítica usando docker

Ahora se quiere desplegar la misma aplicación monolítica pero usando docker. Para ello, hemos creado el script `bloque2.py` entregado en el zip, dentro de la carpeta `Bloque2`, que automatiza la creación de las imágenes y contenedores docker. Además de, lógicamente, el fichero `Dockerfile`, un script que se ejecuta al crear la imagen docker (se hace run desde el Dockerfile) llamado `rename.py` y un script `delete.py` que eliminará los contenedores e imágenes creadas de docker.

Para desplegar esta parte, nos situamos en el directorio `pc2/Bloque2` y ejecutamos el script:
```
pyhton3 bloque2.py
```
Este script:
- Construye la imagen de docker `product-page/37`
- Arranca el contenedor de docker `productpage-37`

La imagen (y por consiguiente el contenedor) se construye según el contenido del `Dockerfile`. Este fichero:
- Contiene la variable de entorno `GROUP_NUMBER` que es nuestro número de grupo (37)
- Clona la carpeta `practica_creativa2` del github de la asignatura (`https://github.com/CDPS-ETSIT/practica_creativa2.git`)
- Instala pyhton y pip en el contenedor e instala las dependencias con pip3
- Copia y ejecuta el script `rename.py` para la imagen durante su proceso de construcción
- Expone el puerto `9080` a través del cual se va a acceder al servicio
- Ejecuta con python3 `productpage_monolith.py` (script de la app) con el puerto `9080` tras haber inicializado el contenedor

El script `rename.py` mencionado, que se utiliza para crear la imagen del contenedor. Este script:
- Extrae la variable de entorno `GROUP_NUMBER` creado en el Dockerfile
- Modifica `productpage.html` para cambiar el título de la app por la variable de entorno
- Modifica `requierements.txt` para corrgir las versiones de las dependencias

El script `delete.py`:
- Borra el contenedor creado `productpage-37`
- Borra la imagen creada `product-page/37`
	

Despues de haber ejecutado `bloque2.py`, introducimos en el navegador la ip pública de la instancia (MV) con el puerto introducido: `http://<ip-publica>:9080/productpage` obteniendo el resultado esperado.

<img width="1440" alt="part2" src="https://user-images.githubusercontent.com/99333138/215883277-412077cb-b366-459e-833b-5fcb442bd0b2.png">

Como podemos observar, la conexión se establece correctamente y el título de la aplicación es 37. Dicha aplicación está compuesta por dos servicios: uno para la página de productos (`productpage`) y otro para la descripción de los productos (`details`).

## Parte 3: Segmentación de una aplicación monolítica en microservicios utilizando docker-compose

Ahora se va a segmentar la aplicación, es decir, se va a separar cada servicio para que funcione de forma independiente usando docker-compose. Además de los servicios que teníamos anteriormente, `productpage` y `details`, se van a añadir dos más: `reviews` y `ratings`. Para ello, hemos creado el script `bloque3.py` entregado en el zip, dentro de la carpeta `Bloque3`, que automatiza la creación y lanzamiento de docker-compose. Además de, lógicamente, el fichero `docker-compose.yaml` y los ficheros `Dockerfile` de cada servicio (contenidos respectivamente en las carpetas con sus nombres de servicio, excepto `reviews`, que se cogerá directamente de la `practica_creativa2`), un script dentro de la carpeta `productPage` que se ejecuta al crear la imagen docker para el servicio productpage (se hace run desde el Dockerfile de `productpage`) llamado `rename.py`, exactamente igual que el utilizado en la parte 2, y un script `delete.py` que eliminará los contenedores e imágenes de docker creadas, (una vez que ha sido lanzada la aplicación con `bloque3.py`).

Para desplegar esta parte, nos situamos en el directorio `pc2/Bloque3` y ejecutamos el script `bloque3.py` seguido de la versión que queremos desplegar (v1, v2 o v3):
```
pyhton3 bloque3.py vX
```
Este script:
- Clona la carpeta `practica_creativa2` del github de la asignatura (`https://github.com/CDPS-ETSIT/practica_creativa2.git`)
- Copia los ficheros `details.rb` (de la carpeta `details` de `practica_creativa2`), `ratings.js` y `package.json` (de `ratings`) para almacenarlos en nuestras carpetas respectivas en `Bloque3` junto al Dockerfile correspondiente.
- Compila y empaqueta los paquetes de la carpeta `reviews` (dentro de `practica_creativa2`)
- Modifica el `docker-compose.yaml` para cambiar las variables de entorno de reviews según la versión elegida
- Construye las imágenes con docker-compose y arranca los contenedores del docker-compose y lanza la aplicación con todos los servicios

En caso de introducir una version inválida (que no sea v1, v2 o v3) sale del script y no se ejecuta nuestra aplicación, habría que volver a ejecutar el script introduciendo una versión válida.

La imagen del servicio productpage se construye con su Dockerfile que hace uso del script `rename.py`, ambos ficheros están en la carpeta `productPage`. Ambos son iguales que en el Bloque 2, salvo que ya no se ejecuta `productpage_monolith.py`, sino `productpage.py`.

La imagen del servicio `details` se construye con su Dockerfile:
- Copia el fichero `details.rb` en la ruta `/opt/microservices/` dentro del contenedor
- Tiene dos variables de entorno: `SERVICE_VERSION` con valor v1 y `ENABLE_EXTERNAL_BOOK_SERVICE con valor true
- Expone el puerto `9080` a través del cual se va a acceder al servicio
- Ejecuta con Ruby `details.rb` (código del servicio `details`) con el puerto `9080` tras haber inicializado el contenedor


La imagen del servicio 'ratings' se construye con su Dockerfile:
- Copia los ficheros `package.json` y `ratings.js` en la ruta `/opt/microservices/` dentro del contenedor
- Tiene la variable de entorno: `SERVICE_VERSION` con valor v1
- Instala las dependencias del json con `npm install`
- Expone el puerto `9080` a través del cual se va a acceder al servicio
- Ejecuta con node `ratings.js` (código del servicio `ratings`) con el puerto `9080` tras haber inicializado el contenedor

La imagen del servicio `reviews` se construye con su Dockerfile dado en la ruta `practica_creativa2/bookinfo/src/reviews/reviews-wlpcfg` ejecutando el siguiente comando:
```
docker run --rm -u root -v "$(pwd)":/home/gradle/project -w /home/gradle/project gradle:4.8.1 gradle clean build
```

El fichero `docker-compose.yaml` establece para cada servicio:
- La imagen que se va a utilizar para crear el contenedor
- El nombre del contenedor que se va a crear
- Las variables de entorno definidas en su Dockerfile con sus valores correspondientes
- En el caso del servicio de `productpage`, los puertos `9080:9080`. Para el resto de servicios, las dependencias (`details` y `reviews` son hijos de `productpage` y `ratings` es hijo de `reviews`)

El script `delete.py`:
- Borra los contenedores creados a partir de docker-compose
- Borra las imágenes creadas (`reviews/37`, `ratings/37`, `details/37`, `productpage/37`)

Despues de haber ejecutado `bloque3.py`, introducimos en el navegador la ip pública de la instancia (MV) con el puerto introducido: `http://<ip-publica>:9080/productpage` obteniendo el resultado esperado.

Seleccionando v1:
<img width="1440" alt="part3-v1" src="https://user-images.githubusercontent.com/99333138/215883363-24619338-15b2-41d1-a586-bf355789b8ed.png">

Seleccionando v2:
<img width="1440" alt="part3-v2" src="https://user-images.githubusercontent.com/99333138/215883431-93dec63c-eb26-40ff-b974-45d11d7b507f.png">

Seleccionando v3:
<img width="1440" alt="part3-v3" src="https://user-images.githubusercontent.com/99333138/215883477-f06f351b-06e2-471c-8549-cddf7dbb4c84.png">

Como podemos observar, la conexión se establece correctamente y el título de la aplicación es 37. Dicha aplicación está compuesta por cuatro servicios: uno para la página de productos (`productpage`) y otro para la descripción de los productos (`details`), uno para las críticas (`ratings`) y otro para las valoraciones (`reviews`).

## Parte 4: Despliegue de una aplicación basada en microservicios utilizando Kubernetes

Ahora se pide desplegar la misma aplicación basada en microservicios pero utilizando Kubernetes, no docker-compose. Para ello, hemos creado el script `bloque4.py` entregado en el zip, dentro de la carpeta `Bloque4`, que automatiza la creación y lanzamiento de los servicios con Kubernetes. Además de, lógicamente, los ficheros yaml que definen los servicios de la aplicación `productpage.yaml` (dentro de la carpeta `productPage`), `details.yaml` (dentro de la carpeta `details`), `ratings.yaml` (dentro de la caeta `ratings`) y para el caso del servicio `reviews` tenemos la definición del servicio `reviews-service.yaml`, y los despliegues para las distintas versiones `reviews-v1-deployment.yaml`, `reviews-v2-deployment.yaml` y `reviews-v3-deployment.yaml` (todos ellos dentro de la carpeta `reviews`). Por último un script `delete.py` que eliminará los pods (y servicios) de Kubernetes, (una vez que ha sido lanzada la aplicación con `bloque4.py`).

Creamos las imágenes de `productpage`, `details`, `ratings` y las de cada versión de `reviews` y las subimos a nuestro repositorio de Docker-hub: `mateosarria/pc2`. Las imágenes siguen una nomenclatura de tipo `mateosarria/pc2:(servicio)` por ejemplo para `productpage`: `mateosarria/pc2:productpage`, para la versión 1 de `reviews`: `mateosarria/pc2:reviews-v1`, (indicado en los ficheros .yaml correspondientes).

Para desplegarlo, creamos un clúster de Kubernetes en Google Cloud (GKE), de modo que se creen 3 nodos. Nos conectamos al clúster a través de la Google Shell y clonamos la carpeta con los scripts. A continuación nos situamos en el directorio `pc2/Bloque4` y ejecutamos el script `bloque4.py` seguido de la versión que queremos desplegar (v1, v2 o v3):
```
pyhton3 bloque4.py v_
```
Este script:
- Construye los servicios de Kubernetes ejecutando los siguientes comandos:
```
kubectl apply -f productPage/productpage.yaml
kubectl apply -f details/details.yaml
kubectl apply -f ratings/ratings.yaml
kubectl apply -f reviews/reviews-svc.yaml
kubectl apply -f reviews/reviews-vX-deployment.yaml #En función de la version vX elegida
```
En caso de introducir una version inválida (que no sea v1, v2 o v3) sale del script y no se ejecuta nuestra aplicación, habría que volver a ejecutar el script introduciendo una versión válida.

Los ficheros `ratings.yaml` y los de reviews, `reviews-svc.yaml` y `reviews-vX-deployment.yaml` (X = 1, 2 o 3 para cada versión), vienen dados como ejemplo en `practica_creativa2/bookinfo/platform`, solo cambiamos el nombre de la imagen correspondiente subida al Docker-hub (como se explicó anteriormente).

El fichero `details.yaml` es como el anterior `ratings.yaml` pero cambiando los nombres por `details`.

El fichero `productpage.yaml` añade un servicio (`productpage-external`) de tipo LoadBalancer para poder acceder a la aplicación por medio de una IP externa.
	
El script `delete.py`:
- Borra los pods y servicios de Kubernetes creados, por ejemplo: `kubectl delete -f details/details.yaml`, así para todos los posibles (sin diferenciar la versión que está corriendo de reviews)

A continuación de haber ejecutado el `bloque4.py` en la Cloud Shell, comprobamos con `kubectl get pods` que los pods se hayan creado correctamente (ready: 1/1) y que estén corriendo (running). Con `kubectl get services` obtenemos la IP externa de `productpage-external`. Como se puede ver en la siguiente imagen, en este caso la IP externa es 146.148.90.41

<img width="1440" alt="kube" src="https://user-images.githubusercontent.com/99333138/215896742-dd4b46cf-396e-4bba-8c42-e3af4a889714.png">

A continuación, introducimos en el navegador la ip externa anterior con el puerto `9080`: `http://<ip-externa>:9080/productpage` obteniendo el resultado esperado.

Seleccionando v1:
<img width="1440" alt="part4-v1" src="https://user-images.githubusercontent.com/99333138/215898178-3dc6a12d-0088-4e75-8222-75c329c1aa5a.png">

Seleccionando v2:
<img width="1440" alt="part4-v2" src="https://user-images.githubusercontent.com/99333138/215898243-bdd0eea7-c071-4be7-a3e9-bf6cd1a85bc3.png">

Seleccionando v3:
<img width="1440" alt="part4-v3" src="https://user-images.githubusercontent.com/99333138/215898315-3b89a3b4-b82d-41f2-bbb3-89b22c5a461a.png">


Como podemos observar, la conexión se establece correctamente y el título de la aplicación es 37. Dicha aplicación está compuesta por cuatro servicios: uno para la página de productos (`productpage`) y otro para la descripción de los productos (`details`), uno para las críticas (`ratings`) y otro para las valoraciones (`reviews`).