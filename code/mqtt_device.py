#!/usr/bin/python
# coding=UTF-8
import paho.mqtt.client as mqtt
import threading
import json
import random
 



host = '1.12.255.251'
port = 1883
keepalive = 60
up_topic = 'DEV00001_UP'
sub_topic = "DEV00001_DOWN"


str_json_test= { "head":{
 "dev_id": 1, 
"msg_id": 50003, 
"msg_no": 1, 
"timestamp": 1492488028395 
},
 "data":{ 
"Battery":55, 
"Longitude": 1142354321, 
"Latitude":225342178, 
"Altitude":900, 
 "Env_Temperature":263, 
 "Env_Humidity": 878,
 "Env_Pressure":1013,
  "Rainfall":12, 
"Wind_Speed": 34, 
 "Wind_Direction": 450,
"Switch":1,
"Variable_Val_0": 23, 
 "Variable_Val_1": 0, 
 "Variable_Val_2": 0
}
}

def fun_timer():
    str_json_test['data']['Env_Temperature'] = 250 + random.randint(-30,30)
    str_json_test['data']['Env_Humidity'] = 700 + random.randint(-30,30)
    str_json_test['data']['Env_Pressure'] = 1010 + random.randint(-30,30)
    str_json_test['data']['Wind_Speed'] = 30 + random.randint(-30,30)
    str_json_test['data']['Wind_Direction'] = 0 + random.randint(-300,300)
    str_json_test['data']['Rainfall'] = 10 + random.randint(-10,10)
    json_str = json.dumps(str_json_test)
    client.publish(up_topic,json_str)
    global timer  #定义变量
    timer = threading.Timer(0.5,fun_timer)   #1秒调用一次函数
    #定时器构造函数主要有2个参数，第一个参数为时间，第二个参数为函数名
    timer.start()    #启用定时器


def on_connect(client, userdata, flags, rc):
    #print("Connected with result code "+str(rc))
    client.subscribe(sub_topic)
    timer = threading.Timer(1,fun_timer)  #首次启动1S time
    timer.start()
    
def on_message(client, userdata, msg):
    print(msg.topic+" " + ":" + str(msg.payload))
    dir_str = json.loads(msg.payload)
    
    str_json_test['data']['Variable_Val_0'] = dir_str['data']['Variable_Val_0']
    str_json_test['data']['Variable_Val_1'] = dir_str['data']['Variable_Val_1']
    str_json_test['data']['Variable_Val_2'] = dir_str['data']['Variable_Val_2']
    json_str = json.dumps(str_json_test)
    client.publish(up_topic,json_str)

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect(host,port,keepalive)
client.loop_forever()



client.disconnect()
print("success")
