import RPi.GPIO as GPIO
import os
import time
from http.server import BaseHTTPRequestHandler, HTTPServer

host_name = '192.168.1.106'  # Change this to your Raspberry Pi IP address
host_port = 8000
motor_control_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

#setup pin to pull down
GPIO.setup(motor_control_pin, GPIO.OUT)
GPIO.output(motor_control_pin, GPIO.LOW)

def cycle_motor():
    # setup servo control on pin 
    GPIO.output(motor_control_pin, GPIO.HIGH)
    time.sleep(4)
    GPIO.output(motor_control_pin, GPIO.LOW)
    print ("Cycle done")

class MyServer(BaseHTTPRequestHandler):
    """ A special implementation of BaseHTTPRequestHander for reading data from
        and control GPIO of a Raspberry Pi
    """

    def do_HEAD(self):
        """ do_HEAD() can be tested use curl command
            'curl -I http://server-ip-address:port'
        """
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        """ do_GET() can be tested using curl command
            'curl http://server-ip-address:
        """
        html = '''
           <html>
            <head>
            <meta http-equiv="content-type" content="text/html; charset=windows-1252">
            <style>
            a.button {
                -webkit-appearance: button;
                -moz-appearance: button;
                appearance: button;
                text-decoration: none;
                color: initial;
                height: 300px;
                display: inline-block;
                width: 50%;
                text-align: center;
                line-height: 300px;
                font-size: 3em;
            }

            body{
                text-align: center;
            }

            </style>
            </head>
            <body>
            <h1>Welcome to Treats!</h1>
            <p><a class="button" href="dispense">Dispense Treat</a></p>
            </body>
            </html>
        '''
        temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
        self.do_HEAD()

        if self.path=='/':
            GPIO.setmode(GPIO.BCM)
        elif self.path=='/dispense':
            cycle_motor()
        self.wfile.write(html.encode("utf-8"))


if __name__ == '__main__':
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))
    
    

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()
