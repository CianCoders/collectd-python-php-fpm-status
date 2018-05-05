# collectd-python-php-fpm-status

PHP-FPM status monitor for collectd

## INSTALLATION

1.  Place phpfpm.py in your CollectD python plugins directory, for example `/usr/local/lib/collectd/python/`
2.  Configure the plugin in CollectD (see below)
3.  Restart CollectD

## COLLECTD CONFIGURATION

Edit your `/etc/collectd/collectd.conf` file, it should look like this:

    LoadPlugin python
    <Plugin python>
        ModulePath "/usr/local/lib/collectd/python"
        Import "phpfpm"
        <Module phpfpm>
                Url "http://127.0.0.2/pool1_status?json&full"
        </Module>
        <Module phpfpm>
                Url "http://127.0.0.2/pool2_status?json&full"
        </Module>
        <Module phpfpm>
                Url "http://127.0.0.2/poolN_status?json&full"
        </Module>
    </Plugin>

You can add as many Module instances as you whish, each one points to a different server url

## DATA FORMAT

The data is collected using the format:

`phpfpm.pool.gauge.metric` for the master process
`phpfpm.pool.process-N.gauge.metric` for each process

##Enjoy!
