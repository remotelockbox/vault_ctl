#!/usr/bin/env python3
import argparse
import datetime
import sys

import requests
import json
from requests.auth import HTTPBasicAuth

# read from vault_credentials.ini
user_name = 'not set'
user_key = 'not set'
box_key = 'not set'

api_headers = {
    "Content-type": "application/json"
}


def read_credentials():
    import configparser
    config = configparser.ConfigParser()
    config.read('vault_credentials.ini')

    global user_name, user_key, box_key
    creds = config['api']
    user_name = creds['user_name']
    user_key = creds['user_key']
    box_key = creds['box_key']


def main():
    parser = argparse.ArgumentParser(
        description='control the pivault. Set API permissions to enable or disable each operation.')
    parser.add_argument('--status', default=False, help='prints lock and session status',
                        action='store_true')
    parser.add_argument('--add-minutes', default=None, type=int, metavar='N',
                        help='minutes to add to the lock time. If not already locked, creates a new sessions')
    parser.add_argument('--show-status', default=False, help='show the release time at the end of the command',
                        action='store_true')
    parser.add_argument('--unlock', default=False, help='unlock the lockbox',
                        action='store_true')
    parser.add_argument('--silent', default=False, help='require manual unlocking by pressing the physical button',
                        action='store_true')
    parser.add_argument('--clear', default=False, help='clear any ongoing session',
                        action='store_true')

    args = parser.parse_args()

    read_credentials()

    if args.status:
        print_status()
    elif args.unlock:
        print("unlocking")
        unlock(args.silent)
    elif args.add_minutes is not None:
        dt = datetime.datetime.utcnow() + datetime.timedelta(minutes=args.add_minutes)
        print(f"adding {args.add_minutes} minutes")
        set_unlock_time(dt)
    else:
        parser.print_help()


def set_unlock_time(dt: datetime):
    api_data = {
        "LockboxApiKey": box_key,
        "DateTime": dt.isoformat(),
        "UseLocal": "False"
    }

    res = requests.post("https://do.pishock.com/pivaultapi/setunlocktime", data=json.dumps(api_data),
                        auth=HTTPBasicAuth(user_name, user_key), headers=api_headers)
    print_response(res)


def unlock(manual: bool = True):
    if manual:
        mode = 1
    else:
        mode = 0

    api_data = {
        "LockboxApiKey": box_key,
        "Mode": str(mode),
        "Buzz": "False",
        "IgnoreTimer": "False"
    }

    res = requests.post("https://do.pishock.com/pivaultapi/unlock", data=json.dumps(api_data),
                        auth=HTTPBasicAuth(user_name, user_key), headers=api_headers)
    print_response(res)


def unlock_delayed(delay_secs: int = None):
    api_data = {
        "LockboxApiKey": box_key,
        "Mode": "2",
        "Seconds": str(delay_secs),
        "Buzz": "False",
        "IgnoreTimer": "False"
    }

    res = requests.post("https://do.pishock.com/pivaultapi/unlock", data=json.dumps(api_data),
                        auth=HTTPBasicAuth(user_name, user_key), headers=api_headers)
    print_response(res)


def clear():
    api_data = {
        "LockboxApiKey": box_key,
    }

    res = requests.post("https://do.pishock.com/pivaultapi/clear", data=json.dumps(api_data),
                        auth=HTTPBasicAuth(user_name, user_key), headers=api_headers)
    print_response(res)


def print_status():
    from datetime import datetime as dt

    res = requests.get("https://do.pishock.com/pivaultapi/getpivaultinfo?lockboxapikey=" + box_key,
                       auth=HTTPBasicAuth(user_name, user_key))
    json = res.json()
    try:
        print(f"lockbox name: {json['name']}")
        print(f"online: {json['online']}")
        print(f"canUnlock: {json['canUnlock']}")
        print(f"no-keyholder mode: {json['selfLocking']}")

        last_polled = json['lastPolled']
        if last_polled:
            print(f"lastPolled: {dt.fromisoformat(last_polled).astimezone()}")

        locked_since = json['lockedSince']
        if locked_since:
            print(f"lockedSince: {dt.fromisoformat(locked_since).astimezone()}")

        locked_until = json['lockedUntil']
        if locked_until:
            if not str.isalpha(locked_until[:-1]):
                locked_until += 'Z'
            print(f"lockedUntil: {dt.fromisoformat(locked_until).astimezone()}")
    except Exception as e:
        print("Response: %s" % e)
        raise e


def print_response(res):
    if res.content:
        print(res.content.decode("utf-8", "replace"))
    else:
        print("status code", res.status_code)


if __name__ == '__main__':
    main()
