from collections import OrderedDict
from model_object import ModelObject
class Parameter(ModelObject):
    _id            = 0
    name           = ''
    parameter_type = ''
    value_encoding = ''
    code_set       = ''
    uom            = ''
    fill_value     = ''
    display_name   = ''
    standard_name  = ''
    long_name      = ''
    data_product   = ''

    def __init__(self, 
            _id=0,
            name='',
            parameter_type='',
            value_encoding='',
            code_set='',
            uom='',
            fill_value='',
            display_name='',
            standard_name='',
            long_name='',
            data_product='',
            **kwargs):
        ModelObject.__init__(self,**kwargs)
        self._id            = _id
        self.name           = name
        self.parameter_type = parameter_type
        self.value_encoding = value_encoding
        self.code_set       = code_set
        self.uom            = uom
        self.fill_value     = fill_value
        self.display_name   = display_name
        self.standard_name  = standard_name
        self.long_name      = long_name
        self.data_product   = data_product

    def schema(self):
        return OrderedDict([
            ('_id'            , self._id),
            ('name'           , self.name),
            ('parameter_type' , self.parameter_type),
            ('value_encoding' , self.value_encoding),
            ('code_set'       , self.code_set),
            ('uom'            , self.uom),
            ('fill_value'     , self.fill_value),
            ('display_name'   , self.display_name),
            ('standard_name'  , self.standard_name),
            ('long_name'      , self.long_name),
            ('data_product'   , self.data_product),
            ])

    def iteritems(self):
        for k,v in self.schema().iteritems():
            yield k, v
        return

