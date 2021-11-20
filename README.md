# Traductor Simultáneo
Aplicación ejemplo sobre el uso de servicios de IBM Watson Speech to Text, Translation y Text to Speech

## Uso
<ol>
  <li>Abra su cuenta en IBM Cloud y cree servicios de IBM Watson Speech to Text, Translation y Text to Speech.</li>
  <li>copie el archivo ejemplo de configuración (application.ini.sample) como application.ini
  <li>Exporte la configuración del servicio, botón download en la página de credenciales de cada una de los servicios
    creados.</li>
  <li>Incluya las configuraciones exportadas en el archivo de application.ini</li>
  <li>Vaya a la carpeta del capítulo que desee revisar</li>
  <li>Ejecute el programa con el comando python Prototipo-Traductor.py</li>
</ol>


## Diferencias con la aplicación presentada en los videos
Esta versión se diferencia básicamente en los siguientes aspectos:
<ol>
  <li>La configuración de los servicios está guardada en application.ini. Los valores de APIKEY y URL de los 
    diferentes servicios pueden ser definidos como variables ambientales o como valores en el archivo de configuración, 
    dando prelación a los definidos por medio de valores ambientales.  Los nombres de las variables ambientales se han
    cambiado para que coincidan con los entregados por los servicios de IBM Watson, haciendo más fácil su
    configuración, solo bajando el archivo de configuración entregado por IBM Watson y copiándolo en 
    application.ini
  </li>
  <li>Se agregó comentarios al código para que este sea más fácil de seguir</li>
  <li>Se organizó el código en tres carpetas, una por cada uno de los videos, pero la construcción es incremental,
    así que si lo desea, puede ir directamente al capítulo 3
  </li>
</ol>
  
