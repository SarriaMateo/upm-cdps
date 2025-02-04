#PC2
#Mateo Sarria Franco de Sarabia
#Rafael Bueno Castro
#Jacobo España-Heredia Beteta

import os, sys, subprocess, yaml
from subprocess import call, run

#Borra los contenedores y las imagenes creadas
subprocess.run(["sudo", "docker-compose", "down", "--rmi", "local"])

#Borra los archivos creados
subprocess.run(["rm", "-f","./details/details.rb","./ratings/ratings.js","./ratings/package.json"])
subprocess.run(["sudo","rm", "-rf","practica_creativa2"])

#Borra los contenedores creados
#subprocess.run(["sudo", "docker", "rm", "details-37", "productpage-37", "ratings-37", "reviews-37"])
#Borra las imagenes creadas
#subprocess.run(["sudo", "docker", "rmi", "details/37", "productpage/37", "ratings/37", "reviews/37"])
