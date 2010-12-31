import urlfs
from urlfs import abstractmethod

class FS(object):
	''' Base class for any filesystem/protocol.'''

class BaseFS(FS):
	def __init__(self, url):
		self.url = urlfs.URL(url)
		self.init()

	def init(self):
		pass

	def open(self, mode):
		if mode == 'w':
			return self.open_stream(writeable=1, trunc=1)
		elif mode == 'w+':
			return self.open_stream(writeable=1, readable=1, trunc=1)
		elif mode == 'r':
			return self.open_stream(readable=1)
		elif mode == 'r+':
			return self.open_stream(readable=1, writeable=1)
		elif mode == 'a':
			return self.open_stream(writeable=1, append=1)
		elif mode == 'a+':
			return self.open_stream(writeable=1, readable=1, append=1)
		raise ValueError('Invalid mode.')

	#@abstractmethod
	def open_stream(self, readable=0, writeable=0, trunc=0, append=0):
		def invalid():
			raise ValueError('Invalid mode.')
		if trunc:
			if not writeable:
				invalid()
			if append:
				invalid()
			if readable:
				return self.open('w+')
			else:
				return self.open('w')
		if append:
			if not writeable:
				invalid()
			if readable:
				return self.open('a+')
			else:
				return self.open('a')
		if writeable:
			return self.open('r+')
		else:
			return self.open('r')


	@abstractmethod
	def remove(self):
		pass

	@abstractmethod
	def attrs(self):
		pass

	@abstractmethod
	def put_attrs(self, created_time=None, modified_time=None, accessed_time=None,
		attr_time=None, mode=None, owner=None, group=None):
		'''
		Returns true if any of requested attributes was not set.
		Example: put_attrs(owner=0)
		'''

	@abstractmethod
	def symlink(self, dest):
		pass

	@abstractmethod
	def move(self, dest):
		pass

	def copy(self, dest):
		in_stream = self.open('r')
		dest_stream = urlfs.get(dest).open('w')
		BLOCK_SIZE = 1024
		while True:
			chunk = in_stream.read(BLOCK_SIZE)
			if not chunk: break
			dest_stream.write(chunk)

	@abstractmethod
	def remove_dir(self):
		pass

	@abstractmethod
	def create_dir(self):
		pass

	@abstractmethod
	def read_link(self):
		pass

	def read(self):
		try:
			f = self.open('r')
			return f.read()
		finally:
			f.close()

	def write(self, content):
		try:
			f = self.open('w')
			f.write(content)
		finally:
			f.close()

	@abstractmethod
	def list(self):
		pass

	def list_files(self):
		return [ self.child(name) for name in self.list() ]

	@abstractmethod
	def exists(self):
		pass

	def child(self, path):
		return type(self)(self.url.join(path))

#	def set_host(self, hostname):
#		if hostname:
#			raise RuntimeError('Hostname in URL not implemented by this protocol.')
#
#class RequiresHost(FS):
#	def __init__(self, func):
#		self.set_host = func
#	def __getattr__(self, name):
#		raise AttributeError('This protocol should have hostname in URL.')

class Attrs(object):
	def __init__(self, created_time=None, modified_time=None, accessed_time=None,
		attr_time=None, mode=None, owner=None, group=None, size=None,
		type=None):
			self.created_time = created_time
			self.modified_time = modified_time
			self.accessed_time = accessed_time
			self.attr_time = attr_time
			self.mode = mode
			self.owner = owner
			self.group = group
			self.size = size
			self.type = type
	
	DIR = 0o040000
	CHAR_DEV = 0o020000
	BLOCK_DEV = 0o060000
	FILE = 0o100000
	FIFO = 0o010000
	LINK = 0o120000
	SOCKET = 0o140000

	def apply_to(self, url):
		'''
		Sets attributes of url using put_attrs method
		'''
		urlfs.get(url).put_attrs(created_time=self.created_time, group=self.group,
			modified_time=self.modified_time, attr_time=self.attr_time,
			accessed_time=self.accessed_time, mode=self.mode, owner=self.owner
		)

	def __repr__(self):
		return urlfs.rich_repr(self)













