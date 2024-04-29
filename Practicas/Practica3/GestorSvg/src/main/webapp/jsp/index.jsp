<!DOCTYPE html>
<html lang="es">
	<head>
		<title>Gestor SVG</title>
		<link href="/GestorSvg/css/styleSheet.css" rel="stylesheet">
		<meta charset="ISO-8859-1">
	</head>
	<body>
		<header>
			<h1>Gestor de im�genes SVG en base de datos eXist</h1>
			<h2>Sistemas Web 2024</h2>
		</header>
		<%	if (request.getAttribute("informacion") != null) {	%>
		<section>
			<font>Informaci�n:</font>
			<%=request.getAttribute("informacion")%>
		</section>
		<% 	} %>
		<!--Muestra las colecciones de imagenes SVG-->
		<section>
			<table>
				<tr>
					<td style="width:150px; background-color:#d7dbdd">
						<h4>Mostrar las im�genes SVG de una Colecci�n</h4>
					</td>
					<td style="width:600px">
						<form id="LeerRecursos" method="GET" action="/GestorSvg/apiLR">
							<table><tr>
								<td>Introducir nombre de la Colecci�n:</td>
								<td><input required name="collection"></td>
							</tr></table>			
						<hr>
						<button type="submit" form="LeerRecursos">Ver imagenes</button>
						</form>
					</td>
				</tr>
			</table>
		</section>
		<!--Crea una nueva colecci�n de imagenes SVG-->
		<section>
			<table>
				<tr>
					<td style="width:150px; background-color:#d7dbdd">
						<h4>Crear una nueva Colecci�n de im�genes SVG</h4>
					</td>
					<td style="width:600px">
						<form id="CrearColeccion" method="GET" action="/GestorSvg/apiCC">
							<table><tr>
								<td>Introducir nombre de la Colecci�n:</td>
								<td><input required name="collection"></td>
							</tr></table>
						
						<hr>
						<button type="submit" form="CrearColeccion">Crear coleccion</button>
						</form>
					</td>
				</tr>
			</table>
		</section>
		<!--Crea una nueva imagen SVG en blanco-->
		<section>
			<table>
				<tr>
					<td style="width:150px; background-color:#d7dbdd">
						<h4>Crear una nueva imagen SVG (en blanco) en una Colecci�n</h4>
					</td>
					<td style="width:600px">
						<form id="ImagenNueva" method="GET" action="/GestorSvg/apiNI">
							<table><tr>
								<td>Nombre de la nueva imagen SVG:</td>
								<td><input required name="svgName"></td>
							</tr><tr>
								<td>Colecci�n destino de la imagen</td>
								<td><input required name="collection"></td>
							</tr></table>
						
						<hr>
						<button id="submit" form="ImagenNueva">Nueva imagen</button>
						</form>
					</td>
				</tr>
			</table>
		</section>
		<!--Borra una colecci�n de imagenes SVG-->
		<section>
			<table>
				<tr>
					<td style="width:150px; background-color:#d7dbdd">
						<h4>Borrar una colecci�n de imagenes SVG</h4>
					</td>
					<td style="width:600px">
						<form id="BorrarColeccion" method="GET" action="/GestorSvg/apiDC">
							<table><tr>
								<td>Introducir nombre de la colecci�n:</td>
								<td><input  required name="collection"></td>
							</tr></table>
						<hr>
						<button form="BorrarColeccion">Borrar colecci�n</button>
						</form>
					</td>
				</tr>
			</table>
		</section>
		<!--Lee un archivo SVG y lo sube a la base de datos-->
		<script>
			function leerArchivo() {
				// Guarda el contenido del archivo en el campo oculto contenidoArchivo
				var fileInput = document.getElementById('fileInput');
				var file = fileInput.files[0];
				var reader = new FileReader();
				reader.onload = function(e) {
					document.getElementById('contenidoArchivo').value = e.target.result;
				};
				reader.readAsText(file);
				console.log("Archivo leido");
				console.log(document.getElementById('contenidoArchivo').value);
			}
		</script>
		<section>
			<table>
				<tr>
					<td style="width:150px; background-color:#d7dbdd">
						<h4>Sube una imagen SVG desde un archivo a un Colecci�n</h4>
					</td>
					<td style="width:600px">
						<input type="file" id="fileInput" accept=".svg" /> 
						<button onclick="leerArchivo()">Leer Archivo</button>
						<hr>
						<form id="ImagenFichero" method="POST" action="/GestorSvg/apiNIF">
							<input type="hidden" id="contenidoArchivo" name="imagenSVG" required>		
							<table><tr>
								<td>Nombre de la nueva imagen SVG:</td>
								<td><input id="nombreArchivo" required name="svgName"></td>	
							</tr><tr>
								<td>Colecci�n destino de la imagen</td>
								<td><input required name="collection"></td>
							</tr></table>
							<hr>
							<button id="submit" form="ImagenFichero">Subir imagen</button>
						</form>
					</td>
				</tr>
			</table>
		</section>
		<!--Footer-->
		<footer>
			<h5>Sistemas Web - Escuela Ingenier�a de Bilbao</h5>
		</footer>
	</body>
</html>