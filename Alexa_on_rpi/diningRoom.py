import sys
import time
import flask
import socket
import subprocess

ON_RPI = True
if ON_RPI == True:
    from gpiozero import LED

CONF_PATH = ""

if len(sys.argv) != 2:
    print("Expecting path to Config Template!")
    exit(0)

CONF_PATH = sys.argv[1]

print("Using Config Template File at "+CONF_PATH)

if ON_RPI == True:
    lamp = LED(4)
    sofaLight = LED(17)

PORT = '5000'

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while(True):
    try:
        s.connect(("8.8.8.8", 80))
        ipAddr = s.getsockname()[0]
        s.close()
        break
    except:
        print("Failed to Retrieve system IP!")
        time.sleep(15)

try:
    fin = open(CONF_PATH + "configTemplate.json", "rt")
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


@app.route('/lamp/on', methods=['GET'])
def lightOn():
    if ON_RPI == True:
        lamp.on()
    return "0"

@app.route('/lamp/off', methods=['GET'])
def lightOff():
    if ON_RPI == True:
        lamp.off()
    return "1"

@app.route('/sofaLight/on', methods=['GET'])
def sofaLightOn():
    if ON_RPI == True:
        sofaLight.on()
    return "0"

@app.route('/sofaLight/off', methods=['GET'])
def sofaLightOff():
    if ON_RPI == True:
        sofaLight.off()
    return "1"

app.run(host=ipAddr, port=PORT)
