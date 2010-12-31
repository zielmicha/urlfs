import urlfs

import httplib

class HttpFS(urlfs.BaseFS):
	def open_stream(self, readable=0, writeable=0, trunc=0, append=0):
		if writeable or trunc or append:
			raise IOError('Read-only filesystem.')
		assert readable, 'Invalid mode.'
		conn = httplib.HTTPConnection(self.url.host)
		conn.request('GET', self.url.path)
		resp = conn.getresponse()
		if resp.status != 200:
			if resp.status == 404:
				urlfs.io_error('NotFound', 'HTTP 404', self.url)
			else:
				urlfs.io_error(None, 'HTTP %d' % resp.status, self.url)
		return HttpStream(resp, conn)

class HttpStream(urlfs.FileLike):
	def __init__(self, resp, conn):
		urlfs.FileLike.__init__(self)
		self.resp = resp
		self.conn = conn

	def close(self):
		self.conn.close()

	def read(self, i=None):
		if i == None:
			content = self.resp.read()
			self.conn.close()
			return content
		else:
			return self.resp.read(i)

urlfs.register_client('http', HttpFS)