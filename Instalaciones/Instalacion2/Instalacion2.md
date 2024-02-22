# Instalacion de Recursos

> [!NOTE]
> Distribucion: Debian 12 (Bookworm)

## Java

> [!NOTE]
> Esta es la version 17 de Java, no la 8 pero no deberia haber problemas con la version de Java.

```bash
# Instalamos Java
sudo apt install openjdk-17-jdk

# Comprobamos la version e instalacion
java -version
javac -version
```

> [!WARNING]
> Si quieres tener varias versiones y quieres cambiar entre ellas, puedes usar `sudo update-alternatives --config java` y `sudo update-alternatives --config javac`

## MySQL

```bash
# Agregamos los repositorios
wget https://dev.mysql.com/get/mysql-apt-config_0.8.29-1_all.deb -O mysql-apt-config.deb
sudo dpkg -i mysql-apt-config.deb
sudo apt update
# Instalamos el servidor
sudo apt install mysql-server
```

> [!WARNING]
> En caso de tener alguna otra base de datos MySQL instalada como MariaDB, es necesario desinstalarla antes de instalar MySQL.
> `sudo apt-get remove --purge mysql\*`

## Tomcat

> [!NOTE]
> No es la version 8 de Tomcat, pero no deberia haber problemas con la version de Tomcat.

```bash
# Añadimos un usuario para Tomcat
sudo useradd -m -d /opt/tomcat -U -s /bin/false tomcat 
```

```bash
# Descargamos Tomcat
wget https://dlcdn.apache.org/tomcat/tomcat-10/v10.1.19/bin/apache-tomcat-10.1.19.tar.gz -O apache-tomcat.tar.gz
sudo mkdir /opt/tomcat
sudo tar xzvf apache-tomcat.tar.gz -C /opt/tomcat --strip-components=1 
```

```bash
# Cambiamos los permisos
sudo chown -R tomcat:tomcat /opt/tomcat/
sudo chmod -R u+x /opt/tomcat/bin
```

```bash
# Configuramos el usuario admin
echo '<tomcat-users xmlns="http://tomcat.apache.org/xml"
              xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
              xsi:schemaLocation="http://tomcat.apache.org/xml tomcat-users.xsd"
              version="1.0">
<role rolename="manager-gui" />
<role rolename="admin-gui" />
<user username="root" password="root" roles="manager-gui,admin-gui" />
</tomcat-users>
' | sudo tee /opt/tomcat/conf/tomcat-users.xml
```

```bash
# Creamos el daemon
echo "[Unit]
Description=Tomcat
After=network.target

[Service]
Type=forking

User=tomcat
Group=tomcat

Environment="JAVA_HOME=/usr/lib/jvm/java-1.17.0-openjdk-amd64"
Environment="JAVA_OPTS=-Djava.security.egd=file:///dev/urandom"
Environment="CATALINA_BASE=/opt/tomcat"
Environment="CATALINA_HOME=/opt/tomcat"
Environment="CATALINA_PID=/opt/tomcat/temp/tomcat.pid"
Environment="CATALINA_OPTS=-Xms512M -Xmx1024M -server -XX:+UseParallelGC"

ExecStart=/opt/tomcat/bin/startup.sh
ExecStop=/opt/tomcat/bin/shutdown.sh

RestartSec=10
Restart=always

[Install]
WantedBy=multi-user.target" | sudo tee /etc/systemd/system/tomcat.service
```

```bash
# Recargamos el daemon
sudo systemctl daemon-reload

# Iniciamos Tomcat
sudo systemctl start tomcat

# Habilitamos Tomcat
sudo systemctl enable tomcat
```
