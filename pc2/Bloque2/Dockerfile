#PC2
#Mateo Sarria Franco de Sarabia
#Rafael Bueno Castro
#Jacobo España-Heredia Beteta

FROM python:3.7.7-slim

# Actualiza el sistema y expone el puerto 9080
RUN apt-get update && apt-get install -y git && apt-get install -y python3-pip && apt-get clean
EXPOSE 9080

# Establece la variable de entorno GROUP_NUMBER con el valor 37
ENV GROUP_NUMBER=37

# Clona el repositorio de GitHub
RUN git clone https://github.com/CDPS-ETSIT/practica_creativa2.git

# Establece el directorio de trabajo en la ubicación de la aplicación
WORKDIR /practica_creativa2/bookinfo/src/productpage

#Copia y ejecuta el script de pyhton de para renombrar requirements.txt e index.html
COPY rename.py .
RUN python3 rename.py

# Instala las dependencias de Python desde requirements.txt
RUN pip3 install -r requirements.txt

# Comando para iniciar la aplicación
CMD ["python3", "productpage_monolith.py", "9080"]
