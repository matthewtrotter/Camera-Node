# Author: Matthew Trotter
# Copyright 2021

from pathlib import Path

import logging
import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('updater')


class Updater:
    def __init__(self) -> None:
        pass

    def update(self, url: str):
        """Download the new code, install, and reboot the system

        Parameters
        ----------
        url : str
            URL of the new code.
        """
        raise NotImplementedError
