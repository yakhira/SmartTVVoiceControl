import random
import uuid

from .alexa_utils import get_utc_timestamp


class AlexaResponse:

    def __init__(self, **kwargs):

        self.context_properties = []
        self.payload_endpoints = []

        # Set up the response structure
        self.context = {}
        self.event = {
            'header': {
                'namespace': kwargs.get('namespace', 'Alexa'),
                'name': kwargs.get('name', 'Response'),
                'messageId': str(uuid.uuid4()),
                'payloadVersion': kwargs.get('payload_version', '3')
                # 'correlation_token': kwargs.get('correlation_token', 'INVALID')
            },
            'endpoint': {
                "scope": {
                    "type": "BearerToken",
                    "token": kwargs.get('token', 'INVALID')
                },
                "endpointId": kwargs.get('endpoint_id', 'INVALID')
            },
            'payload': kwargs.get('payload', {})
        }

        if 'correlation_token' in kwargs:
            self.event['header']['correlation_token'] = kwargs.get('correlation_token', 'INVALID')

        if 'cookie' in kwargs:
            self.event['endpoint']['cookie'] = kwargs.get('cookie', '{}')

        # No endpoint in an AcceptGrant or Discover request
        if self.event['header']['name'] == 'AcceptGrant.Response' or self.event['header']['name'] == 'Discover.Response':
            self.event.pop('endpoint')

    def add_capability(self, **kwargs):
        capabilities = [
            {
                'type': capability.get('type', 'AlexaInterface'),
                'interface': capability.get('interface', 'Alexa'),
                'version': capability.get('version', '3'),
                "capabilityResources": capability.get('capability_resources'),
                "configuration": capability.get('configuration', {}),
                "semantics": capability.get('instance', {}),
                'keys': capability.get('keys', []),
                'inputs': capability.get('keys', []),
                'supportedOperations': capability.get('supportedOperations', []),
                'properties': {
                    'supported': capability.get('supported', None),
                    'proactivelyReported': capability.get('proactively_reported', True),
                    'retrievable': capability.get('retrievable', True)
                }
            }
            for capability in kwargs.get('capabilities', [])
        ]
        
        self.payload_endpoints.append({
            'endpointId': kwargs.get('endpoint_id', 'endpoint_' + "%0.6d" % random.randint(0, 999999)),
            'manufacturerName': kwargs.get('manufacturer_name', 'Sample Manufacturer'),
            'description': kwargs.get('description', 'Sample Endpoint Description'),
            'friendlyName': kwargs.get('friendly_name', 'Sample Endpoint'),
            'displayCategories': kwargs.get('display_categories', ['OTHER']),
            'capabilities': capabilities,
            'additionalAttributes': kwargs.get('additionalAttributes', {}),
            'connections': kwargs.get('connections'),
            'relationships': kwargs.get('relationships', {}),
            'cookie': kwargs.get('cookie', {})
        })
        return self.build_response()

    def add_context_property(self, **kwargs):
        self.context_properties.append({
            'namespace': kwargs.get('namespace', 'Alexa.EndpointHealth'),
            'name': kwargs.get('name', 'connectivity'),
            'value': kwargs.get('value', {'value': 'OK'}),
            'timeOfSample': get_utc_timestamp(),
            'uncertaintyInMilliseconds': kwargs.get('uncertainty_in_milliseconds', 0)
        })
        return self.build_response()
    
    def error_event(self, **kwargs):
        self.event['header']['namespace'] = 'Alexa'
        self.event['header']['name'] = 'ErrorResponse'
        self.event['payload'] = {
            'type': kwargs.get('type', 'INTERNAL_ERROR'),
            'message': kwargs.get('message', 'Internal error')
        }
        return self.build_response()

    def build_response(self, remove_empty=True):

        response = {
            'context': self.context,
            'event': self.event
        }

        if len(self.context_properties) > 0:
            response['context']['properties'] = self.context_properties

        if len(self.payload_endpoints) > 0:
            response['event']['payload']['endpoints'] = self.payload_endpoints

        if remove_empty:
            if len(response['context']) < 1:
                response.pop('context')

        return response
