from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import socket
import json
from mongodbmanager import MongoDBManager
from multiprocessing import Process
from pathlib import Path

class HttpHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        if pr_url.path == '/':
            self.send_html_file('index.html')
        elif pr_url.path == '/success.html':
            self.send_html_file('success.html')
        elif pr_url.path == '/message.html':
            self.send_html_file('message.html')
        elif (pr_url.path.endswith(".png") or pr_url.path.endswith(".css")) and Path("public/" + pr_url.path).is_file():
            self.send_html_file('public' + pr_url.path)
        else:
            self.send_html_file('error.html', 404)


    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        with open(filename, 'rb') as fd:
            self.wfile.write(fd.read())


    def do_POST(self):
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            data = self.rfile.read(int(self.headers['Content-Length']))
            data_parse = urllib.parse.unquote_plus(data.decode())
            data_dict = {key: value for key, value in [el.split('=') for el in data_parse.split('&')]}

            client.connect(('', 5000))     
            json_data = json.dumps(data_dict)
            client.send(json_data.encode('utf-8'))
            message = client.recv(1024).decode('utf-8')

            self.send_response(301)
            self.send_header('Location', '/success.html' if message == 'success' else '/error.html')
            self.end_headers()
        except:
            self.send_response(301)
            self.send_header('Location','/error.html')
            self.end_headers()
            return
        finally:
            client.close()


def run_web_server(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ('', 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


def run_socket_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', 5000))
    server.listen()
    mongoDBManager = MongoDBManager()

    while True:
        client, _ = server.accept()
        data = client.recv(4096)
        if not data:
            break
        
        json_data = data.decode('utf-8')
        parsed_json = json.loads(json_data)
        res = mongoDBManager.add_record(parsed_json)
        client.send(("success" if res else "fail").encode('utf-8'))

    client.close()


if __name__ == '__main__':
    web_server_process = Process(target=run_web_server)
    web_server_process.start()

    socket_server_process = Process(target=run_socket_server)
    socket_server_process.start()

    print("Both servers are running...")

    web_server_process.join()
    socket_server_process.join()
