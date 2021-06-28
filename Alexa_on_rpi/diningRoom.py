import flask
import socket
import subprocess

from gpiozero import LED

led = LED(4)

PORT = '5000'

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
try:
    s.connect(("8.8.8.8", 80))
    ipAddr = s.getsockname()[0]
    s.close()
except:
    print("Failed to Retrieve system IP!")
    exit(0)

try:
    fin = open("configTemplate.json", "rt")
    fout = open("config.json", "wt")
    for line in fin:
        line = line.replace('$ipaddr$', ipAddr)
        line = line.replace('$port$', PORT)
        fout.write(line)
    fin.close()
    fout.close()
except:
    print("Failed to Generate Config file!")
    exit(0)

print("Config file Generated with IP:"+ipAddr+":"+PORT)
process = 0
try:
    process = subprocess.Popen(['fauxmo','-c','config.json', '-v'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
except:
    print("Failed to Start Alexa interface with Fauxmo!")
    exit(0)

print("Alexa interface up.")

app = flask.Flask(__name__)
app.config["DEBUG"] = True


@app.route('/light/on', methods=['GET'])
def lightOn():
    led.on()
    return "0"

@app.route('/light/off', methods=['GET'])
def lightOff():
    led.off()
    return "1"

app.run(host=ipAddr, port=PORT)
