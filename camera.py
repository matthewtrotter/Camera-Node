# Author: Matthew Trotter
# Copyright 2021

from pathlib import Path
import tempfile
import urllib3

import logging
import logging.config
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('camera')


class Camera:
    def __init__(self, local_storage_dir: Path) -> None:
        self.local_storage_dir = Path(local_storage_dir)

    def take_picture(self) -> Path:
        """Take a new picture and return the filepath

        Returns
        -------
        newfile
            Path of the new picture
        """
        
        random_pic_url = 'https://picsum.photos/2592/1944'  # Random picture at same resolution as Rpi camera

        newfile = tempfile.mkstemp(dir=self.local_storage_dir)
        newfile = Path(newfile[1])
        with urllib3.PoolManager() as http:
            with open(newfile, 'wb') as fp:
                r = http.request('GET', random_pic_url)
                fp.write(r.data)
        logger.info(f'Took new picture: {newfile}')
        return newfile

            


