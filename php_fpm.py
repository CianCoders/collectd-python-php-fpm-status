#!/usr/bin/env python
import sys
import urllib
import json

COLLECTD_ENABLED = True
try:
    if COLLECTD_ENABLED:
        import collectd
except ImportError:
    # We're not running in CollectD, set this to False so we can make some changes
    # accordingly for testing/development.
    COLLECTD_ENABLED = False
import re

# default config
CONFIG = {
    'url': 'http://localhost/status?json&full'
}

# gauge: store as is
# derive: store the change over time
TYPES = {
    'start since': 'gauge',
    'accepted conn': 'derive',
    'listen queue': 'gauge',
    'max listen queue': 'gauge',
    'listen queue len': 'gauge',
    'idle processes': 'gauge',
    'active processes': 'gauge',
    'total processes': 'gauge',
    'max active processes': 'gauge',
    'max children reached': 'gauge',
    'slow requests': 'derive',
    'requests': 'gauge',
    'request duration': 'gauge',
    'content length': 'gauge',
    'last request cpu': 'gauge',
    'last request memory': 'gauge',
}


def configure_callback(conf):
    global CONFIG
    for node in conf.children:
        if node.key in CONFIG:
            CONFIG[node.key] = node.values[0]


def dispatch(pool, metric, value, metric_type, process=None):
    if process is None:
        plugin = 'fcm.{}.{}'.format(pool, metric)
    else:
        plugin = 'fcm.{}.process{}.{}'.format(pool, process, metric)
    plugin = plugin.replace(' ', '_')

    if COLLECTD_ENABLED:
        vl = collectd.Values(plugin=plugin, type=metric_type)
        vl.dispatch(values=[value])
    else:
        print 'dispatch: {} type: {} value: {}'.format(
            plugin, metric_type, value)


def read_callback():
    global CONFIG
    url = CONFIG['url']
    response = urllib.urlopen(url)
    data = json.loads(response.read())

    # read master metrics
    pool = data['pool']
    for metric in [m for m in data.keys() if m in TYPES]:
        dispatch(pool, metric, data[metric], TYPES[metric])

    # read each prcess metrics
    if 'processes' in data.keys():
        i = 0
        for process in data['processes']:
            for metric in [m for m in process.keys() if m in TYPES]:
                dispatch(pool, metric,
                         process[metric], TYPES[metric], process=i)
            i += 1


if COLLECTD_ENABLED:
    collectd.register_read(read_callback)
    collectd.register_config(configure_callback)

if __name__ == "__main__" and not COLLECTD_ENABLED:
    from pprint import pprint as pp
    CONFIG['url'] = sys.argv[1]

    print "Running in test mode, invoke with"
    print sys.argv[0] + " URL"

    print "\n\nCONFIG:"
    pp(CONFIG)
    print

    read_callback()
