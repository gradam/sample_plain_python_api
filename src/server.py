import cgi
import urllib.parse

from http.server import BaseHTTPRequestHandler, HTTPServer

from router import router
from utils.exceptions import UnauthenticatedError


class MyServer(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_POST(self):
        try:
            view = self._get_view()
            self._set_headers()
            data = self._get_post_data()
            response = view.post(data)
            self.wfile.write(response)
        except UnauthenticatedError:
            self._unauthenticated_error()
            self.wfile.write()

    def do_DELETE(self):
        try:
            view = self._get_view()
            self._set_headers()
            response = view.delete()
            self.wfile.write(response)
        except UnauthenticatedError:
            self._unauthenticated_error()
            self.wfile.write()

    def do_PATCH(self):
        try:
            view = self._get_view()
            self._set_headers()
            data = self._get_post_data()
            response = view.patch(data)
            self.wfile.write(response)
        except UnauthenticatedError:
            self._unauthenticated_error()
            self.wfile.write()

    def _unauthenticated_error(self):
        self.send_response(401)
        self.end_headers()

    def _get_view(self):
        token = self.headers.get("Authorization", "")
        return router(self.path, token)

    def _get_post_data(self):
        ctype, pdict = cgi.parse_header(self.headers.get("content-type"))
        if ctype == "application/x-www-form-urlencoded":
            length = int(self.headers.get("content-length"))
            data = urllib.parse.parse_qs(self.rfile.read(length), keep_blank_values=1)
        else:
            data = {}

        decoded_data = {
            k.decode("utf-8"): v[0].decode("utf-8") for k, v in data.items()
        }

        return decoded_data


def run():
    print("Listening on 127.0.0.1:8080")
    server = HTTPServer(("127.0.0.1", 8080), MyServer)
    server.serve_forever()


run()
