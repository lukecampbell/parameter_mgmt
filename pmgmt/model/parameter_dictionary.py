from model_object import ModelObject
from collections import OrderedDict

class ParameterDictionary(ModelObject):
    _id         = 0
    name        = ''
    temporal_id = 0
    parameters  = []
    def __init__(self, _id=0, name='', temporal_id='', **kwargs):
        ModelObject.__init__(self,**kwargs)
        self._id         = _id
        self.name        = name
        self.temporal_id = temporal_id


    def schema(self):
        return OrderedDict([
                ('_id'         , self._id),
                ('name'        , self.name),
                ('temporal_id' , self.temporal_id),
                ('parameters'  , self.parameters),
            ])

    def iteritems(self):
        for k,v in self.schema().iteritems():
            yield k, v
        return

    def list_parameter_names(self):
        return ', '.join([p.name for p in self.parameters])

    def list_parameter_links(self):
        parameter_links = ["<a href='/parameter/%s'>%s</a>" % (p._id, p.name) for p in self.parameters]
        return ', '.join(parameter_links)





