import yaml
import pkg_resources
import pmgmt

def read_config(config_path=''):
    path = config_path or pkg_resources.resource_filename(pmgmt.__name__,'resources/config.yml')
    retval = {}

    with open(path,'r') as f:
        retval = yaml.load(f.read())

    def walk(ob):
        if isinstance(ob,basestring):
            if '$' in ob:
                return pkg_resources.resource_filename(pmgmt.__name__,ob.split('$/')[1])
        if hasattr(ob,'__iter__'):
            if isinstance(ob,dict):
                return {k:walk(v) for k,v in ob.iteritems()}
            return [walk(i) for i in ob]
        return ob
    retval = walk(retval)
    return retval



