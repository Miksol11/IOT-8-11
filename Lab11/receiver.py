import paho.mqtt.client as mqtt
import time

broker = "10.108.33.125"
topic = "rfid/card"

client = mqtt.Client()

def processMessage(client, userdata, message):
    message_decoded = str(message.payload.decode("utf-8")).split(";")
    if len(message_decoded) != 2:
        print("Odebrano niepoprawny komunikat!")
        return
    
    print(f"Odebrano: UID: {message_decoded[0]} TIME: {message_decoded[1]}")

def setup():
    client.connect(broker)
    client.on_message = processMessage
    client.loop_start()
    client.subscribe(topic)

def close():
    client.loop_stop()
    client.disconnect()

if __name__ == "__main__":
    try:
        setup()
        while True:
            time.sleep(0.05)
    except KeyboardInterrupt:
        close()