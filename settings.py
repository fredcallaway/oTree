from os import environ

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = {
    'real_world_currency_per_point': 0.0066666,
    'participation_fee': 0.25,
    'min_players_start': 10,
    'doc': "",
    'min_time': 5,
    "min_plays": 6,
    'num_games': 50,
    'min_wait_time': 15,
    'pay_for_waiting': 7/3600,
    'max_pay_for_wainting': 1,
    "treatment": "positive"
}

mturk_hit_settings = {
    'keywords': ['bonus', 'study'],
    'title': 'Multiplayer decision making experiment',
    'description': 'Earn a bonus ($2 on average) in this ~17 minute experiment.',
    'frame_height': 700,
    'preview_template': 'global/MTurkPreview.html',
    'minutes_allotted_per_assignment': 30,
    'expiration_hours': 7*24, # 7 days
    'grant_qualification_id': '3NMEEDRLC2LPZNWS1PU99XGRY40PQV',# to prevent retakes
    'qualification_requirements': [
        {
            'QualificationTypeId': '3NMEEDRLC2LPZNWS1PU99XGRY40PQV',
            'Comparator': 'DoesNotExist',
        },
        {
            'QualificationTypeId': "000000000000000000L0",
            'Comparator': "GreaterThan",
            'IntegerValues': [95]
        },
        {
            'QualificationTypeId': "00000000000000000071",
            'Comparator': "EqualTo",
            'LocaleValues': [{
                'Country': "US",
            }]
        }
    ]
}


SESSION_CONFIGS = [
    {
        'name': 'normal_form_games',
        'display_name': "Normal Form Games",
        'num_demo_participants': 8,
        'mturk_hit_settings': mturk_hit_settings,
        'app_sequence': [
            'lobby',
            'waiting',
            'normal_form_games',
        ],
    },
    {
        'name': 'games_only',
        'display_name': "Games Only",
        'num_demo_participants': 8,
        'mturk_hit_settings': mturk_hit_settings,
        'app_sequence': [
            'normal_form_games',
        ],
    },
    {
        'name': 'lobby',
        'display_name': "Lobby",
        'num_demo_participants': 6,
        'mturk_hit_settings': mturk_hit_settings,
        'app_sequence': [
            'lobby',
        ],
    },
]


# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'en'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'USD'
USE_POINTS = True

ROOMS = []


# AUTH_LEVEL:
# this setting controls which parts of your site are freely accessible,
# and which are password protected:
# - If it's not set (the default), then the whole site is freely accessible.
# - If you are launching a study and want visitors to only be able to
#   play your app if you provided them with a start link, set it to STUDY.
# - If you would like to put your site online in public demo mode where
#   anybody can play a demo version of your game, but not access the rest
#   of the admin interface, set it to DEMO.

# for flexibility, you can set it in the environment variable OTREE_AUTH_LEVEL
AUTH_LEVEL = environ.get('OTREE_AUTH_LEVEL')

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')


# Consider '', None, and '0' to be empty/false
DEBUG = (environ.get('OTREE_PRODUCTION') in {None, '', '0'})

DEMO_PAGE_INTRO_HTML = """ """

# don't share this with anybody.
SECRET_KEY = '!8=wtrajrj+gu-=pg6wd^!f-^rk$mj%$dob)yvl+0s+b#80vm_'

# if an app is included in SESSION_CONFIGS, you don't need to list it here
INSTALLED_APPS = ['otree', 'django.contrib.humanize']
