#PC2
#Mateo Sarria Franco de Sarabia
#Rafael Bueno Castro
#Jacobo España-Heredia Beteta

import os

def reemplazar(archivo, old, new):
    f = open(archivo,'r')
    
    with f as file:
        text = file.read()   
    f.close()
    
    f = open(archivo,'w')
    with f as file:
        text = text.replace(old,new)
        f.write(text)
    f.close()

#Modificamos el archivo requirements.txt
reemplazar("requirements.txt","requests==2.21.0","requests")

#Cambiamos el titulo para incluir el numero de grupo (37)
nGrupo = os.environ.get("GROUP_NUMBER")
reemplazar("templates/productpage.html", "Simple Bookstore App", nGrupo)