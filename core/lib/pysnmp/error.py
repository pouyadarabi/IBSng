"""
   PySNMP exceptions classes.

   Written by Ilya Etingof <ilya@glas.net>, 2001, 2002. Suggested by
   Case Van Horsen <case@ironwater.com>.
"""   
import exceptions

class Generic(exceptions.Exception):
    """Base class for PySNMP error handlers
    """
    def __init__(self, err_msg=None):
        """
        """
        self.err_msg = err_msg

    def __str__(self):
        """
        """
        return self.err_msg

    def __repr__(self):
        """
        """
        return self.__class__.__name__ + '(' + self.err_msg + ')'
