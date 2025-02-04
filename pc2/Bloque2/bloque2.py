#PC2
#Mateo Sarria Franco de Sarabia
#Rafael Bueno Castro
#Jacobo España-Heredia Beteta

import subprocess

#Creamos la imagen de docker
subprocess.run(["sudo", "docker", "build", "-t", "product-page/g37", "."])
#Arrancamos el contenedor
subprocess.run(["sudo", "docker", "run", "--name", "product-page-g37", "-p", "9080:9080", "-e", "GROUP_NUM=37", "-d", "product-page/g37"])