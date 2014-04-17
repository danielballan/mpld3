import os
import shutil
import warnings
from functools import wraps
from . import urls

# Make sure that DeprecationWarning gets printed
warnings.simplefilter("always", DeprecationWarning)


def get_id(obj, suffix=None):
    """Get a unique id for the object"""
    objid = str(os.getpid()) + str(id(obj))
    if suffix:
        objid += str(suffix)
    return objid


def deprecated(func, old_name, new_name):
    """Decorator to mark functions as deprecated."""
    @wraps(func)
    def new_func(*args, **kwargs):
        warnings.warn(("{0} is deprecated and will be removed.  "
                       "Use {1} instead".format(old_name, new_name)),
                      category=DeprecationWarning)
        return func(*args, **kwargs)
    new_func.__doc__ = ("*%s is deprecated: use %s instead*\n\n    "
                        % (old_name, new_name)) + new_func.__doc__
    return new_func


def write_js_libs(location=None, d3_src=None, mpld3_src=None):
    """
    Write the mpld3 and d3 javascript libraries to the given file location.

    This utility is used by the IPython notebook tools to enable easy use
    of mpld3 with no web connection.

    Parameters
    ----------
    location : string (optioal)
        the directory in which the d3 and mpld3 javascript libraries will be
        written. If not specified, the IPython nbextensions directory will be
        used. If IPython doesn't support nbextensions (< 2.0),
        the current working directory will be used.
    d3_src : string (optional)
        the source location of the d3 library. If not specified, the standard
        path in mpld3.urls.D3_LOCAL will be used.
    mpld3_src : string (optional)
        the source location of the mpld3 library. If not specified, the
        standard path in mpld3.urls.MPLD3_LOCAL will be used.    

    Returns
    -------
    d3_url, mpld3_url : string
        The URLs to be used for loading these js files.
    """
    if location is None:
        try:
            from IPython.html import install_nbextension
        except ImportError:
            location = os.getcwd()
            nbextension = False
        else:
            nbextension = True
    else:
        nbextension = False
    
    if d3_src is None:
        d3_src = urls.D3_LOCAL
    if mpld3_src is None:
        mpld3_src = urls.MPLD3_LOCAL

    d3js = os.path.basename(d3_src)
    mpld3js = os.path.basename(mpld3_src)

    if not os.path.exists(d3_src):
        raise ValueError("d3 src not found at '{0}'".format(d3_src))
    if not os.path.exists(mpld3_src):
        raise ValueError("mpld3 src not found at '{0}'".format(mpld3_src))

    if nbextension:
        install_nbextension([d3_src, mpld3_src])
        prefix = 'nbextensions/'
    else:
        # IPython < 2.0 or explicit path.
        # This won't work if users have changed the kernel directory.
        d3_dest = os.path.join(location, d3js)
        mpld3_dest = os.path.join(location, mpld3js)

        shutil.copyfile(d3_src, d3_dest)
        shutil.copyfile(mpld3_src, mpld3_dest)

        prefix = '/files/'

    return prefix + d3js, prefix + mpld3js

