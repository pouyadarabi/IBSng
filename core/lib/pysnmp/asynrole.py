"""
   Asynchronous SNMP manager class based on Sam Rushing's asyncore class.

   Sends and receives UDP packets asynchronously.
 
   Written by Ilya Etingof <ilya@glas.net>, 2000-2002

"""
from types import ClassType
import asyncore

# Import PySNMP components
import role, error

class Error(role.Error):
    """Base class for asynrole module
    """
    pass

class BadArgument(Error):
    """Bad argument given
    """
    pass

class manager(asyncore.dispatcher):
    """An asynchronous SNMP manager based on the asyncore.py class.

       Send and receive UDP packets asynchronously.
    """
    def __init__(self, cb_fun, cb_ctx=None, dst=None, iface=('0.0.0.0', 0)):
        # Make sure we get the callback function
        if not callable(cb_fun):
            raise BadArgument('Bad callback function')

        # Keep references to data and method objects supplied
        # by caller for callback on request completion.
        self.callback_ctx = cb_ctx
        self.callback_fun = cb_fun

        # Call parent classes constructor
        asyncore.dispatcher.__init__(self)

        # Create an instance of manager transport class
        self.manager = role.manager(dst, iface)

        # Create a socket and pass it to asyncore dispatcher
        self.set_socket(self.manager.open())

    def send(self, req, dst=None):
        """
           send(req[, dst])
           
           Send SNMP message (string) to remote server process as specified
           on manager object creation or by 'dst' address (given
           in socket module notation).

           The callback function (as specified on manager object creation)
           will be invoked on response arrival or error.
        """
        self.manager.send(req, dst)

    def handle_read(self):
        """Overloaded asyncore method -- read SNMP reply message from
           socket.        

           This does NOT time out so one needs to implement a mean of
           handling timed out requests (see examples/async_snmp.py for
           one of possible solutions).
        """
        (response, src) = self.manager.read()

        # Pass SNMP response along with references to caller specified data
        # and ourselves
        self.callback_fun(self, self.callback_ctx, (response, src),
                          (None, None, None))

    def writable(self):
        """Objects of this class never expect write events
        """
        return 0

    def handle_connect(self):
        """Objects of this class never expect connect events
        """
        pass

    def handle_close(self):
        """Invoked by asyncore on connection closed event
        """
        self.manager.close()

    def handle_error(self, exc_type, exc_value, exc_traceback):
        """Invoked by asyncore on any exception
        """
        # In case of PySNMP exception, invoke the callback function
        # and pass it an empty result. Otherwise,just pass the exception on.
        if type(exc_type) == ClassType and \
           issubclass(exc_type, error.Generic):
            self.callback_fun(self, self.callback_ctx,\
                              (None, None), (exc_type, \
                                             exc_value, exc_traceback))
        else:
            raise (exc_type, exc_value)

class agent(asyncore.dispatcher):
    """An asynchronous SNMP agent based on the asyncore.py class.

       Wait for and receive SNMP request messages, send SNMP response
       messages asynchronously.
    """
    def __init__(self, cb_fun, cb_ctx=None, ifaces=[('0.0.0.0', 161)]):
        # Make sure we get the callback function
        if not callable(cb_fun):
            raise BadArgument('Bad callback function')

        # Keep references to data and method objects supplied
        # by caller for callback on request arrival.
        self.callback_ctx = cb_ctx
        self.callback_fun = cb_fun

        # Call parent class constructor
        asyncore.dispatcher.__init__(self)

        # Create an instance of SNMP agent transport class
        self.agent = role.agent(ifaces)

        # Create a socket and pass it to asyncore dispatcher.
        self.set_socket(self.agent.open())

    def send(self, rsp, dst=None):
        """
           send(message, dst)
           
           Send SNMP message (string) to remote SNMP process by 'dst' address
           (given in socket module notation).
        """
        session.agent.send(rsp, dst)

    def handle_read(self):
        """Overloaded asyncore method -- read SNMP message from socket.

           This does NOT time out so one needs to implement a mean of
           handling timed out requests (perhaps it's worth looking at
           medusa/event_loop.py for an interesting approach).
        """
        (request, src) = self.agent.read()

        # Pass SNMP request along with references to caller specified data
        # and ourselves
        self.callback_fun(self, self.callback_ctx, (request, src),
                          (None, None, None))

    def writable(self):
        """Objects of this class never expect write events
        """
        return 0

    def handle_connect(self):
        """Objects of this class never expect connect events
        """
        pass

    def handle_close(self):
        """Invoked by asyncore on connection closed event
        """
        self.agent.close()

    def handle_error(self, exc_type, exc_value, exc_traceback):
        """Invoked by asyncore on any exception
        """
        # In case of PySNMP exception, invoke the callback function
        # and pass it an empty result. Otherwise,just pass the exception on.
        if type(exc_type) == ClassType \
           and issubclass(exc_type, error.Generic):
            self.callback_fun(self, self.callback_ctx,\
                              (None, None), (exc_type, \
                                             exc_value, exc_traceback))
        else:    
            raise (exc_type, exc_value)
        
