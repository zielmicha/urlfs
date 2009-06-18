
__author__="michal"
__date__ ="$2009-06-18 17:37:59$"

import urlparser
import os

def _os_to_url(path):
    return '/'.join(urlparse.norm_path(path.split(os.path.sep)))

def _url_to_os(path):
    return os.path.join(urlparse.split_path(path))

class Client:
    def __init__(self, root, asroot=True):
        self.asroot = asroot
        self.root = _os_to_url(root)
    def _path(self, path):
        if self.asroot:
            path = urlparser.norm_path(path)
        return _url_to_os(self.root + '/' + path)
    def chmod(self, path, mod):
        os.chmod(self._path(path), mod)
    def chown(self, path, user, group):
        os.chown(self._path(path), user, group)
    def lchmod(self, path, mod):
        os.lchmod(self._path(path), mod)
    def lchown(self, path, user, group):
        os.lchown(self._path(path), user, group)
    def mkdir(self, path, mod):
        os.mkdir(self._path(path), mod)
    def open(self, path, mod = 'r'):
        return open(self._path(path), mod)
    def access(self, path, mode):
        return os.access(self._path(path), mode)
    def chflags(self, path, flags):
        return os.chflags(self._path(path), flags)
    def link(self, src, dst):
        return os.link(self._path(src), self._path(dst))
    def listdir(self, path):
        return os.listdir(self._path(path))
    def lstat(self, path):
        return os.lstat(self._path(path))
    def mkfifo(self, path, mode):
        os.mkfifo(self._path(path), mode)
    def mknod(self, path, mode):
        os.mkdev(self._path(path), mode)
    def major(self, path):
        return os.major(self._path(path))
    def minor(self, path):
        return os.minor(self._path(path))
    def makedev(self, path, major, minor):
        os.makedev(self._path(path), major, minor)
    def 
    