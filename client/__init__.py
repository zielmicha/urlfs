__author__="michal"
__date__ ="$2010-09-27 20:49:15$"

import urlfs

clients = {}

def register_client(proto, fs):
	clients[proto] = fs

def get(url):
	if isinstance(url, urlfs.FS):
		return url
	if not isinstance(url, urlfs.URL):
		url = urlfs.URL(url)
	#else: url = url
	proto = url.proto
	assert url.absolute
	try:
		client = clients[proto]
	except KeyError:
		raise IOError('Protocol %r not found.' % proto)
	return client(url)

def lazy_client(proto, module):
	def proto_wrapper(url):
		del clients[proto]
		__import__(module)
		return get(url)
	register_client(proto, proto_wrapper)