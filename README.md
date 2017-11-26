This is a mod for the python library that michael arnauts has written on https://github.com/michaelarnauts/comfoconnect/ so that it would work together with any MQTT enabled smart home software (openhab in my case).

You'll need:
- Working linux env
- Python3
- See page of michael for other dependencies
- Paho MQTT lib

What does this gateway script do?

It discovers the ComfoConnect LAN C Device. See the required config at the top in the gateway file. run it with option -d <ip-address of the device> first and then set the parameters in the script. Then, run it without additional parameters and you should see messages in your MQTT broker.
It connects to the Comfoconnect LAN C Device and relays the information between MQTT and the device in both directions. You can see sensor data, config and set the ventilation speed, balance mode, ... The main stuff Michael and myself discovered is in his protocol file.

I am simply sharing my code here so that others may benefit from it. I cannot provide bugfixes or support for this. The python code is very basic and should get you going easily. Simply modify and debug as I did :) And if you discover new things about the protocol, share your intel :)

To startup the script at boot time, add it to your rc.local file, or deamonize it:
For example mine looks like this: /usr/bin/python3 -u /home/orion/comfoconnect/gateway.py >> /var/log/openhab_comfoconnect_gateway.log &

