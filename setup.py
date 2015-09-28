# Copyright (c) Jupyter Development Team.
# Distributed under the terms of the Modified BSD License.

import os
from setuptools import setup, find_packages
from setuptools.command.install import install

from IPython.html.nbextensions import install_nbextension
from IPython.html.services.config import ConfigManager

VERSION_FILE = os.path.join(os.path.dirname(__file__), 'VERSION')
EXT_DIR = os.path.join(os.path.dirname(__file__), 'urth_widgets')
SERVER_EXT_CONFIG = "c.NotebookApp.server_extensions.append('urth.widgets.urth_import')"

class InstallCommand(install):
    def run(self):
        print('Installing Python module')
        install.run(self)

        print('Installing notebook extension')
        install_nbextension(EXT_DIR, overwrite=True, user=True)
        cm = ConfigManager()
        print('Enabling extension for notebook')
        cm.update('notebook', {"load_extensions": {'urth_widgets/js/main': True}})

        print('Installing notebook server extension')
        fn = os.path.join(cm.profile_dir, 'ipython_notebook_config.py')

        if os.path.isfile(fn):
            with open(fn, 'r+') as fh:
                lines = fh.read()
                if SERVER_EXT_CONFIG not in lines:
                    fh.seek(0, 2)
                    fh.write('\n')
                    fh.write(SERVER_EXT_CONFIG)
        else:
            with open(fn, 'w') as fh:
                fh.write('c = get_config()\n')
                fh.write(SERVER_EXT_CONFIG)

# Apply version to build
VERSION = '0.1'
if os.path.isfile(VERSION_FILE):
    # CI build, read metadata and append
    with open(VERSION_FILE, 'r') as fh:
        BUILD_INFO = fh.readline().strip()
    BUILD_NUM, _ = BUILD_INFO.split('-')
    VERSION += '.dev' + BUILD_NUM
else:
    # Local development build
    VERSION += '.dev0'

setup(
    name='urth-widgets-nbexts',
    author='Jupyter Community',
    maintainer='Jupyter Community',
    description='IPython / Jupyter extensions for supporting declarative widgets',
    version=VERSION,
    license='BDS',
    platforms=['IPython Notebook 3.x'],
    packages=find_packages(),
    include_package_data=True,
    install_requires=[],
    cmdclass={
        'install': InstallCommand
    }
)
