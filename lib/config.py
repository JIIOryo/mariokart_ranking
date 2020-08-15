import json

def get_config(config_path):
    with open(config_path) as f:
        config = json.load(f)
    return {
        'nickname': config['nickname'],
        'line_notify_token': config['line_notify_token'],
    }
