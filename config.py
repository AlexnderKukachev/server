import os
import configparser

config = configparser.ConfigParser()

URLS = []
BALANCER_URL = None

__urls_path = os.path.join(os.curdir, 'service_urls.env')
if os.path.exists(__urls_path):
    config.read(__urls_path)
    __targets = config.options('TARGETS')
    for target in __targets:
        URLS.append(config.get('TARGETS', target))
    BALANCER_URL = config.get('BALANCER', 'url')