import requests
import os
import sys
from urllib.parse import urlparse
import time

PROXY_TOKEN = os.environ['PROXY_TOKEN']
PROXY_API_URL = os.environ['PROXY_API_URL']
MAX_RETRIES = os.environ.get("MAX_RETRIES", 10)
WEBDAV_PORT = os.environ.get("WEBDAV_PORT", 8081)
SYNC_TIMEOUT = os.environ.get('SYNC_TIMEOUT', 5)

def run():
  retries = 0
  time.sleep(5)
  while True:
    res = requests.get(os.path.join(PROXY_API_URL, "api/routes"), headers={'Authorization': 'token %s' % PROXY_TOKEN})
    if res.status_code != 200:
      retries += 1
      if retries >= MAX_RETRIES:
        sys.exit(1)

    data = res.json()
    users = []
    for key, val in data.items():
        if key.startswith("/user") and not key.endswith("webdav"):
          webdav_route = data.get(os.path.join(key, "webdav"))
          if webdav_route:
            webdav_hostname = urlparse(webdav_route['target'])
            current_hostname = urlparse(val['target'])
            if webdav_hostname.hostname != current_hostname.hostname:
              users.append((key, "update"))
          else:
            users.append((key, "add"))
        else:
          try:
            if users[users.remove(key[:-7])][1] != "update":
              users.remove(key[:-7])
          except ValueError as e:
            #Delete public route for non-existent user!
            pass

    if len(users) > 0:
      for user in users:
        target = urlparse(data[user[0]]["target"])
        print(target)
        new_target_url = "%s://%s:%s/%s" % (target.scheme, target.hostname, str(WEBDAV_PORT), "webdav")
        print(os.path.join(PROXY_API_URL, "api/routes", user[0], "webdav"))
        res_post = requests.post(os.path.join(PROXY_API_URL, "api/routes", user[0].strip("/"), "webdav"), json={"target": new_target_url}, headers={'Authorization': 'token %s' % PROXY_TOKEN})
        if res_post.status_code != 201:
          print("Failed to create route for %s" % user)

    time.sleep(SYNC_TIMEOUT)
