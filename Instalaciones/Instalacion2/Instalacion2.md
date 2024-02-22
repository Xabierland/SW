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

# Descargamos Tomcat
wget https://dlcdn.apache.org/tomcat/tomcat-10/v10.1.19/bin/apache-tomcat-10.1.19.tar.gz -O apache-tomcat.tar.gz
sudo tar xzvf apache-tomcat.tar.gz -C /opt/tomcat --strip-components=1 

# Cambiamos los permisos
sudo chown -R tomcat:tomcat /opt/tomcat/
sudo chmod -R u+x /opt/tomcat/bin

# Configuramos el usuario admin
echo "<role rolename="manager-gui" />
<user username="manager" password="root" roles="manager-gui" />

<role rolename="admin-gui" />
<user username="admin" password="root" roles="manager-gui,admin-gui" />" | sudo tee -a /opt/tomcat/conf/tomcat-users.xml

echo "...
<Context antiResourceLocking="false" privileged="true" >
  <CookieProcessor className="org.apache.tomcat.util.http.Rfc6265CookieProcessor"
                   sameSiteCookies="strict" />
<!--  <Valve className="org.apache.catalina.valves.RemoteAddrValve"
         allow="127\.\d+\.\d+\.\d+|::1|0:0:0:0:0:0:0:1" /> -->
  <Manager sessionAttributeValueClassNameFilter="java\.lang\.(?:Boolean|Integer|Long|Number|String)|org\.apache\.catalina\.filters\.Csr>
</Context>" | sudo tee -a /opt/tomcat/webapps/manager/META-INF/context.xml

echo "...
<Context antiResourceLocking="false" privileged="true" >
  <CookieProcessor className="org.apache.tomcat.util.http.Rfc6265CookieProcessor"
                   sameSiteCookies="strict" />
<!--  <Valve className="org.apache.catalina.valves.RemoteAddrValve"
         allow="127\.\d+\.\d+\.\d+|::1|0:0:0:0:0:0:0:1" /> -->
  <Manager sessionAttributeValueClassNameFilter="java\.lang\.(?:Boolean|Integer|Long|Number|String)|org\.apache\.catalina\.filters\.Csr>
</Context>" | sudo tee -a /opt/tomcat/webapps/host-manager/META-INF/context.xml

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
WantedBy=multi-user.target" | sudo tee -a /etc/systemd/system/tomcat.service

# Recargamos el daemon
sudo systemctl daemon-reload

# Iniciamos Tomcat
sudo systemctl start tomcat

# Habilitamos Tomcat
sudo systemctl enable tomcat
```
