__author__="michal"
__date__ ="$2010-09-27 21:11:06$"

import os
import platform
import stat as statlib

import urlfs

is_windows = platform.system() == 'Windows'

class FileFS(urlfs.BaseFS):
	def init(self):
		self.path = _url2path(self.url)
		assert not self.url.host, "Host given"
	
	def open(self, mode):
		return open(self.path, mode + 'b')

	def remove(self):
		os.remove(self.path)

	def attrs(self):
		stat = os.stat(self.path)
		def get(name):
			name = 'st_' + name
			return getattr(stat, name, None)
		winctime = get('ctime') if is_windows else None
		return urlfs.Attrs(
			created_time=winctime or get('birthtime'),
			modified_time=get('mtime'),
			attr_time=get('mtime') if not is_windows else None,
			accessed_time=get('atime'),
			mode=get('mode'), owner=get('uid'), group=get('gid'),
			type=statlib.S_IFMT(get('mode')), size=get('size')
		)

	def put_attrs(self, created_time=None, modified_time=None, accessed_time=None,
		attr_time=None, mod=None, owner=None, group=None):
			if accessed_time or modified_time:
				if not accessed_time:
					accessed_time = self.attrs().accessed_time
				if not modified_time:
					modified_time = self.attrs().modified_time
				os.utime(self.path, (accessed_time, modified_time))
			if mod:
				os.chmod(self.path, mod)
			if owner or group:
				if not owner:
					owner = self.attrs().owner
				if not group:
					group = self.attrs().group
				os.chown(self.path, owner, group)
			if created_time or attr_time:
				return True

	def symlink(self, dest):
		os.symlink(self.path, FileFS.get_path(dest))

	def move(self, dest):
		os.rename(self.path, FileFS.get_path(dest))

	def remove_dir(self):
		os.rmdir(self.path)

	def create_dir(self):
		os.mkdir(self.path)

	def read_link(self):
		return os.readlink(self.path)

	def list(self):
		return os.listdir(self.path)

	def exists(self):
		return os.access(self.path, os.F_OK)

	@staticmethod
	def get_path(instance):
		if not isinstance(instance, FileFS):
			urlfs.io_error(None, 'Cannot perform this operation on non-local files', instance.url)
		return instance.path

def _url2path(url):
	path = os.path.join(*url.path.split('/'))
	if url.path.startswith('/'):
		path = os.sep + path
	return path

urlfs.register_client('file', FileFS)






