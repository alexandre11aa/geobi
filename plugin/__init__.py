from .geobi_plugin import GeoBi

def classFactory(iface):

    return GeoBi(iface)
