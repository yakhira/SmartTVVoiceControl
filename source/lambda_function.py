import boto3
import json
import config

from base64 import b64encode
from alexa.skills.smarthome import AlexaResponse as SmartHomeResponse
from alexa.skills.custom import AlexaResponse as SmartSKillsResponse
from smarttv.smarttv import SmartTV


def lambda_handler(request, context):
    response = {}

    smarttv = SmartTV(config.SQS_QUEUE_ARN)

    directive = request.get('directive', {})
    request = request.get('request', {})

    if request.get('type') == 'IntentRequest':
        alexa_response = SmartSKillsResponse(text='Sorry, i don`t know that command')

        if request['intent']['name'] == 'SmartTVApp':
            slots = request['intent']['slots']
            if 'application' in slots:
                smarttv.select_source(source=directive['payload']['name'])
                alexa_response.outputSpeech('LLALALALA')
        elif request['intent']['name'] == 'SmartTVKeypadControl':
            for key, value in request['intent']['slots'].items():
                if 'value' in value:
                    if value['name'] == 'keystroke':
                        smarttv.button(button=value['value'].upper())
                alexa_response.outputSpeech('OK')
        return alexa_response.response

    elif directive:
        name = directive['header']['name']
        namespace = directive['header']['namespace']
        correlation_token = directive['header'].get('correlationToken')
        endpoint_id = directive.get('endpoint', {}).get('endpointId')

        print(
            json.dumps({
                'name': name,
                'namespace': namespace,
                'payload': directive.get('payload')
            })
        )

        alexa_response = SmartHomeResponse(correlation_token=correlation_token)

        if namespace == 'Alexa.Authorization':
            if name == 'AcceptGrant':
                # Note: This sample accepts any grant request
                # In your implementation you would use the code and token to get and store access tokens
                grant_code = directive['payload']['grant']['code']
                grantee_token = directive['payload']['grantee']['token']
                response = SmartHomeResponse(
                    namespace='Alexa.Authorization',
                    name='AcceptGrant.Response'
                ).build_response()

        elif namespace == 'Alexa.Discovery':
            if name == 'Discover':
                alexa_response = SmartHomeResponse(namespace='Alexa.Discovery', name='Discover.Response')

                response = alexa_response.add_capability(
                    friendly_name=config.SKILL_NAME,
                    description=config.SKILL_DESCRIPTION,
                    endpoint_id=config.SKILL_ENDPOINT,
                    manufacturer_name=config.SKILL_MANUFACTURE,
                    display_categories=config.SKILL_CATEGORIES,
                    capabilities=config.SKILL_CAPABITLITES
                )

        elif namespace == 'Alexa.PowerController':
            if name == 'TurnOn':
                smarttv.turn_on()
            else:
                smarttv.turn_off()

            response = alexa_response.add_context_property(
                namespace='Alexa.PowerController',
                name='powerState',
                value='OFF' if name == 'TurnOff' else 'ON'
            )

        elif namespace == 'Alexa.Launcher':
            if name == 'LaunchTarget':
                # smarttv.command(
                #     command='system.launcher/open',
                #     payload={
                #         'target': directive['payload']['name']
                #     }
                # )
                smarttv.select_source(source=directive['payload']['name'])

            response = alexa_response.add_context_property(
                namespace='Alexa.Launcher',
                name='target',
                value={
                    'name': '',
                    'identifier': ''
                }
            )
        elif namespace == 'Alexa.KeypadController':
            if name == 'SendKeystroke':
                keystroke = directive['payload']['keystroke']
                if keystroke == 'SELECT':
                    keystroke = 'ENTER'
                smarttv.button(button=keystroke)

            response = alexa_response.add_context_property(
                namespace='Alexa',
                name='Response'
            )

        elif namespace == 'Alexa.ChannelController':
            if name == 'ChangeChannel':
                if directive['payload']['channelMetadata']:
                    number = directive['payload']['channelMetadata']['name']
                if 'channel' in directive['payload']:
                    number = directive['payload']['channel']['number']

                numbers = str(number)

                for i in range(0, len(numbers)):
                    smarttv.button(button=numbers[i])

            elif name == 'SkipChannels':
                if directive['payload']['channelCount'] > 0:
                    smarttv.button(button='CHANNELUP')
                else:
                    smarttv.button(button='CHANNELDOWN')

            response = alexa_response.add_context_property(
                namespace='Alexa',
                name='Response'
            )
        elif namespace == 'Alexa.Speaker':
            if name == 'AdjustVolume':
                volume = directive['payload']['volume']
                if volume > 0:
                    smarttv.volume_up(
                        1 if volume == 10 
                        else volume
                    )
                else:
                    smarttv.volume_down(
                        -1 if volume == -10 
                        else volume
                    )
            elif name == 'SetVolume':
                volume = int(directive['payload']['volume'])/100
                smarttv.set_volume(volume_level=volume)
            elif name == 'SetMute':
                smarttv.volume_mute(
                    is_volume_muted=directive['payload']['mute']
                )
            response = alexa_response.add_context_property(
                namespace='Alexa',
                name='Response'
            )
        elif namespace == 'Alexa.InputController':
            if name == 'SelectInput':
                input_type = directive['payload']['input']
                smarttv.select_source(source=input_type.replace(' ', '-'))

            response = alexa_response.add_context_property(
                namespace='Alexa.InputController',
                name='input',
                value=input_type
            )
        elif namespace == 'Alexa.PlaybackController':
            if name == 'Play':
                smarttv.media_play()
            if name == 'Pause':
                smarttv.media_pause()
            if name == 'Stop':
                smarttv.media_stop()

            response = alexa_response.add_context_property(
                namespace='Alexa',
                name='Response'
            )
        else:
            response = alexa_response.error_event(
                type='NOT_SUPPORTED_IN_CURRENT_MODE',
                message=f'Command not supported by SmartTV.'
            )

    return response
