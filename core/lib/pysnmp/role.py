"""
   Single-session, blocking network I/O classes.

   Written by Ilya Etingof <ilya@glas.net>, 1999-2002

"""
import socket
import select

# Import package components
import error

class Error(error.Generic):
    """Base class for role module
    """
    pass

class BadArgument(Error):
    """Bad argument given
    """
    pass

class NetworkError(Error):
    """Network transport error
    """
    pass

class NoResponse(NetworkError):
    """No response arrived before timeout
    """
    pass

class NoRequest(NetworkError):
    """No request arrived before timeout
    """
    pass

class manager:
    """Network client: send data item to server and receive a response
    """
    def __init__(self, agent=None, iface=('0.0.0.0', 0)):
        # Initialize defaults
        self.agent = agent
        self.iface = iface
        self.socket = None
        self.timeout = 1.0
        self.retries = 3

    def __del__(self):
        """Close socket on object termination
        """
        try:
            self.close()

        except error.TransportError:
            pass
        
    def get_socket(self):
        """
           get_socket() -> socket

           Return socket object previously created with open() method.
        """
        return self.socket

    def open(self):
        """
           open()
           
           Initialize transport layer (UDP socket) to be used
           for further communication with server.
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        except socket.error, why:
            raise NetworkError('socket() error: ' + str(why))

        # See if we need to bind to specific interface on client machine
        try:
            self.socket.bind(self.iface)

        except socket.error, why:
            raise NetworkError('bind() error: %s: %s' % (self.iface, why))

        # Connect to default destination if given
        if self.agent is not None:
            try:
                self.socket.connect(self.agent)

            except socket.error, why:
                raise NetworkError('connect() error: %s: %s' % (self.agent, why))

        return self.socket

    def send(self, request, dst=None):
        """
           send(req[, dst])
           
           Send "req" message (string) to server by address specified on
           object creation or by "dst" address given in socket module 
           notation.
        """
        # Make sure the connection is established, open it otherwise
        if not self.socket:
            self.open()

        try:
            if dst:
                self.socket.sendto(request, dst)
            else:    
                self.socket.send(request)

        except socket.error, why:
            raise NetworkError('send() error: ' + str(why))

    def read(self):
        """
           read() -> (message, src)
           
           Read data from the socket (assuming there's some data ready
           for reading), return a tuple of response message (as string)
           and source address 'src' (in socket module notation).
        """   
        # Make sure the connection exists
        if not self.socket:
            raise NetworkError('Socket not initialized')

        try:
            (message, src) = self.socket.recvfrom(65536)

        except socket.error, why:
            raise NetworkError('recv() error: ' + str(why))

        return (message, src)
        
    def receive(self):
        """
           receive() -> (message, src)
           
           Wait for incoming data from network or timeout (and return
           a tuple of None's).

           Return a tuple of received data item (as string) and source address
           'src' (in socket module notation).
        """
        # Make sure the connection exists
        if not self.socket:
            raise NetworkError('Socket not initialized')

        # Initialize sockets map
        r, w, x = [self.socket], [], []

        # Wait for response
        r, w, x = select.select(r, w, x, self.timeout)

        # Timeout occurred?
        if r:
            return self.read()

        # Return nothing on timeout
        return(None, None)

    def send_and_receive(self, message, dst=None):
        """
           send_and_receive(data[, dst]) -> (data, src)
           
           Send data item to remote entity by address specified on object 
           creation or 'dst' address and receive a data item in response
           or timeout (and raise NoResponse exception).

           Return a tuple of data item (as string) and source address
           'src' (in socket module notation).
        """
        # Initialize retries counter
        retries = 0

        # Send request till response or retry counter hits the limit
        while retries < self.retries:
            # Send a request
            self.send(message, dst)

            # Wait for response
            (response, src) = self.receive()

            # See if it's succeeded
            if response:
                return(response, src)

            # Otherwise, try it again
            retries = retries + 1

        # No answer, raise an exception
        raise NoResponse('No response arrived before timeout')

    def close(self):
        """
           close()
           
           Terminate communication with remote server.
        """
        # See if it's opened
        if self.socket:
            try:
                self.socket.close()

            except socket.error, why:
                raise NetworkError('close() error: ' + str(why))

            # Initialize it to None to indicate it's closed
            self.socket = None  

class agent:
    """Network client: receive requests, send back responses
    """
    def __init__(self, ifaces=[('0.0.0.0', 161)]):
        # Block on select() waiting for request by default
        self.timeout = None
        
        # Initialize defaults
        self.ifaces = ifaces
        self.socket = None

    def __del__(self):
        """Close socket on object termination
        """
        try:
            self.close()

        except error.TransportError:
            pass

    def get_socket(self):
        """
           get_socket() -> socket

           Return socket object previously created with open() method.
        """
        return self.socket

    def open(self):
        """
           open()
           
           Initialize transport internals to be used for further
           communication with client.
        """
        try:
            self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        except socket.error, why:
            raise NetworkError('socket() error: ' + str(why))

        # Bind to specific interfaces at server machine
        for iface in self.ifaces:
            try:
                self.socket.bind(iface)

            except socket.error, why:
                raise NetworkError('bind() error: %s: %s' % (iface, why))

        return self.socket

    def send(self, message, dst):
        """
           send(rsp, dst)
           
           Send response message (given as string) to client process
           by 'dst' address given in socket module notation.
        """
        # Make sure the connection is established, open it otherwise
        if not self.socket:
            raise NetworkError('Socket not initialized')

        try:
            self.socket.sendto(message, dst)
                
        except socket.error, why:
            raise NetworkError('send() error: ' + str(why))

    def read(self):
        """
           read() -> (req, src)
           
           Read data from the socket (assuming there's some data ready
           for reading), return a tuple of request (as string) and
           source address 'src' (in socket module notation).
        """   
        # Make sure the connection exists
        if not self.socket:
            raise NetworkError('Socket not initialized')

        try:
            (message, peer) = self.socket.recvfrom(65536)

        except socket.error, why:
            raise NetworkError('recvfrom() error: ' + str(why))

        return (message, peer)
        
    def receive(self):
        """
           receive() -> (req, src)
           
           Wait for and receive request message from remote process
           or timeout.

           Return a tuple of request message (as string) and source address
           'src' (in socket module notaton).
        """
        # Attempt to initialize transport stuff
        if not self.socket:
            self.open()
            
        # Initialize sockets map
        r, w, x = [ self.socket ], [], []

        # Wait for response
        r, w, x = select.select(r, w, x, self.timeout)

        # Timeout occurred?
        if r:
            return self.read()

        raise NoRequest('No request arrived before timeout')
    
    def receive_and_send(self, callback):
        """
           receive_and_send(callback)
           
           Wait for request from a client process or timeout (and raise
           NoRequest exception), pass request to the callback function
           to build a response, send response back to client process.
        """
        if not callable (callback):
            raise BadArgument('Bad callback function')

        while 1:
            # Wait for request to come
            (request, src) = self.receive()

            if not request:
                raise NoRequest('No request arrived before timeout')

            # Invoke callback function
            (response, dst) = callback(self, (request, src))

            # Send a response if any
            if (response):
                # Reply back by either source address or alternative
                # destination whenever given
                if dst:
                    self.send(response, dst)
                else:
                    self.send(response, src)

    def close(self):
        """
           close()
           
           Close UDP socket used for communication with client.
        """
        # See if it's opened
        if self.socket:
            try:
                self.socket.close()

            except socket.error, why:
                raise NetworkError('close() error: ' + str(why))

            # Initialize it to None to indicate it's closed
            self.socket = None  
