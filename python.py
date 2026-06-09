from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs

class Servidor(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path == "/":
            self.servir_archivo("index.html", "text/html")
        elif self.path == "/styles.css":
            self.servir_archivo("styles.css", "text/css")
        else:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"404 - No encontrado")

    def do_POST(self):
        if self.path == "/contacto":
            longitud = int(self.headers.get("Content-Length", 0))
            datos_raw = self.rfile.read(longitud).decode("utf-8")
            datos = parse_qs(datos_raw)

            nombre  = datos.get("nombre",  ["(sin nombre)"])[0]
            email   = datos.get("email",   ["(sin email)"])[0]
            mensaje = datos.get("mensaje", ["(sin mensaje)"])[0]

            print("\nNUEVO MENSAJE DE CONTACTO")
            print(f"  Nombre : {nombre}")
            print(f"  Email  : {email}")
            print(f"  Mensaje: {mensaje}")
            print("\n")

            respuesta = b"<h2>Mensaje recibido. Gracias por contactarnos.</h2><a href='/'>Volver</a>"
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(respuesta)

    def servir_archivo(self, nombre_archivo, tipo):
        try:
            with open(nombre_archivo, "rb") as archivo:
                self.send_response(200)
                self.send_header("Content-Type", tipo)
                self.end_headers()
                self.wfile.write(archivo.read())
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Archivo no encontrado")

    def log_message(self, format, *args):
        print(f"[Servidor] {args[0]} {args[1]}")

server = HTTPServer(("localhost", 8000), Servidor)
print("Servidor iniciado")
print("Abrir en: http://localhost:8000")
server.serve_forever()