"""
   Basic Encoding Rules (BER) for structured, SNMP v.2c specific ASN.1 data
   types (SNMP messages).

   Written by Ilya Etingof <ilya@glas.net>, 2002.
"""
import types
import time
import string

# Import package components
import asn1
import v1

class Error(v1.Error):
    """Base class for v2 module exceptions
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

class BadPDUType(Error):
    """Bad PDU type
    """
    pass

class SNMPError(v1.SNMPError):
    """Represent an RFC 1905 SNMP error.
    """
    # Taken from UCD SNMP code
    ERRORS = [
        '(noError) No Error',
        '(tooBig) Response message would have been too large.',
        '(noSuchName) There is no such variable name in this MIB.',
        '(badValue) The value given has the wrong type or length.',
        '(readOnly) The two parties used do not have access to use the specified SNMP PDU.',
        '(genError) A general failure occured.',
        # The rest is for V2c only
        '(noAccess) Access denied.',
        '(wrongType) Wrong BER type',
        '(wrongLength) Wrong BER length.',
        '(wrongEncoding) Wrong BER encoding.',
        '(wrongValue) Wrong value.',
        '(noCreation) ',
        '(inconsistentValue) ',
        '(resourceUnavailable) ',
        '(commitFailed) ',
        '(undoFailed) ',
        '(authorizationError) ',
        '(notWritable) ',
        '(inconsistentName) '
    ]

class BERHEADER(v1.BERHEADER):
    """Extended, SNMP v.2 specific ASN.1 data types
    """
    # v.2 PDU tags
    TAGS = {
        'GETREQUEST_PDU'     : 0x00 | v1.BERHEADER.FORMAT['CONSTRUCTED'] \
                                    | v1.BERHEADER.CLASS['CONTEXT'],
        'GETNEXTREQUEST_PDU' : 0x01 | v1.BERHEADER.FORMAT['CONSTRUCTED'] \
                                    | v1.BERHEADER.CLASS['CONTEXT'],
        'RESPONSE_PDU'       : 0x02 | v1.BERHEADER.FORMAT['CONSTRUCTED'] \
                                    | v1.BERHEADER.CLASS['CONTEXT'],
        'SETREQUEST_PDU'     : 0x03 | v1.BERHEADER.FORMAT['CONSTRUCTED'] \
                                    | v1.BERHEADER.CLASS['CONTEXT'],
        'GETBULKREQUEST_PDU' : 0x05 | v1.BERHEADER.FORMAT['CONSTRUCTED'] \
                                    | v1.BERHEADER.CLASS['CONTEXT'],
        'INFORMREQUEST_PDU'  : 0x06 | v1.BERHEADER.FORMAT['CONSTRUCTED'] \
                                    | v1.BERHEADER.CLASS['CONTEXT'],
        'TRAP_PDU'           : 0x07 | v1.BERHEADER.FORMAT['CONSTRUCTED'] \
                                    | v1.BERHEADER.CLASS['CONTEXT'],
        'REPORT_PDU'         : 0x08 | v1.BERHEADER.FORMAT['CONSTRUCTED'] \
                                    | v1.BERHEADER.CLASS['CONTEXT']
        }

#
# SNMP v.2 PDU types
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

class RESPONSE_PDU(PDU_SEQUENCE):
    """RESPONSE type ASN.1 object
    """
    pass

class SETREQUEST_PDU(PDU_SEQUENCE):
    """SETREQUEST type ASN.1 object
    """
    pass

class GETBULKREQUEST_PDU(PDU_SEQUENCE):
    """GETBULKREQUEST type ASN.1 object
    """
    pass

class INFORMREQUEST_PDU(PDU_SEQUENCE):
    """INFORMREQUEST type ASN.1 object
    """
    pass

class TRAP_PDU(PDU_SEQUENCE):
    """TRAP type ASN.1 object
    """
    pass

class REPORT_PDU(PDU_SEQUENCE):
    """REPORT type ASN.1 object
    """
    pass

#
# SNMP v.2 specific structured ASN.1 data types
#

# error_index XXX

class BINDINGS(BERHEADER, v1.BINDINGS):
    """
    """
    FILTER = { 'encoded_oids' :  ['OBJECTID'],
               'encoded_vals' :  ['NULL', 'INTEGER', 'OCTETSTRING',\
                                  'OBJECTID', 'IPADDRESS', 'COUNTER32',\
                                  'UNSIGNED32', 'GAUGE32', 'TIMETICKS',\
                                  'OPAQUE', 'COUNTER64', 'noSuchObject', \
                                  'noSuchInstance', 'endOfMibView'] }

class RR_PDU(BERHEADER, v1.RR_PDU):
    """
    """
    FILTER = { 'error_status' :  range(0, 19) }

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

class MESSAGE(BERHEADER, v1.MESSAGE):
    """
    """
    ARGS = { 'version'   :  1,
             'community' : 'public',
             'pdu'       :  None }

    FILTER = { 'pdu'     :  ['GETREQUEST_PDU', 'GETNEXTREQUEST_PDU', \
                             'RESPONSE_PDU', 'SETREQUEST_PDU', \
                             'GETBULKREQUEST_PDU', 'INFORMREQUEST_PDU', \
                             'TRAP_PDU', 'REPORT_PDU'] }
    
class RROBJECT(BERHEADER, v1.RROBJECT):
    """Base class for various SNMP v.2 requests&response
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

class REQUESTOBJECT(RROBJECT):
    """SNMP v.2 request class
    """
    def reply(self, **kwargs):
        """
        """
        # Create response object
        rsp = RESPONSE()

        # Initialize it from ourselves
        rsp.update(self)

        # Fix inherited request type
        rsp.update({'tag': 'RESPONSE'})

        # Apply optional arguments
        rsp.update(kwargs)
        
        return rsp

class RESPONSEOBJECT(RROBJECT):
    """SNMP v.2 response class
    """
    pass

class GETREQUEST(REQUESTOBJECT):
    """
    """
    pass

class GETNEXTREQUEST(REQUESTOBJECT):
    """
    """
    pass

class RESPONSE(RESPONSEOBJECT):
    """
    """
    pass

# Just an alias to RESPONSE class
GETRESPONSE = RESPONSE

class SETREQUEST(REQUESTOBJECT):
    """
    """
    pass

class INFORMREQUEST(REQUESTOBJECT):
    """
    """
    pass

class TRAP(REQUESTOBJECT):
    """
    """
    pass

# Just an alias to TRAP class
TRAPREQUEST = TRAP
class REPORT(REQUESTOBJECT):
    """
    """
    pass

#
# GETBULK request stuff
#

class BULK_PDU(BERHEADER, v1.SNMPOBJECT):
    """
    """
    ARGS = { 'request_id'      : 0,
             'non_repeaters'   : 0,
             'max_repetitions' : 0,
             'tag'             : None,
             'bindings'        : None }

    def _cmp(self, other):
        """
        """
        if self['request_id'] == other['request_id']:
            return 0

        return -1
    
    def _encode(self):
        """
            _encode() -> octet stream

           Encode non-repeaters and max-repetitions counters (integers)
           along with variables bindings (string) into SNMP V2 bulk PDU.
        """
        return eval(self['tag']+'_PDU')(\
               asn1.INTEGER(self['request_id']).encode() + \
               asn1.INTEGER(self['non_repeaters']).encode() + \
               asn1.INTEGER(self['max_repetitions']).encode() + \
               self['bindings']).encode()

    def _decode(self, input):
        """
           _decode(input) -> (value, rest)

           Decode SNMP PDU (string), return PDU type (integer), request
           serial ID (integer), error status (integer), error index (integer)
           and variables bindings (string).

           See RFC 1157 for details.
        """
        # Decode PDU
        tag = self.decode_tag(ord(input[0]))
        (pdu, rest) = eval(tag+'()').decode(input)
        self['tag'] = tag[:-4]

        # Get request ID from PDU
        (self['request_id'], pdu) = asn1.INTEGER().decode(pdu)

        # Get non repeaters and max repetitions from PDU
        for key in ('non_repeaters', 'max_repetitions'):
            (self[key], pdu) = asn1.INTEGER().decode(pdu)

        # Get variables bindings
        self['bindings'] = pdu
        
        return rest

class GETBULKREQUEST(REQUESTOBJECT):
    """SNMP v.2 GETBULK request
    """
    def __init__(self, **kwargs):
        """
        """
        self.pdu = BULK_PDU()
        REQUESTOBJECT.__init__(self)
        self.update(kwargs)
    
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

    if msg['version'] == 0:
        return v1.decode(input)

    elif msg['version'] > 1:
        raise BadVersion('Unsupported SNMP protocol version: '\
                         + str(msg['version']))
    
    try:
        tag = BERHEADER().decode_tag(ord(pdu[0]))

    except StandardError, why:
        raise BadEncoding('Decoder failure (bad input?): ' + str(why))

    try:
        # Create request object of matching type
        msg = eval(tag[:-4]+'()')

    except NameError, why:
        raise BadPDUType('Unsuppored SNMP request type: ' + str(why))

    # Decode request
    rest = msg.decode(input)
    
    return (msg, rest)
