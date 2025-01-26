# taken from http://www.piware.de/2011/01/creating-an-https-server-in-python/
# generate server.pem with the following command:
#    openssl req -new -x509 -keyout key.pem -out server.pem -days 365 -nodes
# run as follows:
#    python simple-https-server.py
# then in your browser, visit:
#    https://localhost:4443


import http.server
import ssl

server_address = ('localhost', 8000)
httpd = http.server.HTTPServer(server_address,
                               http.server.SimpleHTTPRequestHandler)
if False:
    httpd.socket = ssl.wrap_socket(httpd.socket,
                                   server_side=True,
                                   certfile="server.pem",
                                   keyfile="key.pem",
                                   ssl_version=ssl.PROTOCOL_TLS)
else:
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain(certfile='server.pem', keyfile="key.pem")
    httpd.socket = context.wrap_socket(httpd.socket, server_side = True)
print("https://localhost:8000")
httpd.serve_forever()
