#PC2
#Mateo Sarria Franco de Sarabia
#Rafael Bueno Castro
#Jacobo España-Heredia Beteta

import os, sys, subprocess
from subprocess import call, run

#El primer parametro de la llamada es la version elegida
version = str(sys.argv[1])

if version == "v1" or version == "v2" or version == "v3":
    #Construimos los servicios de kubernetes
    subprocess.run(["kubectl", "apply", "-f", "productPage/productpage.yaml"])
    subprocess.run(["kubectl", "apply", "-f", "details/details.yaml"])
    subprocess.run(["kubectl", "apply", "-f", "ratings/ratings.yaml"])
    subprocess.run(["kubectl", "apply", "-f", "reviews/reviews-service.yaml"])
    if version == "v1":
      subprocess.run(["kubectl", "apply", "-f", "reviews/reviews-v1-deployment.yaml"])
    if version == "v2":
      subprocess.run(["kubectl", "apply", "-f", "reviews/reviews-v2-deployment.yaml"])
    if version == "v3":
      subprocess.run(["kubectl", "apply", "-f", "reviews/reviews-v3-deployment.yaml"])
else:
    print("ERROR: se ha introducido una version no valida (v1, v2 o v3) !!!\n")
    exit()
  