.TL
Proyecto Visualización Avanzada de datos: mapas de la contaminación en Madrid a tiempo real
.AU
Manuel Bajo Buenestado
.AU
Kevin Craig Alisauskas
.AI
Universitat de València
.PP
En este proyecto se ha realizado una aplicación web utilizando Dash. La aplicación muestra unos mapas de contaminación en Madrid con datos a tiempo real, obtenidos del Portal de Datos Abiertos de Madrid. En la realización los mapas también se ha hecho uso de Plotly.
.NH
Datos
.PP
Explicar datos
.NH
Mapas de las estaciones
.PP
El mapa que se muestra a la izquierda se trata de un mapa interactivo, que utiliza un proveedor de mapas online (Mapbox) y realiza un scatter plot sobre él gracias a plotly. Cada punto azul del mapa indica la posición en el mapa de una estación, que mide el compuesto indicado. Si se sitúa el puntero del ratón sobre uno de estos puntos, se muestran el nombre de la estación y la medida del contaminante indicado realizada por esta.
.PP
El mapa de la derecha muestra un contourplot de la contaminación del compuesto indicado sobre un mapa de Madrid estático. Para realizarlo, se utilizan los puntos medidos de cada estación para triangulizar el espacio sobre el mapa y realizar una interpolación suave dentro de cada triángulo utilizando los datos de las medidas en sus esquinas. De esta manera calculamos los valores estimados de la contaminación en Madrid sobre una red de puntos equiespaciados en el espacio, que se representan mediante un contourplot interactivo de Plotly. Si situamos el puntero del rantón sobre el mapa, obtenemos el valor estimado de la contaminación para una latitud y longitud dada.

