__author__="michal"
__date__ ="$2010-09-27 16:20:16$"

from urlfs.tools import abstractmethod, rich_repr
from urlfs.url import URL
from urlfs.client import register_client, get, lazy_client
from urlfs.fs import BaseFS, FS, Attrs
from urlfs.utils import io_error, FileLike

# load protocols

import urlfs.client.file

lazy_client('http', 'urlfs.client.http')
lazy_client('gio', 'urlfs.client.gio')