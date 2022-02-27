FROM centos:7

RUN yum update -y && \
    yum install wget perl-Digest-SHA -y && \
    wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.0.0-linux-x86_64.tar.gz && \
    wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-8.0.0-linux-x86_64.tar.gz.sha512 && \
    shasum -a 512 -c elasticsearch-8.0.0-linux-x86_64.tar.gz.sha512 && \
    tar -xzf elasticsearch-8.0.0-linux-x86_64.tar.gz

COPY elasticsearch.yml /elasticsearch-8.0.0/config

RUN groupadd -g 1000 elasticsearch && useradd elasticsearch -u 1000 -g 1000 && \
    mkdir /var/lib/elasticsearch && \
    mkdir /var/lib/elasticsearch/data && \
    chown -R elasticsearch:elasticsearch /elasticsearch-8.0.0 && \
    chown -R elasticsearch:elasticsearch /var/lib/elasticsearch

USER elasticsearch

WORKDIR /elasticsearch-8.0.0

CMD ./bin/elasticsearch

EXPOSE 9200