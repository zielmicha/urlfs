import errno

io_causes = {
	'NotFound': errno.ENOENT,
	None: errno.EIO
}

def io_error(cause, *args):
	raise IOError(io_causes[cause], *args)

class FileLike(object):
	
	def readline(self):
		list = []
		while True:
			ch = self.read(1)
			list.append(ch)
			if ch == '\n' or ch == '\r':
				return ''.join(list)
		return ''.join(list)

	def __iter__(self):
		while True:
			line = self.readline()
			if not line:
				return
			yield line

	