import logging
from typing import Optional

import paho.mqtt.client as mqtt

from dvdp.ha_mqtt.message_queue import MessageQueue


class MQTTClient:
    def __init__(
            self,
            broker_ip: str,
            client_name: str,
            username: Optional[str] = None,
            password: Optional[str] = None,
    ):
        self.__client = self.__create_client(
            client_name,
            username,
            password,
        )
        self.__connect(broker_ip)
        self.__message_queue = MessageQueue()
        self.__on_connect_callbacks = []

    async def get(self, topic: str):
        return await self.__message_queue.get(topic)

    def subscribe(self, topic: str, on_connect, qos: int = 0):
        self.__on_connect_callbacks.append(on_connect)
        return self.__client.subscribe(topic, qos)

    def publish(self, topic, payload, qos=2, retain=True):
        return self.__client.publish(topic, payload, qos=qos, retain=retain)

    def __on_connect(self, userdata, flags, rc):
        logging.debug("Connected with result code " + str(rc))

        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        self.__client.subscribe("$SYS/#")
        for callback in self.__on_connect_callbacks:
            callback()

    def __on_message(self, client, userdata, msg):
        if '$SYS' in msg.topic:
            return
        logging.debug('Received: {} -> {}'.format(msg.topic, msg.payload))
        self.__message_queue.add(msg.topic, msg.payload)
        logging.debug('Queue size {}'.format(len(self.__message_queue)))

    def __on_disconnect(self, client, userdata, rc):
        logging.exception('Lost connection to MQTT broker.')
        self.__message_queue.stop_get()
        raise ConnectionError('Lost connection to MQTT broker.')

    def __connect(self, broker_ip):
        try:
            self.__client.connect(broker_ip)
            self.__client.loop_start()
        except ConnectionRefusedError as ex:
            logging.exception(
                'Could not connect to broker. Did you provide the correct ip '
                'as an argument?')
            raise ex

    def __create_client(
            self,
            client_name,
            username=None,
            password=None,
    ):
        logging.info('Starting mqtt client {} ...'.format(client_name))

        client = mqtt.Client(client_name)
        client.username_pw_set(username, password)
        client.on_connect = self.__on_connect
        client.on_message = self.__on_message
        client.on_disconnect = self.__on_disconnect
        return client

