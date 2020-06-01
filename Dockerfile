FROM ubuntu:16.04
LABEL maintainer="hillary.elrick@sickkids.ca"
ENV DEBIAN_FRONTEND noninteractive

# INSTALL BASE REQUIREMENTS
RUN apt-get update && \
    apt-get install -y git sudo apache2 && \
    cd /var/www/html && \
    rm index.html

# CHANGE DOCUMENT ROOT AND SERVERNAME
# Output apache's access.log to stdout and error.log to stderr
WORKDIR /etc/apache2
RUN sed -i -e "/DocumentRoot/a \ \t\<Directory \'\/var\/www\/html\'\>\n\t\tOptions +ExecCGI\n\t\tAddHandler cgi-script .py\n\t\tAllow from all\n\t</Directory\>" sites-available/000-default.conf \
    && sed -i '1 i\ServerName FORCAST' apache2.conf \
    && ln -sf /proc/self/fd/1 /var/log/apache2/access.log \
    && ln -sf /proc/self/fd/2 /var/log/apache2/error.log

# GET HOST CODE
COPY . /var/www/html/
WORKDIR /var/www/html/

# INSTALL DEPENDENCIES
RUN cd src/installation && \
    ./install.sh /var/www/html && \
    ./setPermissions.sh \
    && cp -R /var/www/html/docs/bin/bootstrap-4.4.1-dist /var/www/html/bin/bootstrap-4.4.1-dist
