#PC2
#Mateo Sarria Franco de Sarabia
#Rafael Bueno Castro
#Jacobo España-Heredia Beteta

FROM ruby:2.7.1-slim

WORKDIR /opt/microservices/

COPY details.rb .

ARG service_version
ARG enable_external_book_service

ENV SERVICE_VERSION ${service_version:-v1}
ENV ENABLE_EXTERNAL_BOOK_SERVICE ${enable_external_book_service:-true}

EXPOSE 9080

CMD ["ruby", "details.rb", "9080"]
