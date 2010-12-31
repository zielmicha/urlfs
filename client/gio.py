import urlfs

class GIOFS(urlfs.BaseFS):
	def init(self):
		self.gio = gio.File(uri=self.url.rest)

	def open_stream(self, readable=0, writeable=0, trunc=0, append=0):
		assert not (writeable or trunc or append), 'Invalid mode'
		if readable:
			return self.gio.read()

	def remove(self):
		self.gio.delete()

	def attrs(self):
		urlfs.BaseFS.attrs(self)

	def put_attrs(self, created_time=None, modified_time=None, accessed_time=None,
		attr_time=None, mod=None, owner=None, group=None):
			urlfs.BaseFS.put_attrs(self)

	def symlink(self, dest):
		self.gio.make_symbolic_link(GIOFS.get_gfile(dest))

	def move(self, dest):
		self.gio.move(GIOFS.get_gfile(dest))

	def remove_dir(self):
		self.gio.delete()

	def create_dir(self):
		self.gio.make_directory()

	def read_link(self):
		urlfs.BaseFS.read_link(self)

	def list(self):
		urlfs.BaseFS.list(self)

	def exists(self):
		return self.gio.query_exists()

	@staticmethod
	def get_gfile(instance):
		if not isinstance(instance, GIOFS):
			urlfs.io_error(None, 'Cannot perform this operation on non-gio files', instance.url)
		return instance.gio

urlfs.register_client('gio', GIOFS)

# we can't just import gio :(

D = {}
exec 'import gio' in D
gio = D['gio']