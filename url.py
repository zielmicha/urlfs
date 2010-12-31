
import re

ABSOLUTE_URL = re.compile('^([a-bA-B0-9]+):(.*)')

class URL(object):
	def __new__(cls, url):
		if isinstance(url, URL):
			return url
		if url.startswith('/'):
			return HalfRelativeURL.create(url)
		split = url.split(':', 1)
		if len(split) == 2 and '/' not in split[0]:
			return AbsoluteURL.create(url)
		return RelativeURL.create(url)

	@classmethod
	def create(cls, url):
		self = object.__new__(cls)
		self.url = url
		self.init()
		return self

	def init(self):
		self.host = None
		self.rest = None
		self.path = self.url
		self.proto = None

	def join(self, other):
		if isinstance(other, RelativeURL):
			return RelativeURL(_join_path(self.path, other.path)[1:])
		if isinstance(other, AbsoluteURL):
			return other
		if isinstance(other, HalfRelativeURL):
			return other
		return self.join(URL(other))

	def __str__(self):
		return self.url

	def __repr__(self):
		return 'URL:' + self.url

class AbsoluteURL(URL):
	absolute = True
	relative = False
	def init(self):
		self.proto, self.rest = self.url.split(':', 1)
		if self.rest.startswith('//'):
			if '/' not in self.rest[2:]:
				self.rest += '/'
			self.host, self.path = self.rest[2:].split('/', 1)
		else:
			self.host = ''
			self.path = self.rest
		if not self.path.startswith('/'):
			self.path = '/' + self.path

	def join(self, other):
		if isinstance(other, RelativeURL):
			return AbsoluteURL('%s://%s%s' % (self.proto, self.host, _join_path(self.path, other.path)))
		if isinstance(other, AbsoluteURL):
			return other
		if isinstance(other, HalfRelativeURL):
			return AbsoluteURL('%s://%s%s' % (self.proto, self.host, other.path))
		return self.join(URL(other))

	def relative_to(self, other):
		'''
		Example:
		URL('foo://example.com/foo').relative_to('foo://example.com/') = 'foo'
		'''
		if isinstance(other, AbsoluteURL):
			if self.proto == other.proto and self.host == other.host:
				return RelativeURL(_relative_path_to(self.path, other.path))
			else:
				return self
		elif isinstance(other, basestring):
			return self.relative_to(URL(other))
		else:
			raise ValueError('Cannot make relative url from non absolute urls.')
	
	def get(self):
		''' Equalivment to urlfs.get(self)  '''
		return urlfs.get(self)

class RelativeURL(URL):
	relative = True
	absolute = False

class HalfRelativeURL(URL):
	relative = True
	absolute = False

def _join_path(a, b):
	a_parts = a.split('/')
	a_parts.pop() # /a/b/c > /a/b ; /a/b/ > /a/b
	parts = []
	for part in a_parts + b.split('/'):
		if part == '..':
			if parts: parts.pop()
		elif part != '' and part != '.':
			parts.append(part)
	return '/' + '/'.join(parts)

def _get_path_parts(p):
	parts = []
	for part in p.split('/'):
		if part == '..':
			if parts: parts.pop()
		elif part != '' and part != '.':
			parts.append(part)
	return parts + ([] if not p.endswith('/') else [''])

def _relative_path_to(a, b):
	parts_a = _get_path_parts(a)
	parts_b = _get_path_parts(b)
	i = 0
	for part_a, part_b in zip(parts_a, parts_b):
		if part_a != part_b: break
		i += 1
	out = ['..'] * (len(parts_a) - i - 1)
	out += parts_b[i:]
	return '/'.join(out)

















