# Multi-stage build for any Spring Boot module in this monorepo
# Build arg SERVICE_MODULE = e.g. auth-service, discovery-server

FROM maven:3.9-eclipse-temurin-17 AS build
WORKDIR /app
VOLUME /root/.m2

COPY settings.xml /root/.m2/settings.xml
COPY pom.xml .
COPY common-lib/pom.xml common-lib/
COPY discovery-server/pom.xml discovery-server/
COPY config-server/pom.xml config-server/
COPY api-gateway/pom.xml api-gateway/
COPY auth-service/pom.xml auth-service/
COPY customer-service/pom.xml customer-service/
COPY restaurant-service/pom.xml restaurant-service/
COPY menu-service/pom.xml menu-service/
COPY order-service/pom.xml order-service/
COPY delivery-partner-service/pom.xml delivery-partner-service/
COPY payment-service/pom.xml payment-service/
COPY notification-service/pom.xml notification-service/

#RUN mvn dependency:go-offline -B -q || true

COPY common-lib common-lib
COPY discovery-server discovery-server
COPY config-server config-server
COPY api-gateway api-gateway
COPY auth-service auth-service
COPY customer-service customer-service
COPY restaurant-service restaurant-service
COPY menu-service menu-service
COPY order-service order-service
COPY delivery-partner-service delivery-partner-service
COPY payment-service payment-service
COPY notification-service notification-service

ARG SERVICE_MODULE
RUN mvn clean package -pl ${SERVICE_MODULE} -am -DskipTests -B -q

FROM eclipse-temurin:17-jre-jammy
RUN apt-get update && apt-get install -y --no-install-recommends curl \
    && rm -rf /var/lib/apt/lists/*
WORKDIR /app

ARG SERVICE_MODULE
COPY --from=build /app/${SERVICE_MODULE}/target/${SERVICE_MODULE}-*.jar /app/app.jar

ENV JAVA_OPTS="-Xms256m -Xmx512m"
ENTRYPOINT ["sh", "-c", "java $JAVA_OPTS -jar /app/app.jar"]
