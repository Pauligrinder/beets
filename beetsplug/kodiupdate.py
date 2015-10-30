"""Updates a Kodi library whenever the beets library is changed.

This requires the pyjsonrpc-library, which can be installed using this command:
	
	pip install python-jsonrpc

I tested this using Kodi 15.2 running on an Arch Linux virtual machine, with beets 1.3.14 running on Windows 10.

Put something like the following in your config.yaml to configure:
    kodi:
        host: localhost
        port: 8080
		user: user
		pwd: secret
"""
import pyjsonrpc
from beets import config
from beets.plugins import BeetsPlugin


def update_kodi(host, port, user, pwd):
    """Sends request to the Kodi api to start a library refresh.
    """
    http_client = pyjsonrpc.HttpClient(
    url = "http://{0}:{1}/jsonrpc".format(host, port),
    username = user,
    password = pwd)
	
    return http_client.call("AudioLibrary.Scan")

class KodiUpdate(BeetsPlugin):
    def __init__(self):
        super(KodiUpdate, self).__init__()

        # Adding defaults.
        config['kodi'].add({
            u'host': u'localhost',
            u'port': 8080,
            u'user': u'username',
            u'pwd': u'password'})

        self.register_listener('database_change', self.listen_for_db_change)

    def listen_for_db_change(self, lib, model):
        """Listens for beets db change and register the update for the end"""
        self.register_listener('cli_exit', self.update)

    def update(self, lib):
        """When the client exists try to send library update request to Kodi.
        """

	try:
		update_kodi(
			config['kodi']['host'].get(),
			config['kodi']['port'].get(),
			config['kodi']['user'].get(),
			config['kodi']['pwd'].get())
		self._log.info('... started.')
	
	except:
		self._log.warning("Failed to update your Kodi library. Please check your settings and Kodi setup!")
	
