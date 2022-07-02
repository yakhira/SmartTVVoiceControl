import os

SQS_QUEUE_ARN = os.getenv('SQS_QUEUE_ARN', 'us-west-2')
SKILL_NAME = 'Smart TV'
SKILL_DESCRIPTION = 'Smart TV TV Voice Controll Skill'
SKILL_ENDPOINT = 'smart-tv-01'
SKILL_MANUFACTURE = 'LG'
SKILL_CATEGORIES = ['TV', 'Video']
SKILL_CAPABITLITES = [
    {
        'interface': 'Alexa.PowerController',
        'supported': [
            {
                'name': 'powerState'
            }
        ]
    },
    {
        'interface': 'Alexa.Launcher',
        'supported': [
            {
                'name': 'LaunchTarget'
            }
        ]
    },
    {
        'interface': 'Alexa.KeypadController',
        'keys': [
            'INFO',
            'MORE',
            'SELECT',
            'UP',
            'DOWN',
            'LEFT',
            'RIGHT',
            'PAGE_UP',
            'PAGE_DOWN',
            'PAGE_LEFT',
            'PAGE_RIGHT'
        ]
    },
    {
        'interface': 'Alexa.ChannelController',
        'supported': [
            {
                'name': 'channel'
            }
        ]
    },
    {
        'interface': 'Alexa.Speaker',
        'supported': [
            {
                "name": "volume",
            },
            {
                "name": "muted",
            }
        ]
    },
    {
        'interface': 'Alexa.InputController',
        'supported': [
            {
                'name': 'input'
            }
        ],
        'inputs': [
            {
                'name': 'HDMI-1'
            },
            {
                'name': 'HDMI-2'
            },
            {
                'name': 'HDMI-3'
            },
            {
                'name': 'AV'
            }
        ]
    },
    {
        'interface': 'Alexa.PlaybackController',
        'supportedOperations': [
            'Play',
            'Pause',
            'Stop'
        ]
    }
]
