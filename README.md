**SmartHome and DIY Home automation**

**AlexaInterface** is a simple interfacing between Alex Voice Commands to python script

Dependencies:
1. Fauxmo : `python3 -m pip install fauxmo`
2. Flask: `python3 -m pip install Flask`

Running: `python3 alexaInterface.py`

**Alexa_on_rpi** is a complete smart light switch for controling with Alexa voice commands(work in progress)

Dependencies:
1. Fauxmo : `python3 -m pip install fauxmo`
2. Flask: `python3 -m pip install Flask`

Download the source and install the dependencies to Raspberry pi(tested with raspian)

Running: `python3 Path_to/diningRoom.py Path_to/configTemplate.json &` 
or add the above line to `/home/pi/.bashrc` at the bottom for launching at boot 

After boot up or running the command directly ask Alexa to "alexa discover devices"

Then saying "alexa light on" or "alexa light off" to turn the light 'on' or 'off'.

The python script triggers the rpi gpio pin number 4 high for 'on' and low for 'off'.


