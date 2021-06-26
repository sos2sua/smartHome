# fauxmo -c config.json -v

import flask
import socket
import subprocess


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


@app.route('/movieTime/on', methods=['GET'])
def movTmOn():
    print("Enjoy ur movie...")
    return "0"

@app.route('/movieTime/off', methods=['GET'])
def movTmOff():
    print("hope ur movie was good...")
    return "1"

app.run(host=ipAddr, port=PORT)