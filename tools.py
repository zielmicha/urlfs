
def abstractmethod(method):
	def wmethod(*args, **kwargs):
		raise RuntimeError('Not implemented.')
	wmethod.__doc__ = method.__doc__
	wmethod.__name__ = method.__name__
	return wmethod

def rich_repr(obj):
	attrs = (
		(k, v) for k, v in
		(
			(k, getattr(obj, k)) for k in dir(obj)
			if not (k.startswith('_') or k == k.upper())
		)
		if not callable(v)
	)
	return '<%s.%s %s at 0x%x>' % (
		obj.__class__.__module__, obj.__class__.__name__,
		' '.join( '%s=%r' % (k, v) for k, v in attrs),
		id(obj)
	)

	