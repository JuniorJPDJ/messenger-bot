import os
import importlib
import logging

__author__ = 'JuniorJPDJ'

logger = logging.getLogger(__name__)


class PluginLoader(object):
    def __init__(self, plugins_dir='plugins', plugin_main='__plugin__', *plugin_args, **plugin_kwargs):
        self.plugins_dir, self.plugin_main, self._plugins = plugins_dir, plugin_main, {}
        self.plugin_args, self.plugin_kwargs = plugin_args, plugin_kwargs

    def load_plugins(self):
        logger.debug('Plugins loading started')
        plugins_dir = os.path.join(os.path.split(os.path.abspath(__file__))[0], self.plugins_dir)
        for i in os.listdir(plugins_dir):
            location = os.path.join(plugins_dir, i)
            if i.startswith('!') or not (os.path.isdir(location) and '__init__.py' in os.listdir(location)):
                continue
            plugin = getattr(importlib.import_module('.{}.{}'.format(self.plugins_dir, i)), self.plugin_main, None)
            if plugin is None:
                continue
            logger.debug('Loading plugin started: %s', plugin.name)
            if plugin.name not in self._plugins:
                self._plugins[plugin.name] = True
                self._plugins[plugin.name] = plugin(*self.plugin_args, **self.plugin_kwargs)
                logger.debug('Loading plugin finished: %s', plugin.name)
            else:
                logger.debug('Plugin with same name already loaded: %s', plugin.name)
        logger.debug('Plugins loading finished')

    @property
    def loaded_plugins(self):
        return list(self._plugins.keys())

    def is_plugin_loaded(self, name):
        return name in self._plugins

    def get_plugin(self, name):
        if name in self._plugins:
            return self._plugins[name]
