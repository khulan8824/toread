from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import SocketServer
import urlparse
import time

class HTTPPingServer(BaseHTTPRequestHandler):
    
    def do_GET(self):
        self.send_response(200)
        self.send_header('Last-Modified', self.date_time_string(time.time()))
        self.end_headers()
        self.wfile.write('Response body\n')
        return

    def do_POST(self):
        self.send_response(200)
        self.send_header('Last-Modified', self.date_time_string(time.time()))
        self.end_headers()
        self.wfile.write('Response body\n')
        return


if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer
    server = HTTPServer(('0.0.0.0', 11230), HTTPPingServer)
    print 'Starting server, use <Ctrl-C> to stop'
    server.serve_forever()
