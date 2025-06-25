from http.server import BaseHTTPRequestHandler, HTTPServer
import os
import mimetypes

hostName = "localhost"
serverPort = 8080


class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        # Определяем базовый путь к файлам
        base_dir = os.path.dirname(__file__)

        # Если запрос корневой - отдаем contacts.html
        if self.path == '/':
            file_path = os.path.join(base_dir, 'contacts.html')
        else:
            # Иначе пытаемся найти запрашиваемый файл
            file_path = os.path.join(base_dir, self.path[1:])

        try:
            # Проверяем существование файла
            if not os.path.exists(file_path):
                raise FileNotFoundError

            # Определяем MIME-тип файла
            mime_type, _ = mimetypes.guess_type(file_path)
            if mime_type is None:
                mime_type = 'application/octet-stream'

            # Читаем файл в бинарном режиме
            with open(file_path, 'rb') as file:
                content = file.read()

            self.send_response(200)
            self.send_header("Content-type", mime_type)
            self.end_headers()
            self.wfile.write(content)

        except FileNotFoundError:
            self.send_error(404, "File Not Found")
        except Exception as e:
            self.send_error(500, f"Server Error: {str(e)}")


if __name__ == "__main__":
    webServer = HTTPServer((hostName, serverPort), MyServer)
    print(f"Server started http://{hostName}:{serverPort}")

    try:
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass

    webServer.server_close()
    print("Server stopped.")