#PC2
#Mateo Sarria Franco de Sarabia
#Rafael Bueno Castro
#Jacobo España-Heredia Beteta

FROM node:12.18.1-slim

EXPOSE 9080

WORKDIR /opt/microservices/

COPY package.json .
COPY ratings.js .

ARG service_version
ENV SERVICE_VERSION ${service_version:-v1}

RUN npm install

CMD ["node", "ratings.js", "9080"]

