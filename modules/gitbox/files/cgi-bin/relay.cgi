#!/usr/bin/env python3

import requests
import yaml
import json
import os
import sys
import fnmatch

YAML_PATH = "/x1/gitbox/conf/relay.yaml"
YML = yaml.load(open(YAML_PATH))

PAYLOAD = json.load(sys.stdin)
PAYLOAD_FORMDATA = {
    'payload': json.dumps(PAYLOAD)
}

HEADERS = {
    'User-Agent': os.environ.get('HTTP_USER_AGENT', 'GitHub-Hookshot/abcd'),
    'X-GitHub-Delivery': os.environ.get('HTTP_X_GITHUB_DELIVERY',""),
    'X-GitHub-Event': os.environ.get('HTTP_X_GITHUB_EVENT', "push")
  }


# determine what and where
repo = PAYLOAD['repository']['name']
what = 'commit'
if 'pull_request' in PAYLOAD:
    what = 'pr'
elif 'issue' in PAYLOAD:
    what = 'issue'

for key, entry in YML['relays'].items():
    if fnmatch.fnmatch(repo, entry['repos']): # If yaml entry glob-matches the repo, then...
        hook = entry.get('hook') # Hook URL to post to
        fmt = entry.get('format', 'formdata') # www-formdata or raw json expected by hook?
        wanted = entry.get('events', 'all') # Which events to trigger on; all, pr, issue, commit or a mix.
        enabled = entry.get('enabled', False) # Default to false, so we don't trigger bootstrap example
        try:
            if enabled and hook and (wanted == 'all' or what in wanted):
                if fmt == 'formdata':
                    rv = requests.post(hook, data = PAYLOAD_FORMDATA, headers = HEADERS)
                elif fmt == 'json':
                    rv = requests.post(hook, json = PAYLOAD, headers = HEADERS)
                sys.stderr.write("Delivered %s payload for %s to %s: %u\n" % (what, repo, hook, rv.status_code))
        except:
            pass # fail silently if hook doesn't respond well

print("Status: 204 Handled\r\n\r\n")
