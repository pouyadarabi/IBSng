#!/usr/bin/env python2

"""pyst

A module for asterisk AGI programming

pyvr

{'agi_callerid' : 'mars.putland.int',
 'agi_channel'  : 'IAX[kputland@kputland]/119',
 'agi_context'  : 'default',
 'agi_dnid'     : '666',
 'agi_enhanced' : '0.0',
 'agi_extension': '666',
 'agi_language' : 'en',
 'agi_priority' : '1',
 'agi_rdnis'    : '',
 'agi_request'  : 'pyst',
 'agi_type'     : 'IAX'}

"""

import sys, pprint, re
from types import ListType

DEFAULT_TIMEOUT = 2000 # 2sec timeout used as default for functions that take timeouts
DEFAULT_RECORD  = 20000 # 20sec record time

re_code = re.compile(r'(^\d*)\s*(.*)')
re_kv = re.compile(r'(?P<key>\w+)=(?P<value>[\w-]+)\s*(?:\((?P<data>.*)\))*')

class AGIException(Exception): pass

class AGI:
    def __init__(self):
        sys.stderr.write('ARGS: ')
        sys.stderr.write(str(sys.argv))
        sys.stderr.write('\n')
        self.env = {}
        self._get_agi_env()

    def _get_agi_env(self):
        while 1:
            line = sys.stdin.readline().strip()
            sys.stderr.write('ENV LINE: ')
            sys.stderr.write(line)
            sys.stderr.write('\n')
            if line == '':
                #blank line signals end
                break
            key,data = line.split(':')[0], ':'.join(line.split(':')[1:])
            key = key.strip()
            data = data.strip()
            if key <> '':
                self.env[key] = data
        sys.stderr.write('class AGI: self.env = ')
        sys.stderr.write(pprint.pformat(self.env))
        sys.stderr.write('\n')
        
    def execute(self, command, *args):
        try:
            self.send_command(command, *args)
            return self.get_result()
        except IOError,e:
            if e.errno == 32:
                # Broken Pipe * let us go
                sys.exit(1)
            else:
                raise

    def send_command(self, command, *args):
        command = command.strip()
        command = '%s %s' % (command, ' '.join(map(str,args)))
        command = command.strip()
        if command[-1] != '\n':
            command += '\n'
        sys.stderr.write('    COMMAND: %s' % command)
        sys.stdout.write(command)
        sys.stdout.flush()

    def get_result(self, stdin=sys.stdin):
        code = 0
        result = {'result':('UNDEFINED','')}
        line = stdin.readline().strip()
        sys.stderr.write('    RESULT_LINE: %s\n' % line)
        m = re_code.search(line)
        if m:
            code, response = m.groups()
            code = int(code)

        if code == 200:
            for key,value,data in re_kv.findall(response):
                result[key] = (value, data)

                # If user hangs up... we get 'hangup' in the data
                if data == 'hangup':
                    AGIException(code, "User hungup during execution")

            sys.stderr.write('    RESULT_DICT: %s\n' % pprint.pformat(result))
            return result
        elif code == 510:
            raise AGIException(code, response)
        elif code == 520:
            usage = [line]
            line = stdin.readline().strip()
            while line[:3] != '520':
                usage.append(line)
                line = stdin.readline().strip()
            usage.append(line)
            usage = '%s\n' % '\n'.join(usage)
            raise AGIException(code, usage)
        else:
            raise AGIException(code, 'Unhandled code or undefined response')

    def _process_digit_list(self, digits):
        if type(digits) == ListType:
            digits = ''.join(map(str, digits))
        digits = '"%s"' % digits
        return digits

    def answer(self):
        """agi.answer() --> None
        Answer channel if not already in answer state.
        """
        res = self.execute('answer')['result']
        if res == '-1':
            raise AGIException('Channel falure on channel %s' % self.env.get('agi_channel','UNKNOWN'))

    def wait_for_digit(self, timeout=DEFAULT_TIMEOUT):
        """agi.wait_for_digit(timeout=DEFAULT_TIMEOUT) --> digit
        Waits for up to 'timeout' milliseconds for a channel to receive a DTMF digit.
        Returns digit dialed
        Throws AGITimeout if no digit entered
        Throws AGIException on channel falure
        """
        res = self.execute('wait for digit', timeout)['result'][0]
        if res == '-1':
            raise AGIException('Channel falure on channel %s' % self.env.get('agi_channel','UNKNOWN'))
        elif res == '0':
            return ''
        else:
            try:
                return chr(int(res))
            except:
                raise AGIException('Unable to convert result to digit: %s' % res)

    def get_digit(self, *args):
        """agi.get_digit(timeout=DEFAULT_TIMEOUT) --> digit
        Alias for agi.wait_for_digit() to align with agi.get_data()
        """
        self.wait_for_digit(*args)

    def send_text(self, text=''):
        """agi.send_text(text='') --> None
        Sends the given text on a channel.  Most channels do not support the
        transmission of text.
        Throws AGIException on error/hangup
        """
        text = '"%s"' % text
        res = self.execute('send_text', text)['result'][0]
        if res == '-1':
            raise AGIException('Channel falure on channel %s' % self.env.get('agi_channel','UNKNOWN'))

    def receive_char(self, timeout=DEFAULT_TIMEOUT):
        """agi.receive_char(timeout=DEFAULT_TIMEOUT) --> chr
        Receives a character of text on a channel.  Specify timeout to be the
        maximum time to wait for input in milliseconds, or 0 for infinite. Most channels
        do not support the reception of text.
        """
        res = self.execute('receive char', timeout)['result'][0]
        if res == '-1':
            raise AGIException('Channel error/hangup on channel %s' % self.env.get('agi_channel','UNKNOWN'))
        elif res == '0':
            return ''
        else:
            try:
                return chr(int(res))
            except:
                raise AGIException('Unable to convert result to char: %s' % res)

    def tdd_mode(self, mode='off'):
        """agi.tdd_mode(mode='on'|'off') --> None
        Enable/Disable TDD transmission/reception on a channel. 
        Throws AGIException if channel is not TDD-capable.
        """
        res = self.execute('tdd mode', mode)['result'][0]
        if res == '0':
            raise AGIException('Channel %s is not TDD-capable')
            
    def stream_file(self, filename, escape_digits='', sample_offset=0):
        """agi.stream_file(filename, escape_digits='', sample_offset=0) --> digit
        Send the given file, allowing playback to be interrupted by the given
        digits, if any.  escape_digits is a string '12345' or a list  of 
        ints [1,2,3,4,5] or strings ['1','2','3'] or mixed [1,'2',3,'4']
        If sample offset is provided then the audio will seek to sample
        offset before play starts.  Returns  digit if one was pressed.
        Throws AGIException if the channel was disconnected.  Remember, the file
        extension must not be included in the filename.
        """
        escape_digits = self._process_digit_list(escape_digits)
        response = self.execute('stream file', filename, escape_digits, sample_offset)
        res = response['result'][0]
        if res == '-1':
            raise AGIException('Channel falure on channel %s' % self.env.get('agi_channel','UNKNOWN'))
        elif res == '0':
            return ''
        else:
            try:
                return chr(int(res))
            except:
                raise AGIException('Unable to convert result to char: %s' % res)

    def send_image(self, filename):
        """agi.send_image(filename) --> None
        Sends the given image on a channel.  Most channels do not support the
        transmission of images.   Image names should not include extensions.
        Throws AGIException on channel failure
        """
        res = self.execute('send image', filename)['result'][0]
        if res != '0':
            raise AGIException('Channel falure on channel %s' % self.env.get('agi_channel','UNKNOWN'))

    def say_digits(self, digits, escape_digits=''):
        """agi.say_digits(digits, escape_digits='') --> digit
        Say a given digit string, returning early if any of the given DTMF digits
        are received on the channel.  
        Throws AGIException on channel failure
        """
        digits = self._process_digit_list(digits)
        escape_digits = self._process_digit_list(escape_digits)
        res = self.execute('say digits', digits, escape_digits)['result'][0]
        if res == '-1':
            raise AGIException('Channel falure on channel %s' % self.env.get('agi_channel','UNKNOWN'))
        elif res == '0':
            return ''
        else:
            try:
                return chr(int(res))
            except:
                raise AGIException('Unable to convert result to char: %s' % res)

    def say_number(self, number, escape_digits=''):
        """agi.say_number(number, escape_digits='') --> digit
        Say a given digit string, returning early if any of the given DTMF digits
        are received on the channel.  
        Throws AGIException on channel failure
        """
        number = self._process_digit_list(number)
        escape_digits = self._process_digit_list(escape_digits)
        res = self.execute('say number', number, escape_digits)['result'][0]
        if res == '-1':
            raise AGIException('Channel falure on channel %s' % self.env.get('agi_channel','UNKNOWN'))
        elif res == '0':
            return ''
        else:
            try:
                return chr(int(res))
            except:
                raise AGIException('Unable to convert result to char: %s' % res)

    def get_data(self, filename, timeout=DEFAULT_TIMEOUT, max_digits=255):
        """agi.get_data(filename, timeout=DEFAULT_TIMEOUT, max_digits=255) --> digits
        Stream the given file and receive dialed digits
        """
        result = self.execute('get data', filename, timeout, max_digits)
        res, value = result['result']
        return res

    def set_context(self, context):
        """agi.set_context(context)
        Sets the context for continuation upon exiting the application.
        No error appears to be produced.  Does not set exten or priority
        Use at your own risk.  Ensure that you specify a valid context.
        """
        self.execute('set context', context)

    def set_extension(self, extension):
        """agi.set_extension(extension)
        Sets the extension for continuation upon exiting the application.
        No error appears to be produced.  Does not set context or priority
        Use at your own risk.  Ensure that you specify a valid extension.
        """
        self.execute('set extension', extension)

    def set_priority(self, priority):
        """agi.set_priority(priority)
        Sets the priority for continuation upon exiting the application.
        No error appears to be produced.  Does not set exten or context
        Use at your own risk.  Ensure that you specify a valid priority.
        """
        self.execute('set priority', priority)

    def goto_on_exit(self, context='', extension='', priority=''):
        context = context or self.env['agi_context']
        extension = extension or self.env['agi_extension']
        priority = priority or self.env['agi_priority']
        self.set_context(context)
        self.set_extension(extension)
        self.set_priority(priority)

    def record_file(self, filename, format='gsm', escape_digits='#', timeout=DEFAULT_RECORD, offset=0, beep='beep'):
        """agi.record_file(filename, format, escape_digits, timeout=DEFAULT_TIMEOUT, offset=0, beep='beep') --> None
        Record to a file until a given dtmf digit in the sequence is received
        The format will specify what kind of file will be recorded.  The timeout 
        is the maximum record time in milliseconds, or -1 for no timeout. Offset 
        samples is optional, and if provided will seek to the offset without 
        exceeding the end of the file
        """
        escape_digits = self._process_digit_list(escape_digits)
        res = self.execute('record file', filename, format, escape_digits, timeout, offset, beep)['result'][0]
        if res == '-1':
            raise AGIException('Channel falure on channel %s' % self.env.get('agi_channel','UNKNOWN'))
        else:
            try:
                return chr(int(res))
            except:
                raise AGIException('Unable to convert result to digit: %s' % res)

    def set_autohangup(self, secs):
        """agi.set_autohangup(secs) --> None
        Cause the channel to automatically hangup at <time> seconds in the
        future.  Of course it can be hungup before then as well.   Setting to
        0 will cause the autohangup feature to be disabled on this channel.
        """
        self.execute('set autohangup', time)

    def hangup(self, channel=''):
        """agi.hangup(channel='')
        Hangs up the specified channel.
        If no channel name is given, hangs up the current channel
        """
        self.execute('hangup', channel)

    def appexec(self, application, options=''):
        """agi.exec(application, options=''):
        Executes <application> with given <options>.
        Returns whatever the application returns, or -2 on failure to find application
        """
        options = '"%s"' % options
        result = self.execute('exec', application, options)
        res = result['result'][0]
        if res == '-2':
            raise AGIException('Unable to find application: %s' % application)
        return res

    def set_callerid(self, number):
        """agi.set_callerid(number) --> None
        Changes the callerid of the current channel.
        """
        self.execute('set callerid', number)

    def channel_status(self, channel=''):
        """agi.channel_status(channel='') --> int
        Returns the status of the specified channel.
        If no channel name is given the returns the status of the
        current channel.
        Return values:
        0 Channel is down and available
        1 Channel is down, but reserved
        2 Channel is off hook
        3 Digits (or equivalent) have been dialed
        4 Line is ringing
        5 Remote end is ringing
        6 Line is up
        7 Line is busy
        """
        result = self.execute('channel status', channel)
        return result['result']

    def set_variable(self, name, value):
        """agi.set_variable(name, value) --> None
        """
        name = '"%s"' % name
        value = '"%s"' % str(value)
        self.execute('set variable', name, value)
        # XXX - Check for error?

    def get_variable(self, name):
        """agi.get_variable(name) --> str
        Returns 0 if <variablename> is not set.  Returns 1 if <variablename>
        is set and returns the variable in parenthesis
        example return code: 200 result=1 (testvariable)
        """
        name = '%s' % name
        result = self.execute('get variable', name)
        res, value = result['result']
        if res == '0':
            raise AGIException("Variable %s is not set" % name)

        return value

    def verbose(self, message='', level=1):
        """agi.verbose(message='', level=1) --> None
        Sends <message> to the console via verbose message system.
        <level> is the the verbose level (1-4)
        Always returns 1
        """
        message = '"%s"' % message
        self.execute('verbose', message, level)

    def database_get(self, family, key):
        """agi.database_get(family, key) --> str
        Retrieves an entry in the Asterisk database for a given family and key.
        Returns 0 if <key> is not set.  Returns 1 if <key>
        is set and returns the variable in parenthesis
        example return code: 200 result=1 (testvariable)
        """
        family = '"%s"' % family
        key = '"%s"' % key
        result = self.execute('database get', family, key)
        res, value = result['result']
        if res == '0':
            raise AGIException('Key not found in database: family=%s, key=%s' % (family, key))
        elif res == '1':
            return value
        else:
            raise AGIException('Unknown exception for : family=%s, key=%s, result=%s' % (family, key, pprint.pformat(result)))

    def database_put(self, family, key, value):
        """agi.database_put(family, key, value) --> None
        Adds or updates an entry in the Asterisk database for a
        given family, key, and value.
        """
        family = '"%s"' % family
        key = '"%s"' % key
        value = '"%s"' % value
        result = self.execute('database put', family, key, value)
        res, value = result['result']
        if res == '0':
            raise AGIException('Unable to put vaule in databale: family=%s, key=%s, value=%s' % (family, key, value))
            
    def database_del(self, family, key):
        """agi.database_del(family, key) --> None
        Deletes an entry in the Asterisk database for a
        given family and key.
        """
        family = '"%s"' % family
        key = '"%s"' % key
        result = self.execute('database del', family, key)
        res, value = result['result']
        if res == '0':
            raise AGIException('Unable to delete from database: family=%s, key=%s' % (family, key))

    def database_deltree(self, family, key=''):
        """agi.database_deltree(family, key='') --> None
        Deletes a family or specific keytree withing a family
        in the Asterisk database.
        """
        family = '"%s"' % family
        key = '"%s"' % key
        result = self.execute('database deltree', family, key)
        res, value = result['result']
        if res == '0':
            raise AGIException('Unable to delete tree from database: family=%s, key=%s' % (family, key))

    def noop(self):
        """agi.noop() --> None
        Does nothing
        """
        self.execute('noop')

if __name__=='__main__':
    agi = AGI()
    #agi.appexec('festival','Welcome to Klass Technologies.  Thank you for calling.')
    #agi.appexec('festival','This is a test of the text to speech engine.')
    #agi.appexec('festival','Press 1 for sales ')
    #agi.appexec('festival','Press 2 for customer support ')
    #agi.hangup()
    #agi.goto_on_exit(extension='1234', priority='1')
    #sys.exit(0)
    #agi.say_digits('123', [4,'5',6])
    #agi.say_digits([4,5,6])
    #agi.say_number('1234')
    #agi.say_number('01234')  # 668
    #agi.say_number('0xf5')   # 245
    agi.get_data('demo-congrats')
    agi.hangup()
    sys.exit(0)
    #agi.record_file('pyst-test') #FAILS
    #agi.stream_file('demo-congrats', [1,2,3,4,5,6,7,8,9,0,'#','*'])
    #agi.appexec('background','demo-congrats')
    try:
        agi.appexec('backgrounder','demo-congrats')
    except AGIException:
        sys.stderr.write("Handled exception for missing application backgrounder\n")
    agi.set_variable('foo','bar')
    agi.get_variable('foo')
    try:
        agi.get_variable('foobar')
    except AGIException:
        sys.stderr.write("Handled exception for missing variable foobar\n")
    agi.database_put('foo', 'bar', 'foobar')
    agi.database_put('foo', 'baz', 'foobaz')
    agi.database_put('foo', 'bat', 'foobat')
    v = agi.database_get('foo', 'bar')
    sys.stderr.write('DBVALUE foo:bar = %s\n' % v)
    try:
        v = agi.database_get('bar', 'foo')
        sys.stderr.write('DBVALUE foo:bar = %s\n' % v)
    except AGIException:
        sys.stderr.write("Handled exception for missing database entry bar:foo\n")
    agi.database_del('foo', 'bar')
    agi.database_deltree('foo')
    agi.hangup()
