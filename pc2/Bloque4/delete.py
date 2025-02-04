#PC2
#Mateo Sarria Franco de Sarabia
#Rafael Bueno Castro
#Jacobo España-Heredia Beteta

import os, sys, subprocess, yaml
from subprocess import call, run

#Destruimos los servicios de kubernetes
subprocess.run(["kubectl", "delete", "-f", "details/details.yaml"])
subprocess.run(["kubectl", "delete", "-f", "ratings/ratings.yaml"])
subprocess.run(["kubectl", "delete", "-f", "reviews/reviews-service.yaml"])
subprocess.run(["kubectl", "delete", "-f", "reviews/reviews-v1-deployment.yaml"])
subprocess.run(["kubectl", "delete", "-f", "reviews/reviews-v2-deployment.yaml"])
subprocess.run(["kubectl", "delete", "-f", "reviews/reviews-v3-deployment.yaml"])
subprocess.run(["kubectl", "delete", "-f", "productPage/productpage.yaml"])
