#!/bin/bash
LIQUIBASE=/opt/liquibase/liquibase.jar

java -jar $LIQUIBASE \
    --changeLogFile=/opt/builder/src/src/main/resources/liquibase/changelog.xml \
    --driver=com.mysql.jdbc.jdbc2.optional.MysqlDataSource \
    --username=agora \
    --password=tomasz.12 \
    --url=jdbc:mysql://172.16.1.5:3306/agora_erp \
    --classpath=/opt/liquibase/mysql-connector-java-5.0.8-bin.jar \
    --driver=com.mysql.jdbc.Driver \
    update%     