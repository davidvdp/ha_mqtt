from datetime import datetime, timedelta
import uuid
import json
import paho.mqtt.client as mqtt
import logging

from dvdp.ha_mqtt.client import MQTTClient

class Device:
    def __init__(self, name):
        self.__name = name

class HAMQTTLight(Device):
    def __init__(
        self,
        name: str,
        mqtt_client: MQTTClient,
        state_change_callback,
    ):
        """
        Create Home Assistant MQTT Light.

        :param name: The name that is used for its MQTT nodes.
        :param mqtt_client: MQTTClient object used for communication.
        :param state_change_callback: Callback function called when a state
        change has been requested. Function should have 1 argument (state:
        str) either 'ON' or 'OFF'
        """
        logging.info(f'Setting up MQTT Light {name}...')
        super().__init__(name)
        self.__client = mqtt_client
        self.__state_change_callback = state_change_callback
        self.__name = name

        unique_id = '{}_{}'.format(name, uuid.getnode())

        self.__root_topic = 'homeassistant/light/{}/light'.format(name)
        self.__command_topic = '{}/set'.format(self.__root_topic)
        self.__state_topic = '{}/state'.format(self.__root_topic)
        self.__availability_topic = '{}/available'.format(self.__root_topic)

        config = dict()
        config['brightness'] = False
        config['color_temp'] = False
        config['schema'] = 'json'
        config['command_topic'] = self.__command_topic
        config['state_topic'] = self.__state_topic
        config['json_attributes_topic'] = self.__root_topic
        config['name'] = name
        config['unique_id'] = unique_id
        config['availability_topic'] = self.__availability_topic

        device = dict()
        device['identifiers'] = [unique_id]
        device['name'] = name
        device['sw_version'] = '1.0'
        device['model'] = 'Action Kaku'
        config['device'] = device

        self.__config_json = json.dumps(config, indent='  ')
        self.__started = False

    async def __fetch_messages(self):
        while self.__started:
            value = await self.__client.get(
                self.__command_topic)
            self.__handle_command(value)

    def __handle_command(self, command):
        logging.debug('Handling command {} for {}.'.format(
            command,
            self.__name,
        ))
        self.__client.publish(self.__state_topic, command, qos=2, retain=True)

        command_json = json.loads(command.decode())
        self.__state_change_callback(command_json['state'])

    def on_connect(self):
        logging.debug('Handling on connect call for {}'.format(self.__name))
        self.__initialize()
        self.__subscribe()

    def __initialize(self):
        self.__client.publish(
            '{}/config'.format(self.__root_topic),
            self.__config_json
        )
        self.__client.publish(
            self.__availability_topic,
            'online',
        )

    def __subscribe(self):
        result, mid = self.__client.subscribe(
            topic=self.__command_topic,
            on_connect=self.on_connect,
        )
        if result == mqtt.MQTT_ERR_NO_CONN:
            logging.error('Could not subscribe to topic '
                          '{}.'.format(self.__command_topic))

    async def start(self):
        self.__initialize()
        self.__subscribe()

        self.__started = True
        logging.info(f'Started MQTT light {self.__name}')
        await self.__fetch_messages()

    def stop(self):
        self.__started = False
