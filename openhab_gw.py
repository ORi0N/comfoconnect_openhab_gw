#!/usr/bin/python3
import argparse
import paho.mqtt.client as mqtt
import datetime
from time import sleep
from binascii import unhexlify
from random import randint
from pycomfoconnect import *
import getopt

## Configuration #######################################################################################################

local_name = 'OpenHAB2 ComfoConnect Gateway'			# Name of the service
local_uuid = bytes.fromhex('00000000000000000000000000000005')  # Can be what you want, used to differentiate devices (as only 1 simultaneously connected device is allowed)

device_ip = "192.168.2.150"					# Look in your router administration and get the ip of the comfoconnect device and set it as static lease
device_uuid = bytes.fromhex('0000000000191011800170b3d5426d66') # Get this from using discovery first by running the script with flag: -d <ip-address> and then configure it here
pin = 1234 							# Set PIN of vent unit !

mqtt_broker = "192.168.1.50"					# Set your MQTT broker here
mqtt_user = "my_user"						# Set the MQTT user login
mqtt_passw = "my_pw"						# Set the MQTT user password
mqtt_topic = "Zehnder/ComfoAirQ450/"				# Set the MQTT root topic

## Start logger ########################################################################################################

## Connect to Comfocontrol device  #####################################################################################
bridge = Bridge(device_ip, device_uuid)
#bridge.debug = True
comfoconnect = ComfoConnect(bridge, local_uuid, local_name, pin)

previousreply = b'\x01'
prevspeed = 0
prevmode = 0
prevalt = 0
prevvalue = {81 : 0, 213 : 0, 122 : 0, 121 : 0 }

def pub_on_connect(client, userdata, flags, rc):
    print("publisher connected")
def pub_on_disconnect(client, userdata, rc):
    print("publisher disconnected, reconnecting...")
    clientpub.reconnect()
def sub_on_connect(client, userdata, flags, rc):
    print("subscriber connected")
def sub_on_disconnect(client, userdata, rc):
    print("subscriber disconnected, reconnecting...")
    client.reconnect()

def on_message(client, userdata, message):
    global prevalt
    #print("message received " ,str(message.payload.decode("utf-8")))
    setting = str(message.payload.decode("utf-8"))
    # comfoconnect.cmd_rmi_request(CMD_FAN_MODE_AWAY)  # Go to away mode
    # comfoconnect.cmd_rmi_request(CMD_FAN_MODE_LOW)  # Set fan speed to 1
    # comfoconnect.cmd_rmi_request(CMD_FAN_MODE_MEDIUM)  # Set fan speed to 2
    # comfoconnect.cmd_rmi_request(CMD_FAN_MODE_HIGH)  # Set fan speed to 3
    if setting == '0':
         comfoconnect.cmd_rmi_request(CMD_FAN_MODE_AWAY)
         print("SETTING FANSPEED LOW")
         get_status_msg()
    elif setting == '1':
         comfoconnect.cmd_rmi_request(CMD_FAN_MODE_LOW)
         print("SETTING FANSPEED NORMAL")
         get_status_msg()
    elif setting == '2':
         comfoconnect.cmd_rmi_request(CMD_FAN_MODE_MEDIUM)
         print("SETTING FANSPEED HIGH")
         get_status_msg()
    elif setting == '3':
         comfoconnect.cmd_rmi_request(CMD_FAN_MODE_HIGH)
         print("SETTING FANSPEED MAX")
         get_status_msg()
    elif setting == '4':
         comfoconnect.cmd_rmi_request(CMD_MODE_AUTO)
         print("SETTING TO AUTO")
         prevalt=0
         get_status_msg()
    elif setting == '5':
         comfoconnect.cmd_rmi_request(CMD_MODE_MANUAL)
         print("SETTING TO MANUAL")
         prevalt=0
         get_status_msg()
    elif setting == '6':
         get_status_msg()
    elif setting == '7':
         comfoconnect.cmd_rmi_request(CMD_VENTMODE_SUPPLY)
         print("NOW IN SUPPLY MODE ONLY")
    elif setting == '8':
         comfoconnect.cmd_rmi_request(CMD_VENTMODE_BALANCE)
         print("NOW IN BALANCE MODE")
    elif setting == '9':
         comfoconnect.cmd_rmi_request(CMD_TEMPPROF_NORMAL)
         print("CONFIG: TEMP PROFILE NORMAL")
    elif setting == '10':
         comfoconnect.cmd_rmi_request(CMD_TEMPPROF_COOL)
         print("CONFIG: TEMP PROFILE COOL")
    elif setting == '11':
         comfoconnect.cmd_rmi_request(CMD_TEMPROF_WARM)
         print("CONFIG: TEMP PROFILE WARM")
    elif setting == '12':
         comfoconnect.cmd_rmi_request(CMD_BYPASS_ON)
         print("CONFIG: BYPASS ACTIVATED")
    elif setting == '13':
         comfoconnect.cmd_rmi_request(CMD_BYPASS_OFF)
         print("CONFIG: BYPASS DEACTIVATED")
    elif setting == '14':
         comfoconnect.cmd_rmi_request(CMD_BYPASS_AUTO)
         print("CONFIG: BYPASS IN AUTO MODE")
    elif setting == '15':
         comfoconnect.cmd_rmi_request(CMD_SENS_TEMP_OFF)
         print("CONFIG: TEMPERATURE PASSIVE DEACTIVATED")
    elif setting == '16':
         comfoconnect.cmd_rmi_request(CMD_SENS_TEMP_AUTO)
         print("CONFIG: TEMPERATURE PASSIVE IN AUTO MODE")
    elif setting == '17':
         comfoconnect.cmd_rmi_request(CMD_SENS_TEMP_ON)
         print("CONFIG: TEMPERATURE PASSIVE ACTIVATED")
    elif setting == '18':
         comfoconnect.cmd_rmi_request(CMD_SENS_HUMC_OFF)
         print("CONFIG: HUMIDITY COMFORT DEACTIVATED")
    elif setting == '19':
         comfoconnect.cmd_rmi_request(CMD_SENS_HUMC_AUTO)
         print("CONFIG: HUMIDITY COMFORT IN AUTO MODE")
    elif setting == '20':
         comfoconnect.cmd_rmi_request(CMD_SENS_HUMC_ON)
         print("CONFIG: HUMIDITY COMFORT ACTIVATED")
    elif setting == '21':
         comfoconnect.cmd_rmi_request(CMD_SENS_HUMP_OFF)
         print("CONFIG: HUMIDITY PROTECTION DEACTIVATED")
    elif setting == '22':
         comfoconnect.cmd_rmi_request(CMD_SENS_HUMP_AUTO)
         print("CONFIG: HUMIDITY PROTECTION IN AUTO MODE")
    elif setting == '23':
         comfoconnect.cmd_rmi_request(CMD_SENS_HUMP_ON)
         print("CONFIG: HUMIDITY PROTECTION ACTIVATED")
    elif setting == '24':
         comfoconnect.cmd_rmi_request(CMD_VENTMODE_EXTRACT)
         print("VENT MODE EXTRACT ONLY ACTIVATED")
    elif int(setting) >= 50:
         comfoconnect.cmd_rmi_request(eval("CMD_UNKNOWN%s" %setting))
         print("UNKNOWN%s" % setting)

def get_status_msg():
         global previousreply, prevspeed, prevmode, prevalt
         reply = comfoconnect.cmd_rmi_request(CMD_READ_CONFIG)

         if previousreply != reply.msg.message[11:58]:
               #print("READ CONFIG %s" % reply.msg)
               #print("READ CONFIG %s" % reply.msg.message)
               previousreply = reply.msg.message[11:58]

         if b'\x00' == reply.msg.message[10:11]:
               alt = 0
         else:
               alt = 1
         if b'\x01' == reply.msg.message[57:58]:
               #print("IS MANUAL")
               mode="5"
         else:
               #print("IS AUTOMATIC")
               if (alt==0):
                     mode=4
               else:
                     mode=41
         if b'\x00' == reply.msg.message[14:15]:
                #print("SPEED 0")
               speed=0
         elif b'\x01' == reply.msg.message[14:15]:
               #print("SPEED 1")
               speed=1
         elif b'\x02' == reply.msg.message[14:15]:
               #print("SPEED 2")
               speed=2
         elif b'\x03' == reply.msg.message[14:15]:
               #print("SPEED 3")
               speed=3
         if b'\x00' == reply.msg.message[10:11]:
               alt = 0
         else:
               alt = 1
         if (speed != prevspeed) or (mode!= prevmode) or (alt != prevalt):
               print("mode:%s speed:%s alt:%s" % (mode, speed, alt))
               clientpub.publish(("%sconfig/mode" % mqtt_topic), ("%s" % mode))
               clientpub.publish(("%sconfig/speed" % mqtt_topic), ("%s" % speed))
               prevspeed = speed
               prevmode = mode
               prevalt = alt

         clientpub.publish(("%sconfig/mode" % mqtt_topic), ("%s" % mode))
         clientpub.publish(("%sconfig/speed" % mqtt_topic), ("%s" % speed))

client = mqtt.Client(client_id="S1_%s" % randint(1, 10000), clean_session=False)
client.on_connect = sub_on_connect
client.on_disconnect = sub_on_disconnect
client.username_pw_set(mqtt_user,mqtt_passw)
client.connect(mqtt_broker)
client.subscribe("Zehnder/ComfoAirQ450/ExecuteFunction",qos=1)
client.on_message=on_message #attach function to callback
client.loop_start()

clientpub = mqtt.Client(client_id="P1_%s" % randint(1, 10000), clean_session=False)
clientpub.on_connect = pub_on_connect
clientpub.on_disconnect = pub_on_disconnect
clientpub.username_pw_set(mqtt_user,mqtt_passw)
clientpub.connect(mqtt_broker)
clientpub.loop_start()

def bridge_discovery(ip):
    ## Bridge discovery ################################################################################################

    # Method 1: Use discovery to initialise Bridge
    #bridges = Bridge.discover(timeout=1)
    #if bridges:
    #    bridge = bridges[0]
    #else:
    #    bridge = None

    # Method 2: Use direct discovery to initialise Bridge
    bridges = Bridge.discover(ip)
    if bridges:
        bridge = bridges[0]
    else:
        bridge = None

    # Method 3: Setup bridge manually
    # bridge = Bridge(args.ip, bytes.fromhex('0000000000251010800170b3d54264b4'))

    if bridge is None:
        print("No bridges found!")
        exit(1)

    print("Bridge found: %s (%s)" % (bridge.uuid.hex(), bridge.host))
    bridge.debug = True

    return bridge

def callback_sensor(var, value):
    ## Callback sensors ################################################################################################
    if (var == 81):
         num = struct.unpack('<i', bytes.fromhex(value))
         #print("%d" % num)
         value = ("%d" % num)
         now = datetime.datetime.now()
         end = b = now + datetime.timedelta(0,int(value))
         #print(end.strftime("%d-%m-%Y %H:%M"))
         value = end.strftime("%d-%m-%Y %H:%M")

    #if(var not in [213, 81, 121, 122, 117, 118, 119, 120, 128]):
    clientpub.publish("%s%s" % (mqtt_topic,var) ,"%s" % value, 0, 1)
    #print("Sent to MQTT Broker : %s%s = %s" % (mqtt_topic, var, value))

def main():
    opts, args = getopt.getopt(sys.argv[1:],"d:",["discovery"])
    for opt, args in opts:
        if opt in ("-d", "--discovery"):
            print("discover!")
            bridge = bridge_discovery(args)
            exit(0)


    comfoconnect.callback_sensor = callback_sensor

    try:
        # Connect to the bridge
        # comfoconnect.connect(False)  # Don't disconnect existing clients.
        comfoconnect.connect(True)  # Disconnect existing clients.

    except Exception as e:
        print('ERROR: %s' % e)
        exit(1)

    ## Register sensors ################################################################################################

    comfoconnect.register_sensor(SENSOR_FAN_NEXT_CHANGE)  # General: Countdown until next fan speed change
    comfoconnect.register_sensor(SENSOR_FAN_SUPPLY_SPEED)  # Fans: Supply fan speed
    comfoconnect.register_sensor(SENSOR_FAN_EXHAUST_SPEED)  # Fans: Exhaust fan speed
    comfoconnect.register_sensor(SENSOR_POWER_TOTAL_YEAR)  # Power Consumption: Total year-to-date
    comfoconnect.register_sensor(SENSOR_AVOIDED_HEATING_TOTAL_YEAR)  # Avoided Heating: Avoided year-to-date
    comfoconnect.register_sensor(SENSOR_FAN_SPEED_MODE)  # Fans: Fan speed setting
    comfoconnect.register_sensor(SENSOR_FAN_SUPPLY_DUTY)  # Fans: Supply fan duty
    comfoconnect.register_sensor(SENSOR_FAN_EXHAUST_DUTY)  # Fans: Exhaust fan duty
    comfoconnect.register_sensor(SENSOR_FAN_SUPPLY_FLOW)  # Fans: Supply fan flow
    comfoconnect.register_sensor(SENSOR_FAN_EXHAUST_FLOW)  # Fans: Exhaust fan flow
    comfoconnect.register_sensor(SENSOR_POWER_CURRENT)  # Power Consumption: Current Ventilation
    comfoconnect.register_sensor(SENSOR_POWER_TOTAL)  # Power Consumption: Total from start
    comfoconnect.register_sensor(SENSOR_DAYS_TO_REPLACE_FILTER)  # Days left before filters must be replaced
    comfoconnect.register_sensor(SENSOR_AVOIDED_HEATING_CURRENT)  # Avoided Heating: Avoided actual
    comfoconnect.register_sensor(SENSOR_AVOIDED_HEATING_TOTAL)  # Avoided Heating: Avoided total
    comfoconnect.register_sensor(SENSOR_TEMPERATURE_SUPPLY)  # Temperature & Humidity: Supply Air (temperature)
    comfoconnect.register_sensor(SENSOR_TEMPERATURE_EXTRACT)  # Temperature & Humidity: Extract Air (temperature)
    comfoconnect.register_sensor(SENSOR_TEMPERATURE_EXHAUST)  # Temperature & Humidity: Exhaust Air (temperature)
    comfoconnect.register_sensor(SENSOR_TEMPERATURE_OUTDOOR)  # Temperature & Humidity: Outdoor Air (temperature)
    comfoconnect.register_sensor(SENSOR_HUMIDITY_SUPPLY)  # Temperature & Humidity: Supply Air (temperature)
    comfoconnect.register_sensor(SENSOR_HUMIDITY_EXTRACT)  # Temperature & Humidity: Extract Air (temperature)
    comfoconnect.register_sensor(SENSOR_HUMIDITY_EXHAUST)  # Temperature & Humidity: Exhaust Air (temperature)
    comfoconnect.register_sensor(SENSOR_HUMIDITY_OUTDOOR)  # Temperature & Humidity: Outdoor Air (temperature)
    comfoconnect.register_sensor(SENSOR_BYPASS_STATE)  # Bypass state
    comfoconnect.register_sensor(SENSOR_RUNMODE_SUPPLY_BALANCE)
    comfoconnect.register_sensor(SENSOR_AUTO_STATE)
#    comfoconnect.register_sensor(SENSOR_AWAY_STATE)
#    comfoconnect.register_sensor(SENSOR_TEMP_PROFILE)
#    comfoconnect.register_sensor(SETTING_BYPASS)
#    comfoconnect.register_sensor(SETTING_HEATING_SEASON)
#    comfoconnect.register_sensor(SETTING_RF_PAIRING)

    #unknown types investigation
#    unknown = [33, 37, 53, 71, 82, 85, 86, 87, 144, 145, 146, 208, 211, 212, 216, 217, 218, 219, 224, 226, 228, 321, 325, 337, 338, 341, 369, 370, 371, 372, 384, 386, 400, 401, 402, 416, 417, 418, 419]
#    for x in unknown:
#         comfoconnect.register_sensor(x)
#         print ("%d" % x)


    ## Execute functions ###############################################################################################

    # TimeRequest
    timeinfo = comfoconnect.cmd_time_request()
    #print(timeinfo)

    ## Executing functions #############################################################################################

    # comfoconnect.cmd_rmi_request(CMD_FAN_MODE_AWAY)  # Go to away mode
    # comfoconnect.cmd_rmi_request(CMD_FAN_MODE_LOW)  # Set fan speed to 1
    # comfoconnect.cmd_rmi_request(CMD_FAN_MODE_MEDIUM)  # Set fan speed to 2
    # comfoconnect.cmd_rmi_request(CMD_FAN_MODE_HIGH)  # Set fan speed to 3

    ## Example interaction #############################################################################################

    try:
        print('Waiting... Stop with CTRL+C')
        while True:
            # Callback messages will arrive in the callback method.
            if comfoconnect.is_connected():
                get_status_msg()
            else:
                print('%s > We are not connected anymore...' % datetime.datetime.now())
            sleep(5)
    except KeyboardInterrupt:
        pass

    ## Closing the session #############################################################################################

    client.loop_stop()
    clientpub.loop_stop()
    comfoconnect.disconnect()


if __name__ == "__main__":
    main()
