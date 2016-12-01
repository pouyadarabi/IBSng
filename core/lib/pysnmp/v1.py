"""
   Basic Encoding Rules (BER) for structured, SNMP v.1 specific ASN.1 data
   types (SNMP messages).

   Written by Ilya Etingof <ilya@glas.net>, 1999-2002.
"""
import types
import time
import string

# Import package components
import asn1

class Error(asn1.Error):
    """Base class for v1 module exceptions
    """
    pass

class TypeError(Error):
    """V1 data type incompatibility
    """
    pass

class BadArgument(Error):
    """Bad V1 object value
    """
    pass

class BadPDUType(Error):
    """Bad SNMP PDU type
    """
    pass

class BadVersion(Error):
    """Bad SNMP version
    """
    pass

class BadEncoding(Error):
    """Bad BER encoding in SNMP message
    """
    pass

class SNMPError:
    """Represent an RFC 1157 SNMP error.
    """
    # Taken from UCD SNMP code
    ERRORS = [
        '(noError) No Error',
        '(tooBig) Response message would have been too large.',
        '(noSuchName) There is no such variable name in this MIB.',
        '(badValue) The value given has the wrong type or length.',
        '(readOnly) The two parties used do not have access to use the specified SNMP PDU.',
        '(genError) A general failure occured.'
    ]
    
    def __init__(self, status):
        self.status = status

    def __str__(self):
        """Return verbose error message if known
        """
        if self.status > 0 and self.status < len(self.ERRORS):
            return self.ERRORS[self.status]

class BERHEADER(asn1.BERHEADER):
    """Extended, SNMP v.1 specific ASN.1 data types
    """
    TAGS = {
        'GETREQUEST_PDU'     : 0x00 | asn1.BERHEADER.FORMAT['CONSTRUCTED'] \
                                    | asn1.BERHEADER.CLASS['CONTEXT'],
        'GETNEXTREQUEST_PDU' : 0x01 | asn1.BERHEADER.FORMAT['CONSTRUCTED'] \
                                    | asn1.BERHEADER.CLASS['CONTEXT'],
        'GETRESPONSE_PDU'    : 0x02 | asn1.BERHEADER.FORMAT['CONSTRUCTED'] \
                                    | asn1.BERHEADER.CLASS['CONTEXT'],
        'SETREQUEST_PDU'     : 0x03 | asn1.BERHEADER.FORMAT['CONSTRUCTED'] \
                                    | asn1.BERHEADER.CLASS['CONTEXT'],
        'TRAPREQUEST_PDU'    : 0x04 | asn1.BERHEADER.FORMAT['CONSTRUCTED'] \
                                    | asn1.BERHEADER.CLASS['CONTEXT']
        }

#
# SNMP v.1 PDU types
#

class PDU_SEQUENCE(BERHEADER, asn1.SEQUENCE):
    """Extended ASN.1 data type
    """
    pass

class GETREQUEST_PDU(PDU_SEQUENCE):
    """GETREQUEST type ASN.1 object
    """
    pass

class GETNEXTREQUEST_PDU(PDU_SEQUENCE):
    """GETNEXTREQUEST type ASN.1 object 
    """
    pass

class GETRESPONSE_PDU(PDU_SEQUENCE):
    """GETRESPONSE type ASN.1 object
    """
    pass

class SETREQUEST_PDU(PDU_SEQUENCE):
    """SETREQUEST type ASN.1 object
    """
    pass

class TRAPREQUEST_PDU(PDU_SEQUENCE):
    """TRAPREQUEST type ASN.1 object
    """
    pass

#
# SNMP v.1 specific structured ASN.1 data types
#

class SNMPOBJECT(BERHEADER):
    """
       Basic SNMP object. Defines behaviour and properties of
       various structured ASN.1 objects.
    """
    ARGS = {}
    def __init__(self, **kwargs):
        """Store dictionary args
        """
        self.update(kwargs)

    def __str__(self):
        """Return string representation of class instance
        """
        return '%s: %s' % (self.__class__.__name__, str(self.value))

    def __repr__(self):
        """Return native representation of instance payload
        """
        res = ''
        for key in self.value.keys():
            if res:
                res = res + ', ' + key + '=' + repr(self.value[key]) 
            else:    
                res = key + '=' + repr(self.value[key])
        return self.__class__.__name__ + '(' + res + ')'        

    def __cmp__(self, other):
        """Attempt to compare the payload of instances of the same class
        """
        try:
            return self._cmp(other)

        except AttributeError:
            raise TypeError('Comparation method not provided for %s'\
                            % self.__class__.__name)

        except StandardError, why:
            raise TypeError('Cannot compare %s vs %s: %s'\
                            % (str(self), str(other), why))

    def encode(self, **kwargs):
        """
            encode() -> string
            
            BER encode object payload whenever possible
        """
        self.update(kwargs)
        
        try:
            return self._encode()

        except AttributeError, why:
            raise TypeError('No encoder defined for %s object' %\
                            self.__class__.__name__)

        except KeyError, why:
            raise TypeError('Missing mandatory parameter: %s' % why)
    
        except StandardError, why:
            raise BadArgument('Encoder failure (bad input?): ' + str(why))
            
    def decode(self, input):
        """
            decode(input) -> (rest)
            
            BER decode input (string) into ASN1 object payload, return
            the rest of input stream.
        """
        self.clear()
        
        try:
            return self._decode(input)
        
        except AttributeError, why:
            raise TypeError('No decoder defined for %s object' %\
                            self.__class__.__name__)

        except StandardError, why:
            raise BadArgument('Decoder failure (bad input?): ' + str(why))

    #
    # Dictionary interface
    #
    
    def __getitem__(self, key):
        """
        """
        return self.value[key]

    def __setitem__(self, key, value):
        """
        """
        try:
            if self._filter(key, value):
                raise TypeError('Unexpected value type for %s: %s'\
                                % (key, repr(value)))
        except AttributeError:
            pass
        
        self.value[key] = value

    def keys(self):
        """
        """
        return self.value.keys()

    def has_key(self, key):
        """
        """
        return self.value.has_key(key)

    def get(self, key, default):
        """
        """
        if self.value.has_key(key):
            return self.value[key]

        return default

    def update(self, args):
        """
        """
        if not hasattr(self, 'value'):
            self.value = {}

        for key in self.ARGS.keys():
            if args.has_key(key):
                self[key] = args[key]
            elif self.ARGS[key] is not None and not self.has_key(key):
                self[key] = self.ARGS[key]

    def clear(self):
        """
        """
        self.value = {}
        
    def copy(self, other):
        """Attempt to copy the payload of instances of the same class
        """
        try:
            result = self.__class__.__name__ != other.__class__.__name__
            
        except:
            result = 1

        if result:
            raise TypeError('Type mismatch for copy operation %s vs %s'\
                            % (str(self), str(other)))

        try:
            try:
                return self._copy(other)

            except AttributeError:
                raise TypeError('No copy method defined for %s object' %\
                                self.__class__.__name__)
        
        except StandardError, why:
            raise TypeError('Cannot copy %s from %s: %s'\
                            % (str(self), str(other), why))
        
class BINDINGS(SNMPOBJECT):
    """
    """
    ARGS   = { 'encoded_oids' :  [],
               'encoded_vals' :  [] }

    FILTER = { 'encoded_oids' :  ['OBJECTID'],
               'encoded_vals' :  ['NULL', 'INTEGER', 'OCTETSTRING',\
                                  'OBJECTID', 'IPADDRESS', 'COUNTER32',\
                                  'UNSIGNED32', 'GAUGE32', 'TIMETICKS',\
                                  'OPAQUE'] }

    def _filter(self, key, value):
        """
        """
        if not value or not self.FILTER.has_key(key):
            return

        for val in value:
            object = asn1.decode(val)[0]
            if not object.__class__.__name__ in self.FILTER[key]:
                return -1

    def _encode(self):
        """
            _encode() -> octet stream

            Bind together encoded object IDs and their associated values
            (lists of strings) into bindings.
        """
        # Initialize stuff
        index = 0
        encoded_oid_pairs = ''

        # XXX handle unequal pairs
        
        # Encode encoded objid's and encoded values together
        while index < len(self['encoded_oids']):
            # Encode and concatinate one oid_pair
            if self['encoded_vals'] and \
               self['encoded_vals'][index]:
                # Merge oid with value
                oid_pairs = self['encoded_oids'][index] + \
                            self['encoded_vals'][index]
            else:
                # Merge oid with value
                oid_pairs = self['encoded_oids'][index] + \
                            asn1.NULL().encode()

            # Encode merged pairs
            encoded_oid_pairs = encoded_oid_pairs + \
                asn1.SEQUENCE(oid_pairs).encode()

            # Progress index
            index = index + 1

        # Return encoded bindings
        return asn1.SEQUENCE(encoded_oid_pairs).encode()

    def _decode(self, input):
        """
           _decode(input)
           
           Decode input octet stream (string) into lists or encoded
           Object IDs and their associated values (lists of strings).
        """
        (bindings, rest) = asn1.SEQUENCE().decode(input)
            
        # Initialize objids and vals lists
        self['encoded_oids'] = []
        self['encoded_vals'] = []
        
        # Walk over bindings
        while bindings:
            # Unpack one binding
            (binding, bindings) = asn1.SEQUENCE().decode(bindings)

            # Get OID
            oid = asn1.OBJECTID()
            binding = oid.decode(binding)[1]
            self['encoded_oids'].append(oid.encode())

            # Get value
            (val, binding) = asn1.decode(binding)
            self['encoded_vals'].append(val.encode())

            # Nothing should left out
            if binding:
                raise TypeError('Trailing garbage in binding: %s' % repr(binding))
        return rest

class RR_PDU(SNMPOBJECT):
    """
    """
    ARGS = { 'request_id'   :  0,
             'error_status' :  0,
             'error_index'  :  0,
             'tag'          :  None,
             'bindings'     :  None }

    FILTER = { 'error_status' :  range(0, 6) }
                            
    def _filter(self, key, value):
        """
        """
        if value is None or not self.FILTER.has_key(key):
            return

        if not value in self.FILTER[key]:
            return -1
    
    def _cmp(self, other):
        """
        """
        if self['request_id'] == other['request_id']:
            return 0

        return -1

    def _encode(self):
        """
           _encode() -> octet stream

           Encode PDU type (string), request ID (integer), error status and
           index (integers) alone with variables bindings (string) into
           SNMP PDU.
        """
        return eval(self['tag']+'_PDU')(\
               asn1.INTEGER(self['request_id']).encode() + \
               asn1.INTEGER(self['error_status']).encode() + \
               asn1.INTEGER(self['error_index']).encode() + \
               self['bindings']).encode()

    def _decode(self, input):
        """
           _decode(input) -> (value, rest)
           
           Decode SNMP PDU (string), return PDU type (string), request
           serial ID (integer), error status (integer), error index (integer)
           and variables bindings (string).

           See RFC 1157 for details.
        """
        # Decode PDU
        tag = self.decode_tag(ord(input[0]))
        (pdu, rest) = eval(tag+'()').decode(input)
        self['tag'] = tag[:-4]

        # Get request ID, error status and error index from PDU
        for key in ('request_id', 'error_status', 'error_index'):
            (self[key], pdu) = asn1.INTEGER().decode(pdu)

        # Get variables bindings
        self['bindings'] = pdu
        
        return rest

class MESSAGE(SNMPOBJECT):
    """
    """
    ARGS = { 'version'   :  0,
             'community' : 'public',
             'pdu'       :  None }

    FILTER = { 'pdu'     :  ['GETREQUEST_PDU', 'GETNEXTREQUEST_PDU', \
                             'GETRESPONSE_PDU', 'SETREQUEST_PDU', \
                             'TRAPREQUEST_PDU' ] }

    def _filter(self, key, value):
        """
        """
        if not value or not self.FILTER.has_key(key):
            return

        try:
            tag = self.decode_tag(ord(value[0]))

        except error.UnknownTag:
            return -1

        if not tag in self.FILTER[key]:
            return -1

    def _cmp(self, other):
        """
        """
        if self['version'] == other['version'] or \
           self['community'] == other['community']:
            return 0

        return -1

    def _encode(self):
        """
           _encode() -> octet stream

           Encode SNMP version, community name and PDU into SNMP message.
        """
        return asn1.SEQUENCE( \
               asn1.INTEGER(self['version']).encode() + \
               asn1.OCTETSTRING(self['community']).encode() + \
               self['pdu']).encode()

    def _decode(self, input):
        """
           _decode(input) -> (value, rest)

           Parse SNMP message (string), return SNMP protocol version used
           (integer), community name (string) and SNMP PDU (string).
        """
        # Unpack message
        (message, rest) = asn1.SEQUENCE().decode(input)
        
        # Get SNMP version
        (self['version'], message) = asn1.INTEGER().decode(message)

        # Get SNMP community name
        (self['community'], self['pdu']) = \
                            asn1.OCTETSTRING().decode(message)
        return rest

    def decode_header(self, input):
        """
           _decode(input) -> (value, rest)

           Parse SNMP message (string), return SNMP protocol version used
           (integer) and community name (string).
        """
        # Unpack message
        (message, rest) = asn1.SEQUENCE().decode(input)
        
        # Get SNMP version
        (self['version'], message) = asn1.INTEGER().decode(message)

        # Get SNMP community name
        (self['community'], pdu) = \
                            asn1.OCTETSTRING().decode(message)
        if pdu:
            return (pdu, rest)
        else:
            return (None, rest)

class RROBJECT:
    """Base class for various SNMP requests&response
    """
    def __init__(self, **kwargs):
        """
        """
        kwargs['tag'] = self.__class__.__name__
        
        self.bindings = BINDINGS()
        if not hasattr(self, 'pdu'):
            self.pdu = RR_PDU()
        self.msg = MESSAGE()
        
        self.update(kwargs)

    def __str__(self):
        """
        """
        return str(self.bindings) + ' ' + str(self.pdu) + ' '+ str(self.msg)

    def __repr__(self):
        """Return native representation of instance payload
        """
        res = ''
        for member in self.bindings, self.pdu, self.msg:
            for key in member.keys():
                if res:
                    res = res + ', ' + key + '=' + repr(member[key]) 
                else:    
                    res = key + '=' + repr(member[key])
        return self.__class__.__name__ + '(' + res + ')'        

    def __cmp__(self, other):
        """Compare two requests
        """
        return not (self.pdu == other and self.msg == other)
    
    def encode(self, **kwargs):
        """
           encode([kwargs]) -> octet stream

           Encode entire SNMP message into BER octet-stream.
        """
        self.update(kwargs)
        return self.msg.encode(pdu=self.pdu.encode(bindings=\
                                                   self.bindings.encode()))

    def decode(self, input):
        """
           decode(octet-stream) -> rest

           Decode input octet-stream (string) into SNMP message and return
           the rest of unprocessed input.
        """
        # Unpack message
        rest = self.msg.decode(input)

        # Decode PDU
        if self.pdu.decode(self.msg['pdu']):
            raise BadEncoding('Trailing garbage in PDU: '+ repr(garbage))

        if self.pdu['tag'] != self.__class__.__name__:
            raise BadPDUType('Unmatched PDU type: %s vs %s' % \
                                   (self.pdu['tag'], \
                                    self.__class__.__name__))

        # Decode variables bindings
        if self.bindings.decode(self.pdu['bindings']):
            raise BadEncoding('Trailing garbage in bindings: ' + repr(garbage))

        return rest

    #
    # Dictionary interface
    #

    def __getitem__(self, key):
        """Attempt to get requested item from either of message components XXX
        """
        if self.bindings.has_key(key):
            return self.bindings[key]
        if self.pdu.has_key(key):
            return self.pdu[key]
        if self.msg.has_key(key):
            return self.msg[key]
        
    def __setitem__(self, key, value):
        """Attempt to re-assign requested item to either of message
           components XXX
        """
        for part in self.msg, self.pdu, self.bindings:
            if part.has_key(key):
                part[key] = value
                return

        raise TypeError('Unexpected key=value %s object type'\
                            % (self.__class__.__name__))
    
    def keys(self):
        """Return keys for all message components
        """
        return self.bindings.keys() + \
               self.pdu.keys() + \
               self.msg.keys()

    def has_key(self, key):
        """Invoke has_key() against all message components
        """
        for comp in self.bindings, self.pdu, self.msg:
            if comp.has_key(key):
                return 1

    def get(self, key, default):
        """Get item by key with default
        """
        if self.has_key(key):
            return self[key]

        return default
    
    def update(self, args):
        """Commit passed dictionary to either of message components
        """
        for comp in self.bindings, self.pdu, self.msg:
            comp.update(args)

    def clear(self):
        """Clear all message components
        """
        for comp in self.bindings, self.pdu, self.msg:
            comp.clear()

    def copy(self, other):
        """Copy all message components from passed message
        """
        self.bindings.copy(other.bindings)
        self.pdu.copy(other.pdu)
        self.msg.copy(other.msg)

class REQUESTOBJECT(RROBJECT):
    """Base class for SNMP v.1 requests
    """
    def reply(self, **kwargs):
        """Build reply message based on ourselves
        """
        # Create response object
        rsp = GETRESPONSE()

        # Initialize it from ourselves
        rsp.update(self)

        # Fix inherited request type
        rsp.update({'tag': 'GETRESPONSE'})

        # Apply optional arguments
        rsp.update(kwargs)
        
        return rsp
    
class RESPONSEOBJECT(RROBJECT):
    """Base class for SNMP v.1 response
    """
    pass

class GETREQUEST(REQUESTOBJECT):
    """SNMP v.1 GETREQUEST class
    """
    pass

class GETNEXTREQUEST(REQUESTOBJECT):
    """SNMP v.1 GETNEXTREQUEST class
    """
    pass

class GETRESPONSE(RESPONSEOBJECT):
    """SNMP v.1 GETRESPONSE class
    """
    pass

class SETREQUEST(REQUESTOBJECT):
    """SNMP v.1 SETNEXTREQUEST class
    """
    pass

#
# Trap messages
#

# Generic trap types (see RFC-1157)
GENERIC_TRAP_TYPES = {
    'COLDSTART': 0x00,
    'WARMSTART': 0x01,
    'LINKDOWN': 0x02,
    'LINKUP': 0x03,
    'AUTHENTICATIONFAILURE': 0x04,
    'EGPNEIGHBORLOSS': 0x05,
    'ENTERPRISESPECIFIC': 0x06
}

class TRAP_PDU(SNMPOBJECT):
    """
    """
    ARGS = { 'agent_addr'    :  '0.0.0.0',
             'generic_trap'  :  GENERIC_TRAP_TYPES['COLDSTART'],
             'specific_trap' :  0,
             'time_stamp'    :  int(time.time()),
             'enterprise'    :  None,
             'tag'           :  None,
             'bindings'      :  None }

    FILTER = { 'generic_trap':  range(0, 7) }

    def _filter(self, key, value):
        """
        """
        if value is None or not self.FILTER.has_key(key):
            return

        if not value in self.FILTER[key]:
            return -1

    def _encode(self):
        """
           _encode() -> octet stream

           Encode enterpise Object-ID (given as a list of integer subIDs),
           agent IP address (string), generic trap type (integer), specific
           trap type (integer), timeticks (integer) and variable bindings
           (string) into SNMP Trap-PDU (see RFC-1157 for details)
        """
        return eval(self['tag']+'_PDU')(\
               asn1.OBJECTID(self.value['enterprise']).encode() + \
               asn1.IPADDRESS(self['agent_addr']).encode() + \
               asn1.INTEGER(self['generic_trap']).encode() + \
               asn1.INTEGER(self['specific_trap']).encode() + \
               asn1.TIMETICKS(self['time_stamp']).encode() + \
               self['bindings']).encode()

    def _decode(self, input):
        """
           _decode(input) -> (value, rest)

           Decode SNMP trap PDU (string) to enterpise Object-ID (list of
           integer sub-IDs), agent IP address (string), generic trap type
           (integer), specific trap type (integer), timeticks (integer) and
           variable bindings (string).

           See RFC-1157 for details.
        """
        # Decode PDU
        tag = self.decode_tag(ord(input[0]))
        (pdu, rest) = eval(tag+'()').decode(input)
        self['tag'] = tag[:-4]

        # Get enterprise Object ID
        (self['enterprise'], pdu) = asn1.OBJECTID().decode(pdu)

        # Get agent address
        (self['agent_addr'], pdu) = asn1.IPADDRESS().decode(pdu)        

        # Get generic and specific traps
        for key in ('generic_trap', 'specific_trap'):
            (self[key], pdu) = asn1.INTEGER().decode(pdu)

        # Get time stamp
        (self['time_stamp'], pdu) = asn1.TIMETICKS().decode(pdu)
        
        # Get variables bindings
        self['bindings'] = pdu
        
        return rest

class TR(REQUESTOBJECT):
    """Base class for SNMP v.1 TRAP requests
    """
    def __init__(self, **kwargs):
        """
        """
        self.pdu = TRAP_PDU()
        REQUESTOBJECT.__init__(self)
        self.update(kwargs)
        
class TRAPREQUEST(TR):
    """
    """
    pass

#
# Input data neutral decoding function
#

def decode(input):
    """
       decode(input) -> (SNMPOBJECT, rest)
       
       Decode input octet stream (string) into a SNMPOBJECT and return
       the rest of input (string).
    """
    msg = MESSAGE()
    (pdu, rest) = msg.decode_header(input)

    if msg['version'] > 0:
        raise BadVersion('Unsupported SNMP protocol version: '\
                         + str(msg['version']))

    try:
        # Probe PDU
        tag = BERHEADER().decode_tag(ord(pdu[0]))

    except StandardError, why:
        raise BadEncoding('Decoder failure (bad input?): ' + str(why))

    try:
        # Create request object of matching type
        msg = eval(tag[:-4]+'()')

    except NameError, why:
        raise BadPDUType('Unsuppored SNMP PDU type: ' + str(why))

    # Decode request
    rest = msg.decode(input)
    
    return (msg, rest)
