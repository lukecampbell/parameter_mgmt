

class ModelObject(object):
    def __init__(self, *args, **kwargs):
        for k,v in kwargs.iteritems():
            if hasattr(self,k):
                setattr(self,k,v)

    def schema(self):
        retval = {}
        for k,v in self.__dict__.iteritems():
            if callable(v):
                continue
            if '__' in k:
                continue
            retval[k] = type(v).__name__
        return retval
