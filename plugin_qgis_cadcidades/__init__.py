def classFactory(iface):
    """
    Load and return an instance of the plugin's main class.
    """
    from .main import CADCidades
    return CADCidades(iface)