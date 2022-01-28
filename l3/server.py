from http.server import HTTPServer, SimpleHTTPRequestHandler


class MyServer(SimpleHTTPRequestHandler):
    def do_GET(self) -> None:
        self.send_response(200)
        self.send_header("content-type", "text/html")
        self.end_headers()
        content = '<h1>hello world</h1>'
        self.wfile.write(content.encode())


address = "127.0.0.1"
port = 8000
server_address = (address, port)
httpd = HTTPServer(server_address, MyServer)
httpd.serve_forever()
