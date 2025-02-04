#PC2
#Mateo Sarria Franco de Sarabia
#Rafael Bueno Castro
#Jacobo España-Heredia Beteta

import subprocess, os

def reemplazar(archivo, old, new):
    f = open('./practica_creativa2/bookinfo/src/productpage/'+archivo,'r')
    
    with f as file:
        text = file.read()
    
    f.close()
    
    f = open("./practica_creativa2/bookinfo/src/productpage/"+archivo,'w')
    with f as file:
        text = text.replace(old,new)
        f.write(text)
    f.close()

    
#Clonamos el repositorio
subprocess.call(["git clone https://github.com/CDPS-ETSIT/practica_creativa2.git"], shell=True)

#Modificamos el archivo requirements.txt
reemplazar("requirements.txt","requests==2.21.0","requests")

#Instalamos pip3 y las dependencias
subprocess.call(["pip3 install -r ./practica_creativa2/bookinfo/src/productpage/requirements.txt"], shell=True)

#Cambiamos el titulo para incluir el numero de grupo (37)
os.environ["GROUP_NUMBER"]="37"
nGrupo = os.environ.get("GROUP_NUMBER")
reemplazar("templates/productpage.html", "Simple Bookstore App", nGrupo)
    
#Lanzamos el programa
subprocess.call([f"python3 ./practica_creativa2/bookinfo/src/productpage/productpage_monolith.py 9080"], shell=True)
