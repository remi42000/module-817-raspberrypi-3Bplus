from http.server import BaseHTTPRequestHandler, HTTPServer
import RPi.GPIO as GPIO
from urllib.parse import urlparse, parse_qs

# List of GPIO pins to control
PINS = [17, 27, 22, 5]

# GPIO setup
GPIO.setmode(GPIO.BCM)
for pin in PINS:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urlparse(self.path)
        query = parse_qs(parsed.query)

        if parsed.path == "/gpio" and "pin" in query and "state" in query:
            try:
                pin = int(query["pin"][0])
                state = query["state"][0]
                if pin in PINS:
                    GPIO.output(pin, GPIO.HIGH if state == "on" else GPIO.LOW)
                    self.send_response(204)
                    self.end_headers()
                    return
            except:
                pass
            self.send_error(400, "Bad Request")
        elif parsed.path == "/" or parsed.path == "/index.html":
            try:
                with open("index.html", "rb") as file:
                    self.send_response(200)
                    self.send_header("Content-type", "text/html")
                    self.end_headers()
                    self.wfile.write(file.read())
            except FileNotFoundError:
                self.send_error(404, "index.html not found")
        else:
            self.send_error(404)

# Start server
if __name__ == "__main__":
    try:
        server = HTTPServer(('', 8000), Handler)
        print("Server running at http://<pi_ip>:8000/")
        server.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down server")
    finally:
        GPIO.cleanup()
