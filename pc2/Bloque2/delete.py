#PC2
#Mateo Sarria Franco de Sarabia
#Rafael Bueno Castro
#Jacobo España-Heredia Beteta

import subprocess 

#Detiene el contenedor
subprocess.run(["sudo", "docker", "stop", "product-page-g37"])
#Borra el contenedor
subprocess.run(["sudo", "docker", "rm", "product-page-g37"])
#Borra la imagen de docker
subprocess.run(["sudo", "docker", "rmi", "product-page/g37"])