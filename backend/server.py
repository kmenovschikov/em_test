import http.server
import socketserver

PORT = 8800
Handler = http.server.SimpleHTTPRequestHandler

with socketserver.TCPServer(("", PORT), Handler) as httpd:
    print(f"Сервер запущен на порту {PORT}")
    httpd.serve_forever()
