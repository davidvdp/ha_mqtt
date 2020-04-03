import argparse
import asyncio
import logging

from dvdp.ha_mqtt.client import MQTTClient
from dvdp.ha_mqtt.light import HAMQTTLight


def on_light_state_change(state):
    logging.info(f'State of light changed to {state}')


def light(args, client):
    initial_state = args.state
    logging.info(f'Initial state of light: {initial_state}')
    ha_mqtt_light = HAMQTTLight(
        args.name,
        client,
        state_change_callback=on_light_state_change,
    )
    loop = asyncio.get_event_loop()
    task = loop.create_task(ha_mqtt_light.start())
    loop.run_until_complete(task)


def switch(args, client):
    logging.warning('Switch is not available for testing.')


def main():
    parser = argparse.ArgumentParser('Test mqtt devices.')
    parser.add_argument('name', help='Name of device.')
    parser.add_argument('brokerip', help='IP of broker.')
    parser.add_argument('--username', '-u', help='MQTT username.')
    parser.add_argument('--password', '-p', help='MQTT password.')
    parser.add_argument(
        '-v',
        '--verbose',
        help='Verbose logging',
        default=False,
        action='store_true',
    )
    subparsers = parser.add_subparsers(help='Choose a device to test')
    parser_light = subparsers.add_parser('light', help='Simulate Light')
    parser_light.add_argument(
        '--state',
        '-s',
        default=False,
        type=bool,
        help='Initial state of light.'
    )
    parser_light.set_defaults(func=light)
    parser_switch = subparsers.add_parser('switch', help='Simulate Switch')
    parser_switch.set_defaults(func=switch)
    args = parser.parse_args()
    if args.verbose:
        level = logging.DEBUG
    else:
        level = logging.INFO
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=level,
    )

    client = MQTTClient(
        args.brokerip,
        'test_client',
        args.username,
        args.password,
    )

    args.func(args, client)


if __name__ == '__main__':
    main()