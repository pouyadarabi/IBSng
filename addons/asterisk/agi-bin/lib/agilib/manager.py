#!/usr/bin/env python

"""manager.py

Interface for Asterisk Manager

"""

import sys,os
import socket
import threading
import Queue
import re
from select import select
from cStringIO import StringIO
from types import *
from time import sleep

EOL = '\r\n'

class ManagerMsg(object): 
    def __init__(self, response):
        self.response = response
        self.data = ''
        self.headers = {}
        #print response.getvalue()
        self.parse(response)
        if not self.headers:
            # Bad app not returning any headers.  Let's fake it
            self.headers['Response'] = 'Generated Header'
            #            'Response:'

    def parse(self, response):
        print response.getvalue()
        response.seek(0)
        #print response.getvalue()
        data = []
        for line in response.readlines():
            line = line.rstrip()
            if not line: continue
            #print 'LINE: %s' % line
            if line.find(':') > -1:
                item = [x.strip() for x in line.split(':',1)]
                #print 'ITEM:', item
                if len(item) == 2:
                    self.headers[item[0]] = item[1]
                else:
                    data.append(line)
            else:
                data.append(line)
        self.data = '%s\n' % '\n'.join(data)

    def has_header(self, hname):
        return self.headers.has_key(hname)

    def get_header(self, hname):
        return self.headers[hname]


class Event(object):
    callbacks = {}
    registerlock = threading.Lock()
    def __init__(self, message):
        self.message = message
        self.data = message.data
        self.headers = message.headers
        if not message.has_header('Event'):
            raise ManagerException('Trying to create event from non event message')
        self.name = message.get_header('Event')

        # get a copy of current registered callbacks
        lock = Event.registerlock
        try:
            lock.acquire()
            self.listeners = Event.callbacks.get(self.name,[])[:]
            self.listeners.extend(Event.callbacks.get('*',[]))
        finally:
            if lock.locked():
                lock.release()

    def dispatch_events(self):
        for func in self.listeners:
            func(self)
    
    # static method
    def register(eventname, func):
        lock = Event.registerlock
        try:
            lock.acquire()
            callbacks = Event.callbacks.get(eventname, [])
            callbacks.append(func)
            Event.callbacks[eventname] = callbacks
        finally:
            if lock.locked():
                lock.release()
    register = staticmethod(register)

    def get_action_id(self):
        return self.headers.get('ActionID',0000)


class Manager(object):
    #__slots__ = ['host','port','username','secret']
    def __init__(self, host='localhost', port=5038):
        self.host = host
        self.port = port
        # sock_lock is used to serialize acces to the socket in the case of us
        # issuing a command and wanting to read the immediate response
        self.sock_lock = threading.Lock()
        self.sock = None
        self.sockf = None
        self.connected = 0
        self.message_queue = Queue.Queue()
        self.response_queue = Queue.Queue()
        self.event_queue = Queue.Queue()
        self.reswaiting = []
        self._seqlock = threading.Lock()
        self._seq = 0
        self.hostname = socket.gethostname()

    def __del__(self):
        self.quit()

    def next_seq(self):
        self._seqlock.acquire()
        try:
            return self._seq
        finally:
            self._seq += 1
            self._seqlock.release()
        
    def send_action(self, cdict={}, **kwargs):
        cdict.update(kwargs)
        cdict['ActionID'] = '%s-%08x' % (self.hostname, self.next_seq())
        clist = []
        for item in cdict.items():
            #print item
            item = tuple([str(x) for x in item])
            clist.append('%s: %s' % item)
        clist.append(EOL)
        command = EOL.join(clist)

        rsocks, wsocks, esocks = select([],[self.sock],[],60)
        if not wsocks:
            raise ManagerSocketException('Communication Problem:  self.sock not ready for writing')
        if self.sock.fileno() < 0:
            raise ManagerSocketException('Connection Terminated')
        try:
            self.sock_lock.acquire()
            self.sock.sendall(command)
        finally:
            self.sock_lock.release()

        self.reswaiting.insert(0,1)
        response = self.response_queue.get()
        self.reswaiting.pop(0)
        return response

    def _receive_data(self):
        """Read the response from a command.
           This SHOULD be called from a block that is locked
           on self.sock_lock
           self.sock should also be ready for reading
        """
        while 1:
            rsocks, wsocks, esocks = select([self.sock],[],[],1)
            if not self.running: break
            lines = []
            try:
                sys.stderr.write('*')
                self.sock_lock.acquire()
                if rsocks:
                    sys.stderr.write('+')
                    if not self.sock_lock.locked():
                        raise ManagerException('self.sock_lock is not locked')
                    if self.sock.fileno() < 0:
                        raise ManagerSocketException('Connection Terminated')
                    while 1:
                        #line = self.sockf.readline()
                        line = []
                        while 1:
                            c = self.sock.recv(1)
                            sys.stderr.write(repr(c))
                            line.append(c)
                            if c == '\n':
                                sys.stderr.write('\n')
                                line = ''.join(line)
                                break
                        assert type(line) in StringTypes
                        print line
                        lines.append(line)
                        if line == EOL:
                            break
                        if line.find('Asterisk Call Manager') >= 0:
                            self.version = line.split('/')[1].strip()
                            break
                            sys.stderr.write('.')

                        sleep(.001)
            finally:
                if lines:
                    self.message_queue.put(StringIO(''.join(lines)))
                sys.stderr.write('-')
                self.sock_lock.release()

    def event_loop(self):
        t = threading.Thread(target=self._receive_data)
        t.start()
        try:
            while 1:
                #print data.getvalue()
                data = self.message_queue.get()
                if not data:
                    # None so quit
                    break
                message = ManagerMsg(data)
                if message.has_header('Event'):
                    ev = Event(message)
                    self.event_queue.put(ev)
                elif message.has_header('Response'):
                    self.response_queue.put(message)
                else:
                    print 'No clue what we got\n%s' % message.data
        finally:
            t.join()
                            

    def event_dispatch(self):
        # event dispatching is serialized in this thread
        while 1:
            ev = self.event_queue.get()
            if not ev:
                # None so quit
                break
            ev.dispatch_events()

    def connect(self, host='', port=0):
        host = host or self.host
        port = port or self.port
        assert type(host) in StringTypes
        port = int(port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host,port))
        rsocks, wsocks, esocks = select([],[self.sock],[],1)
        if not wsocks:
            raise ManagerException('Could not establish connection')
        self.sock.setblocking(1)
        #self.sock.settimeout(.5)
        self.connected = 1
        # use this for reading only
        self.sockf = self.sock.makefile()
        self.running = 1
        self.event_thread = t = threading.Thread(target=self.event_loop)
        t.start()
        self.event_dispatch_thread = t = threading.Thread(target=self.event_dispatch)
        t.start()
        # hmmmmmm XXX
        return self.response_queue.get()

    def quit(self):
        self.running = 0

        self.message_queue.put(None)
        self.event_queue.put(None)
        for waiter in self.reswaiting:
            self.response_queue.put(None)

        if self.event_thread:
            self.event_thread.join()

        if self.event_dispatch_thread:
            self.event_dispatch_thread.join()

        self.sock.shutdown(2)
        self.sock.close()

    def login(self, username='', secret=''):
        cdict = {'Action':'Login'}
        cdict['Username'] = username
        cdict['Secret'] = secret
        response = self.send_action(cdict)
        return response

    def ping(self):
        cdict = {'Action':'Ping'}
        response = self.send_action(cdict)
        return response

    def logoff(self):
        cdict = {'Action':'Logoff'}
        response = self.send_action(cdict)
        return response

    def hangup(self, channel):
        cdict = {'Action':'Hangup'}
        cdict['Channel'] = channel
        response = self.send_action(cdict)
        return response

    def status(self):
        cdict = {'Action':'Status'}
        response = self.send_action(cdict)
        return response

    def redirect(self, channel, exten, priority='1', extra_channel='', context=''):
        cdict = {'Action':'Redirect'}
        cdict['Channel'] = channel
        cdict['Exten'] = exten
        cdict['Priority'] = priority
        if context:   cdict['Context']  = context
        if timeout:   cdict['Timeout']  = timeout
        if caller_id: cdict['CallerID'] = caller_id
        response = self.send_action(cdict)
        return response

    def originate(self, channel, exten, context='', priority='', timeout='', caller_id=''):
        cdict = {'Action':'Originate'}
        cdict['Channel'] = channel
        cdict['Exten'] = exten
        if context:   cdict['Context']  = context
        if priority:  cdict['Priority'] = priority
        if timeout:   cdict['Timeout']  = timeout
        if caller_id: cdict['CallerID'] = caller_id
        response = self.send_action(cdict)
        return response

    def mailbox_status(self, mailbox):
        cdict = {'Action':'MailboxStatus'}
        cdict['Mailbox'] = mailbox
        response = self.send_action(cdict)
        return response

    def command(self, command):
        cdict = {'Action':'Command'}
        cdict['Command'] = command
        response = self.send_action(cdict)
        return response

    def extension_state(self, exten, context):
        cdict = {'Action':'ExtensionState'}
        cdict['Exten'] = exten
        cdict['Context'] = context
        response = self.send_action(cdict)
        return response

    def absolute_timeout(self, channel, timeout):
        cdict = {'Action':'AbsoluteTimeout'}
        cdict['Channel'] = channel
        cdict['Timeout'] = timeout
        response = self.send_action(cdict)
        return response

    def mailbox_count(self, mailbox):
        cdict = {'Action':'MailboxCount'}
        cdict['Mailbox'] = mailbox
        response = self.send_action(cdict)
        return response

class ManagerException(Exception): pass
class ManagerSocketException(ManagerException): pass


if __name__=='__main__':
    from pprint import pprint
    def spew(event):
        print 'EVENT: ', event.name
        pprint(event.headers)
        pprint(event.data)

    Event.register('*',spew)

    mgr = Manager('myastbox')
    mess = mgr.connect()
    pprint(mess.headers)
    pprint(mess.data)
    
    mess = mgr.login('username','passwd')
    pprint(mess.headers)
    pprint(mess.data)

    try:
        #raw_input("Press <enter> to exit")
        while 1:
            sleep(5)
            os.system('clear')
            mess = mgr.status()
            pprint(mess.headers)
            pprint(mess.data)
    finally:
        mgr.quit()
