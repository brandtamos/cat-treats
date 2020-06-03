import RPi.GPIO as GPIO
import os
from time
from http.server import BaseHTTPRequestHandler, HTTPServer

host_name = '192.168.1.106'  # Change this to your Raspberry Pi IP address
host_port = 8000
servo_control_pin = 18
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

def cycle_servo():
    # setup servo control on pin 
    GPIO.setup(servo_control_pin,GPIO.OUT)
    servo1 = GPIO.PWM(servo_control_pin,50) # Note 18 is pin, 50 = 50Hz pulse
    servo1.start(0) #start PWM running, but with value of 0 (pulse off)
    time.sleep(1)
    servo1.ChangeDutyCycle(12)
    time.sleep(1)
    servo1.ChangeDutyCycle(2)
    time.sleep(1)
    servo1.ChangeDutyCycle(0)
    # Wait a couple of seconds
    time.sleep(1)
    servo1.stop()
    GPIO.cleanup()
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
           <body style="width:960px; margin: 20px auto;">
           <h1>Welcome to my Raspberry Pi</h1>
           <p>Current GPU temperature is {}</p>
           <p>Turn LED: <a href="/on">On</a> <a href="/off">Off</a></p>
           <div id="led-status"></div>
           <script>
               document.getElementById("led-status").innerHTML="{}";
           </script>
           </body>
           </html>
        '''
        temp = os.popen("/opt/vc/bin/vcgencmd measure_temp").read()
        self.do_HEAD()
        status = ''
        if self.path=='/':
            GPIO.setmode(GPIO.BCM)
        elif self.path=='/on':
            #GPIO.output(18, GPIO.HIGH)
            cycle_servo()
            status='LED is On'
        elif self.path=='/off':
            #GPIO.output(18, GPIO.LOW)
            status='LED is Off'
        self.wfile.write(html.format(temp[5:], status).encode("utf-8"))


if __name__ == '__main__':
    http_server = HTTPServer((host_name, host_port), MyServer)
    print("Server Starts - %s:%s" % (host_name, host_port))
    
    

    try:
        http_server.serve_forever()
    except KeyboardInterrupt:
        http_server.server_close()
