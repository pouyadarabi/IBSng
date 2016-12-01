"""
   Basic Encoding Rules (BER) for fundamental and non-structured SNMP
   application specific ASN.1 data types.

   Written by Ilya Etingof <ilya@glas.net>, 1999-2002.

   This code is partially derived from Simon Leinen's <simon@switch.ch>
   BER Perl module.
"""
import string

# Import package components
import error

class Error(error.Generic):
    """Base class for asn1 module exceptions
    """
    pass

class UnknownTag(Error):
    """Unknown BER tag
    """
    pass

class OverFlow(Error):
    """Data item does not fit the packet
    """
    pass

class UnderRun(Error):
    """Short BER data stream
    """
    pass

class BadEncoding(Error):
    """Incorrect BER encoding
    """
    pass

class TypeError(Error):
    """ASN.1 data type incompatibility
    """
    pass

class BadArgument(Error):
    """Malformed argument
    """
    pass

class BERHEADER:
    """BER packet header encoders & decoders
    """
    # BER class types
    CLASS = { 
        'UNIVERSAL'          : 0x00,
        'APPLICATION'        : 0x40,
        'CONTEXT'            : 0x80,
        'PRIVATE'            : 0xC0,
        }

    # BER format types
    FORMAT = {
        'SIMPLE'             : 0x00,
        'CONSTRUCTED'        : 0x20
        }
    
    # BER tags for various ASN.1 data types
    TAGS = {
        # Primitive ASN.1 types tags
        'BOOLEAN'            : 0x00 | FORMAT['SIMPLE'] | CLASS['UNIVERSAL'],
        'INTEGER'            : 0x02 | FORMAT['SIMPLE'] | CLASS['UNIVERSAL'],
        'BITSTRING'          : 0x03 | FORMAT['SIMPLE'] | CLASS['UNIVERSAL'],
        'OCTETSTRING'        : 0x04 | FORMAT['SIMPLE'] | CLASS['UNIVERSAL'],
        'NULL'               : 0x05 | FORMAT['SIMPLE'] | CLASS['UNIVERSAL'],
        'OBJECTID'           : 0x06 | FORMAT['SIMPLE'] | CLASS['UNIVERSAL'],
        'SEQUENCE'           : 0x10 | FORMAT['CONSTRUCTED'] | CLASS['UNIVERSAL'],
        'SET'                : 0x11 | FORMAT['CONSTRUCTED'] | CLASS['UNIVERSAL'],
        # Primitive SNMP application specific tags
        'IPADDRESS'          : 0x00 | FORMAT['SIMPLE'] | CLASS['APPLICATION'],
        'COUNTER32'          : 0x01 | FORMAT['SIMPLE'] | CLASS['APPLICATION'],
        'UNSIGNED32'         : 0x02 | FORMAT['SIMPLE'] | CLASS['APPLICATION'],
        'GAUGE32'            : 0x02 | FORMAT['SIMPLE'] | CLASS['APPLICATION'],
        'TIMETICKS'          : 0x03 | FORMAT['SIMPLE'] | CLASS['APPLICATION'],
        'OPAQUE'             : 0x04 | FORMAT['SIMPLE'] | CLASS['APPLICATION'],
        'NSAPADDRESS'        : 0x05 | FORMAT['SIMPLE'] | CLASS['APPLICATION'],
        'COUNTER64'          : 0x06 | FORMAT['SIMPLE'] | CLASS['APPLICATION'],
        # SNMP v.2 exception tags
        'noSuchObject'       : 0x00 | FORMAT['SIMPLE'] | CLASS['CONTEXT'],
        'noSuchInstance'     : 0x01 | FORMAT['SIMPLE'] | CLASS['CONTEXT'],
        'endOfMibView'       : 0x02 | FORMAT['SIMPLE'] | CLASS['CONTEXT']
        }

    def encode_tag(self, name):
        """
           encode_tag(name) -> octet stream
           
           Encode ASN.1 data item (specified by name) into its numeric
           representation.
        """
        # Lookup the tag ID by name
        if self.TAGS.has_key(name):
            return '%c' % self.TAGS[name]
    
        raise UnknownTag('Unknown tag: ' + name)

    def encode_length(self, length):
        """
           encode_length(length) -> octet string
           
           Encode ASN.1 data item length (integer) into octet stream
           representation.
        """
        # If given length fits one byte
        if length < 0x80:
            # Pack it into one octet
            return '%c' % length
        
        # One extra byte required
        elif length < 0xFF:
            # Pack it into two octets
            return '%c%c' % (0x81, length)
        
        # Two extra bytes required
        elif length < 0xFFFF:
            # Pack it into three octets
            return '%c%c%c' % (0x82, \
                               (length >> 8) & 0xFF, \
                               length & 0xFF)
        
        # Three extra bytes required
        elif length < 0xFFFFFF:
            # Pack it into three octets
            return '%c%c%c%c' % (0x83, \
                                 (length >> 16) & 0xFF, \
                                 (length >> 8) & 0xFF, \
                                 length & 0xFF)
        
        # More octets may be added
        else:
            raise OverFlow('Too large length: ' + str(length))

    def decode_tag(self, tag):
        """
           decode_tag(tag) -> name
           
           Decode a tag (octet) into symbolic representation of ASN.1 data
           item type tag.
        """
        # Lookup tag in the dictionary of known tags
        for key in self.TAGS.keys():
            if tag == self.TAGS[key]:
                return key
            
        raise UnknownTag('Unknown tag: ' + repr(tag))

    def decode_length(self, input):
        """
           decode_length(input) -> (length, size)
           
           Return the data item's length (integer) and the size of length
           data (integer).
        """
        try:
            # Get the most-significant-bit
            msb = ord(input[0]) & 0x80
            if not msb:
                return (ord(input[0]) & 0x7F, 1)

            # Get the size if the length
            size = ord(input[0]) & 0x7F

            # One extra byte length
            if msb and size == 1:
                return (ord(input[1]), size+1)
            
            # Two extra bytes length
            elif msb and size == 2:
                result = ord(input[1])
                result = result << 8
                return (result | ord(input[2]), size+1)

            # Two extra bytes length
            elif msb and size == 3:
                result = ord(input[1])
                result = result << 8
                result = result | ord(input[2])
                result = result << 8
                return (result | ord(input[3]), size+1)

            else:
                raise OverFlow('Too many length bytes: ' + str(size))

        except StandardError, why:
            raise BadEncoding('Malformed input: ' + str(why))


#
# ASN.1 object classes
#

class ASN1OBJECT(BERHEADER):
    """
       Basic ASN.1 object. Defines behaviour and properties of
       various ASN.1 objects.
    """
    def __init__(self, value=None):
        """Store ASN.1 value
        """
        self.value = None
        self.update(value)

    def __str__(self):
        """Return string representation of class instance
        """
        return '%s: %s' % (self.__class__.__name__, str(self.value))

    def __repr__(self):
        """Return native representation of instance payload
        """
        return self.__class__.__name__ + '(' + repr(self.value) + ')'

    def __call__(self):
        """Return instance payload
        """
        if self.value is None:
            raise BadArgument('Uninitialized object payload')
        
        return self.value

    def __cmp__(self, other):
        """Attempt to compare the payload of instances of the same class
        """
        try:
            return self._cmp(other)

        except AttributeError:
            pass

        except StandardError, why:
            raise TypeError('Cannot compare %s vs %s: %s'\
                            % (str(self), str(other), why))

        return cmp(self.value, other)

    def update(self, value):
        """
        """
        if value is None:
            return
        
        if hasattr(self, '_range'):
            try:
                if self._range(value):
                    raise OverFlow('Value %s does not fit the %s type' \
                                   % (str(value), self.__class__.__name__))

            except StandardError, why:
                raise TypeError('Cannot range check value %s: %s'\
                                % (str(value), why))
            
        self.value = value

    def encode(self, value=None):
        """
            encode() -> string
            
            BER encode object payload whenever possible
        """
        self.update(value)
        
        try:
            result = self._encode()

            return self.encode_tag(self.__class__.__name__) + \
                   self.encode_length(len(result)) + result

        except AttributeError:
            raise TypeError('No encoder defined for %s object' %\
                            self.__class__.__name__)

        except StandardError, why:
            raise BadArgument('Encoder failure (bad input?): ' + str(why))
    
    def decode(self, input):
        """
            decode(input) -> (value, rest)
            
            BER decode input (string) into ASN1 object payload, return
            the rest of input stream.
        """
        try:
            tag = self.decode_tag(ord(input[0]))

            if tag != self.__class__.__name__:
                raise TypeError('Type mismatch: %s vs %s' %\
                                (self.__class__.__name__, tag))
            
            (length, size) = self.decode_length(input[1:])

            if len(input) < length:
                raise UnderRun('Short input')

            self.update(self._decode(input[1+size:1+size+length]))
            
            return (self.value, input[1+size+length:])

        except AttributeError:
            raise TypeError('No decoder defined for %s object' %\
                            self.__class__.__name__)

        except StandardError, why:
            raise BadEncoding('Decoder failure (bad input?): '\
                                    + str(why))
    
class INTEGER(ASN1OBJECT):
    """An ASN.1, indefinite length integer object
    """
    def __init__(self, value=None):
        """Invoke base class constructor and install specific defaults
        """
        ASN1OBJECT.__init__(self, value)

    def _encode(self):
        """
           _encode() -> octet stream
           
           Encode tagged integer into octet stream.
        """
        result = ''
        integer = self.value
        
        # The 0 and -1 values need to be handled separately since
        # they are the terminating cases of the positive and negative
        # cases repectively.
        if integer == 0:
            result = '\000'
            
        elif integer == -1:
            result = '\377'
            
        elif integer < 0:
            while integer <> -1:
                (integer, result) = integer>>8, chr(integer & 0xff) + result
                
            if ord(result[0]) & 0x80 == 0:
                result = chr(0xff) + result
        else:
            while integer > 0:
                (integer, result) = integer>>8, chr(integer & 0xff) + result
                
            if (ord(result[0]) & 0x80 <> 0):
                result = chr(0x00) + result

        return result

    def _decode(self, input):
        """
           _decode(input)
           
           Decode octet stream into signed ASN.1 integer (of any length).
        """
        bytes = map(ord, input)

        if bytes[0] & 0x80:
            bytes.insert(0, -1L)

        result = reduce(lambda x,y: x<<8 | y, bytes, 0L)

        try:
            return int(result)

        except OverflowError:
            return result

class UNSIGNED32(INTEGER):
    """ASN.1 UNSIGNED32 object
    """
    def __init__(self, value=None):
        """
           Invoke base class constructor and install specific defaults
        """
        INTEGER.__init__(self, value)

    def _decode(self, input):
        """
           _decode(input)
           
           Decode octet stream into unsigned ASN.1 integer (of any length).
        """
        bytes = map(ord, input)

        if bytes[0] & 0x80:
            bytes.insert(0, 0xffffffffL)

        res = reduce(lambda x,y: x<<8 | y, bytes, 0L)

        # Attempt to return int whenever possible
        try:
            return int(res)

        except OverflowError:
            return res

    def _range(self, value):
        """
        """
        return value < 0 or value & ~0xffffffffL

class TIMETICKS(UNSIGNED32):
    """ASN.1 TIMETICKS object
    """
    pass

class UPTIME(UNSIGNED32):
    """ASN.1 UPTIME object
    """
    pass

class COUNTER32(UNSIGNED32):
    """ASN.1 COUNTER32 object
    """
    pass

class GAUGE32(UNSIGNED32):
    """ASN.1 GAUGE32 object
    """
    pass

class COUNTER64(UNSIGNED32):
    """ASN.1 COUNTER64 object
    """
    def __init__(self, value=None):
        """Invoke base class constructor and install specific defaults
        """
        UNSIGNED32.__init__(self, value)
        
    def _range(self, value):
        """
        """
        return value < 0 or value & ~0xffffffffffffffffL
    
class SEQUENCE(ASN1OBJECT):
    """ASN.1 sequence object
    """
    def _encode(self):
        """
           _encode() -> octet stream

           Encode ASN.1 sequence (specified as string) into octet
           string.
        """
        if self.value is None:
            return ''
        return self.value

    def _decode(self, input):
        """
           _decode(input)
           
           Decode octet stream into ASN.1 sequence.
        """
        return input

class OPAQUE(SEQUENCE):
    """ASN.1 opaque object
    """
    pass

class OCTETSTRING(SEQUENCE):
    """ASN.1 octet string object
    """
    pass

class OBJECTID(ASN1OBJECT):
    """ASN.1 Object ID object (taken and returned as string in conventional
       "dotted" representation)
    """
    def _encode(self):
        """
           _encode() -> octet stream
           
           Encode ASN.1 Object ID into octet stream.
        """
        # Turn string type Object ID into numeric representation
        oid = self.str2num(self.value)

        # Make sure the Object ID is long enough
        if len(oid) < 2:
            raise BadArgument('Short Object ID: ' + str(oid))

        # Build the first twos
        index = 0
        result = oid[index] * 40
        result = result + oid[index+1]
        try:
            result = [ '%c' % int(result) ]

        except OverflowError:
            raise BadArgument('Too large initial sub-IDs: ' + str(oid[index:]))

        # Setup index
        index = index + 2

        # Cycle through subids
        for subid in oid[index:]:
            if subid > -1 and subid < 128:
                # Optimize for the common case
                result.append('%c' % (subid & 0x7f))

            elif subid < 0 or subid > 0xFFFFFFFFL:
                raise BadArgument('Too large Sub-Object ID: ' + str(subid))

            else:
                # Pack large Sub-Object IDs
                res = [ '%c' % (subid & 0x7f) ]
                subid = subid >> 7
                while subid > 0:
                    res.insert(0, '%c' % (0x80 | (subid & 0x7f)))
                    subid = subid >> 7

                # Convert packed Sub-Object ID to string and add packed
                # it to resulted Object ID
                result.append(string.join(res, ''))

        # Convert BER encoded Object ID to string and return
        return string.join(result, '')
        
    def _decode(self, input):
        """
           _decode(input)
           
           Decode octet stream into ASN.1 Object ID
        """
        oid = []
        index = 0

        # Get the first subid
        subid = ord(input[index])
        oid.append(int(subid / 40))
        oid.append(int(subid % 40))

        index = index + 1

        # Loop through the rest
        while index < len(input):
            # Get a subid
            subid = ord(input[index])

            if subid < 128:
                oid.append(subid)
                index = index + 1
            else:
                # Construct subid from a number of octets
                next = subid
                subid = 0
                while next >= 128:
                    # Collect subid
                    subid = (subid << 7) + (next & 0x7F)

                    # Take next octet
                    index = index + 1
                    next = ord(input[index])

                    # Just for sure
                    if index > len(input):
                        raise BadArgument('Malformed sub-Object ID')

                # Append a subid to oid list
                subid = (subid << 7) + next
                oid.append(subid)
                index = index + 1

        # Turn numeric Object ID into string representation
        return self.num2str(oid)        

    def _cmp(self, other):
        """
        """
        return cmp(self.str2num(self.value), self.str2num(other()))

    def isaprefix(self, other):
        """
           isaprefix(other) -> boolean
           
           Compare our own OID with the other one (given as a string),
           return non-None if ours is a prefix of the other OID.

           This is intended to be used for MIB tables retrieval.
        """
        # Convert into numeric
        value = self.str2num(self.value)
        ovalue = self.str2num(other)

        # Pick the shortest oid
        if len(value) <= len(ovalue):
            # Get the length
            length = len(value)

            # Compare oid'es
            if value[:length] == ovalue[:length]:
                return not None

        # Our OID turned to be greater than the other
        return None

    def str2num(self, soid):
        """
            str2num(soid) -> noid
            
            Convert Object ID "soid" presented in a dotted form into an
            Object ID "noid" represented as a list of numeric sub-ID's.
        """    
        # Convert string into a list and filter out empty members
        # (leading dot causes this)
        try:
            toid = filter(lambda x: len(x), string.split(soid, '.'))

        except:
            raise BadArgument('Malformed Object ID: ' + str(soid))

        # Convert a list of symbols into a list of numbers
        try:
            noid = map(lambda x: string.atol(x), toid)

        except:
            raise BadArgument('Malformed Object ID: ' + str(soid))

        if not noid:
            raise BadArgument('Empty Object ID: ' + str(soid))

        return noid

    def num2str(self, noid):
        """
            num2str(noid) -> snoid
            
            Convert Object ID "noid" presented as a list of numeric
            sub-ID's into Object ID "soid" in dotted notation.
        """    
        if not noid:
            raise BadArgument('Empty numeric Object ID')

        # Convert a list of number into a list of symbols and merge all
        # list members into a string
        try:
            soid = reduce(lambda x, y: x+y,\
                          map(lambda x: '.%lu' % x, noid))
        except:
            raise BadArgument('Malformed numeric Object ID: '+ str(noid))
 
        if not soid:
            raise BadArgument('Empty numeric Object ID: ' + str(noid))

        return soid

class IPADDRESS(ASN1OBJECT):
    """ASN.1 IP address object (taken and returned as string in conventional
       "dotted" representation)
    """
    def _encode(self):
        """
           _encode() -> octet stream
           
           Encode ASN.1 IP address into octet stream.
        """
        # Assume address is given in dotted notation
        try:
            packed = string.split(self.value, '.')

        except:
            raise BadArgument('Malformed IP address: '+ str(self.value))
        
        # Make sure it is four octets length
        if len(packed) != 4:
            raise BadArgument('Malformed IP address: '+ str(self.value))

        # Convert string octets into integer counterparts
        # (this is still not immune to octet overflow)
        try:
            packed = map(lambda x: string.atoi (x), packed)
        except string.atoi_error:
            raise BadArgument('Malformed IP address: '+ str(self.value))
        
        # Build a result
        result = '%c%c%c%c' % (packed[0], packed[1],\
                               packed[2], packed[3])

        # Return encoded result
        return result

    def _decode(self, input):
        """
           _decode(input)
           
           Decode octet stream into ASN.1 IP address
        """
        if len(input) != 4:
            raise BadEncoding('Malformed IP address: '+ str(input))

        return '%d.%d.%d.%d' % \
               (ord(input[0]), ord(input[1]), \
                ord(input[2]), ord(input[3]))
        
class NULL(ASN1OBJECT):
    """ASN.1 NULL object
    """
    def _encode(self):
        """
           _encode() -> octet stream
           
           Encode ASN.1 NULL object into octet stream.
        """
        return ''

    def _decode(self, input):
        """
           _decode(input)
           
           Decode octet stream into ASN.1 IP address
        """
        if input:
            raise BadEncoding('Non-empty NULL value: %s' % str(input))

        return ''

    def _range(self, value):
        """
        """
        return value

class noSuchObject(NULL):
    """SNMP v.2 noSuchObject exception
    """
    pass

class noSuchInstance(NULL):
    """SNMP v.2 noSuchInstance exception
    """
    pass

class endOfMibView(NULL):
    """SNMP v.2 endOfMibView exception
    """
    pass

#
# BER data stream decoder
#

def decode(input):
    """
       decode(input) -> (asn1, rest)
       
       Decode input octet stream (string) into ASN.1 object and return
       the rest of input (string).
    """
    tag = BERHEADER().decode_tag(ord(input[0]))
    
    try:
        object = eval(tag + '()')
        return (object, object.decode(input)[1])

    except NameError, why:
        raise UnknownTag('Unsuppored ASN.1 data type: %s' % tag)
    
    except StandardError, why:
        raise BadEncoding('Decoder failure (bad input?): ' + str(why))
