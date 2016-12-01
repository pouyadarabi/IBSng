# packet.py
# 
# Copyright 2002 Wichert Akkerman <wichert@deephackmode.org>
#
# A RADIUS packet as defined in RFC 2138


"""
RADIUS packet 
"""

__docformat__   = "epytext en"

from core.lib.mschap import mschap,mppe
from core.lib import digest

import md5, struct, types, random, UserDict
import tools

# Packet codes
AccessRequest           = 1
AccessAccept            = 2
AccessReject            = 3
AccountingRequest       = 4
AccountingResponse      = 5
AccessChallenge         = 11
StatusServer            = 12
StatusClient            = 13
DisconnectRequest       = 40
DisconnectAck           = 41
DisconnectNack          = 42


# Current ID
CurrentID               = random.randrange(1, 255)

class PacketError(Exception):
        pass


class Packet(UserDict.UserDict):
        """Packet acts like a standard python map to provide simple access
        to the RADIUS attributes. Since RADIUS allows for repeated
        attributes the value will always be a sequence. pyrad makes sure
        to preserve the ordering when encoding and decoding packets.

        There are two ways to use the map intereface: if attribute
        names are used pyrad take care of en-/decoding data. If
        the attribute type number (or a vendor ID/attribute type
        tuple for vendor attributes) is used you work with the
        raw data.
        """

        def __init__(self, code=0, id=None, secret="", authenticator=None, **attributes):
                """Constructor

                @param dict:   RADIUS dictionary
                @type dict:    pyrad.dictionary.Dictionary class
                @param secret: secret needed to communicate with a RADIUS server
                @type secret:  string
                @param id:     packet identifaction number
                @type id:      integer (8 bits)
                @param code:   packet type code
                @type code:    integer (8bits)
                @param packet: raw packet to decode
                @type packet:  string
                """
                UserDict.UserDict.__init__(self)
                self.code=code
                if id != None:
                        self.id=id
                else:
                        self.id=CreateID()
                self.secret=secret
                self.authenticator=authenticator

                if attributes.has_key("dict"):
                        self.dict=attributes["dict"]

                if attributes.has_key("packet"):
                        self.DecodePacket(attributes["packet"])

                for (key,value) in attributes.items():
                        if key in [ "dict", "packet"]:
                                continue

                        key=key.replace("_", "-")
                        self.AddAttribute(key, value)


        def CreateReply(self, **attributes):
                return Packet(self.id, self.secret, **attributes)


        def _DecodeValue(self, attr, value):
                if attr.values.HasBackward(value):
                        return attr.values.GetBackward(value)
                else:
                        return tools.DecodeAttr(attr.type, value)
        

        def _EncodeValue(self, attr, value):
                if attr.values.HasForward(value):
                        return attr.values.GetForward(value)
                else:
                        return tools.EncodeAttr(attr.type, value)
        

        def _EncodeKeyValues(self, key, values):
                if type(key)!=types.StringType:
                        return (key, values)

                attr=self.dict.attributes[key]

                if attr.vendor:
                        key=(self.dict.vendors.GetForward(attr.vendor), attr.code)
                else:
                        key=attr.code

                return (key,
                        map(lambda v,a=attr,s=self: s._EncodeValue(a,v), values))


        def _EncodeKey(self, key):
                if type(key)!=types.StringType:
                        return key

                attr=self.dict.attributes[key]
                if attr.vendor:
                        return (self.dict.vendors.GetForward(attr.vendor), attr.code)
                else:
                        return attr.code
        

        def _DecodeKey(self, key):
                "Turn a key into a string if possible"

                if self.dict.attrindex.HasBackward(key):
                        return self.dict.attrindex.GetBackward(key)

                return key


        def AddAttribute(self, key, value):
                """Add an attribute to the packet.

                @param key:   attribute name or identification
                @type key:    string, attribute code or (vendor code, attribute code) tuple
                @param value: value
                @type value:  depends on type of attribute
                """
                (key,value)=self._EncodeKeyValues(key, [value])
                value=value[0]

                if self.data.has_key(key):
                        self.data[key].append(value)
                else:
                        self.data[key]=[value]


        def __getitem__(self, key):
                if type(key)!=types.StringType:
                        return self.data[key]

                values=self.data[self._EncodeKey(key)]
                attr=self.dict.attributes[key]
                res=[]
                for v in values:
	                    res.append(self._DecodeValue(attr, v))
                return res

        

        def has_key(self, key):
                return self.data.has_key(self._EncodeKey(key))


        def __setitem__(self, key, item):
                if type(key)==types.StringType:
                        (key,item)=self._EncodeKeyValues(key, [item])
                        self.data[key]=item
                else:
                        assert(type(item)==types.ListType)
                        self.data[key]=[item]


        def keys(self):
                return map(self._DecodeKey, self.data.keys())


        def CreateAuthenticator(self):
                """Create a packet autenticator.
                
                All RADIUS packets contain a sixteen byte authenticator which
                is used to authenticate replies from the RADIUS server and in
                the password hiding algorithm. This function returns a suitable
                random string that can be used as an authenticator.

                @return: valid packet authenticator
                @rtype: string
                """

                data=""
                for i in range(16):
                        data+=chr(random.randrange(0,256))

                return data


        def CreateID(self):
                """Create a packet ID
                
                All RADIUS requests have a ID which is used to identify
                a request. This is used to detect retries and replay
                attacks. This functino returns a suitable random number
                that can be used as ID.

                @return: ID number
                @rtype:  integer

                """
                return random.randrange(0,256)


        def ReplyPacket(self):
                """Create a ready-to-transmit authentication reply packet

                Return a RADIUS packet which can be directly transmitted
                to a RADIUS server. This differs with Packet() in how
                the authenticator is calculated.
                
                @return: raw packet
                @rtype:  string
                """
                assert(self.authenticator)
                assert(self.secret)

                attr=self._PktEncodeAttributes()
                header=struct.pack("!BBH", self.code, self.id, (20+len(attr)))

                authenticator=md5.new(header[0:4] + self.authenticator
                        + attr + self.secret).digest()

                return header + authenticator + attr


        def VerifyReply(self, reply, rawreply=None):
                if reply.id!=self.id:
                        return 0

                if rawreply==None:
                        rawreply.reply.ReplyPacket()
                
                hash=md5.new(rawreply[0:4] + self.authenticator + 
                        rawreply[20:] + self.secret).digest()

                if hash!=reply.authenticator:
                        return 0

                return 1




        def _PktEncodeAttribute(self, key, value):
                if type(key)==types.TupleType:
                        value=struct.pack("!L", key[0]) + \
                                self._PktEncodeAttribute(key[1], value)
                        key=26

                return struct.pack("!BB", key, (len(value)+2))+value


        def _PktEncodeAttributes(self):
                result=""
                for (code, datalst) in self.items():
                        for data in datalst:
                                result+=self._PktEncodeAttribute(code, data)

                return result


        def _PktDecodeVendorAttribute(self, data):
                # Check if this packet is long enough to be in the
                # RFC2865 recommended form
                if len(data)<6:
                        return (26, data)

                try:
                        vendor = struct.unpack("!L", data[:4])[0]
                        
                        if vendor == 429: #USR
                            type = struct.unpack("!L", data[4:8])[0]
                            value = data[8:]

                        else:
                            (type, length)=struct.unpack("!BB", data[4:6])[0:2]

                            # Another sanity check
                            if len(data) != length+4:
                                return (26, data)
                            
                            value = data[6:]
                            
                except struct.error:
                        raise PacketError, "Vender attribute header is corrupt"

                return ((vendor,type), value)


        def _PktDecodeDigestAttribute(self, data):
	    #decode Digest-Attributes according to draft-sterman-aaa-sip-00.txt
		try:
    			sub_type, sub_length = struct.unpack("!BB", data[:2])
		except struct.error:
                        raise PacketError, "Digest attribute header is corrupt"
		
		key = 1062 + sub_type
		value = data[2:sub_length]
		
		return key, value


        def DecodePacket(self, packet):
                """Initialize the object from raw packet data.

                Decode a packet as received from the network and decode
                it.
                
                @param packet: raw packet
                @type packet:  string"""

                try:
                        (self.code, self.id, length, self.authenticator)=struct.unpack("!BBH16s", packet[0:20])
                except struct.error:
                        raise PacketError, "Packet header is corrupt"
                if len(packet)!=length:
                        raise PacketError, "Packet has invalid length actual length:%s packet length:%s"%(len(packet),length)
                if length>8192:
                        raise PacketError, "Packet length is too long (%s)"%length

                self.clear()

                packet=packet[20:]
                while packet:
                        try:
                                (key, attrlen)=struct.unpack("!BB", packet[0:2])
                        except struct.error:
                                raise PacketError, "Attribute header is corrupt"

                        if attrlen<2 or attrlen>255:
                            raise PacketError, "Invalid attribute length (%s)"%attrlen
                            
                        value=packet[2:attrlen]
                        if key==26: #VSA
                                (key,value)=self._PktDecodeVendorAttribute(value)

			elif key == 207: #Digest
				(key,value)=self._PktDecodeDigestAttribute(value)
	    
                        if self.data.has_key(key):
                                self.data[key].append(value)
                        else:
                                self.data[key]=[value]

                        packet=packet[attrlen:]


class AuthPacket(Packet):
        def __init__(self, code=AccessRequest, id=None, secret="", authenticator=None, **attributes):
                """Constructor

                @param code:   packet type code
                @type code:    integer (8bits)
                @param id:     packet identifaction number
                @type id:      integer (8 bits)
                @param secret: secret needed to communicate with a RADIUS server
                @type secret:  string

                @param dict:   RADIUS dictionary
                @type dict:    pyrad.dictionary.Dictionary class

                @param packet: raw packet to decode
                @type packet:  string
                """
                Packet.__init__(self, code, id, secret, authenticator, **attributes)


        def CreateReply(self, **attributes):
                return AuthPacket(AccessAccept, self.id,
                        self.secret, self.authenticator, **attributes)


        def RequestPacket(self):
                """Create a ready-to-transmit authentication request packet

                Return a RADIUS packet which can be directly transmitted
                to a RADIUS server.
                
                @return: raw packet
                @rtype:  string
                """

                attr=self._PktEncodeAttributes()

                if self.authenticator==None:
                        self.authenticator=self.CreateAuthenticator()

                if self.id==None:
                        self.id=self.CreateID()

                header=struct.pack("!BBH16s", self.code, self.id,
                        (20+len(attr)), self.authenticator)

                return header+attr

	#Digest Methods
	def checkDigestPassword(self, password):
	    """
		password: clear text password of user
	    """	
	    username = self["Digest-User-Name"][0]
	    realm = self["Digest-Realm"][0]
	    nonce = self["Digest-Nonce"][0]
	    method = self["Digest-Method"][0]
	    digest_uri = self["Digest-URI"][0]
	    
	    HA1 = digest.DigestCalcHA1(username, realm, password, nonce)
	    digest_response = digest.DigestCalcResponse(HA1, nonce, method, digest_uri)

	    return digest_response == self["Digest-Response"][0]

	#MS Chap Methods
	
        def checkMSChapPassword(self, password):
	    """
		password: clear text password of user
	    """	
	    mschap_response = mschap.generate_nt_response_mschap(self["MS-CHAP-Challenge"][0],password)
            return mschap_response == self["MS-CHAP-Response"][0][26:]

        def checkMSChap2Password(self, username, password):
	    """
		password: clear text password of user
	    """	
            peer_challenge=self["MS-CHAP2-Response"][0][2:18]
	    mschap2_response = mschap.generate_nt_response_mschap2(self["MS-CHAP-Challenge"][0],peer_challenge,username,password)
            return mschap2_response == self["MS-CHAP2-Response"][0][26:]

        def generateMSChap2AuthenticatorResponse(self,username,password):
	    """
		generate Authenticator response to set as MS-CHAP2-Success value in Access-Accept
	    """
            peer_challenge=self["MS-CHAP2-Response"][0][2:18]
            nt_response=self["MS-CHAP2-Response"][0][26:]
            authenticator_challenge=self["MS-CHAP-Challenge"][0]
            ident=self["MS-CHAP2-Response"][0][0]
            return ident+mschap.generate_authenticator_response(password,nt_response,peer_challenge,authenticator_challenge,username)

        def addMSChapMPPEkeys(self,password,encryption_policy="\x01",encryption_types="\x06"):
            """
                add mppe keys to packet. use for mschap-v1 authentications
                password(string): clear text password
                encryption_policy(string):          1      Encryption-Allowed 2      Encryption-Required
                encryption_types(string):
            """
            lm_hash=mschap.lm_password_hash(password)
            nt_hash=mschap.hash_nt_password_hash(mschap.nt_password_hash(password,False))
            self["MS-CHAP-MPPE-Keys"]=self.PwCrypt(lm_hash[:8]+nt_hash+"\000"*8)
            self["MS-MPPE-Encryption-Policy"]="\000"*3+encryption_policy
            self["MS-MPPE-Encryption-Types"]="\000"*3+encryption_types


        def addMSChap2MPPEkeys(self,password,nt_response,encryption_policy="\x01",encryption_types="\x06"):
            """
                add mppe keys to packet.use for mschap-v2 authentications
                password(string): clear text password
                encryption_policy(string):          1      Encryption-Allowed 2      Encryption-Required
                encryption_types(string):
            """
            (send_key,recv_key)=mppe.mppe_chap2_gen_keys(password,nt_response)
            (send_text,recv_text)=map(mppe.create_plain_text,(send_key,recv_key))
            (send_salt,recv_salt)=mppe.create_salts()
            
            self["MS-MPPE-Send-Key"]=send_salt+\
                                     mppe.radius_encrypt_keys(send_text,self.secret,self.authenticator,send_salt)
            self["MS-MPPE-Recv-Key"]=recv_salt+\
                                     mppe.radius_encrypt_keys(recv_text,self.secret,self.authenticator,recv_salt)

            self["MS-MPPE-Encryption-Policy"]="\000"*3+encryption_policy
            self["MS-MPPE-Encryption-Types"]="\000"*3+encryption_types


	#Chap Methods

        def checkChapPassword(self,password):
                """Check if chap password in packet matched with password
                This method assumes CHAP-Password and CHAP-Challenge are available in attributes.
                It always return false in case they don't exists
                
                XXX TODO: Change this to be able to check authenticator if chap_challeng not available
                
                @param password: clear text password that will be check against packet chap password
                @type password: string

                @return:         true if password correct, else false
                @rtype:          boolean
                """
                try:
                    chap_password=self["CHAP-Password"][0]
                except KeyError:
                    return False

                if self.has_key("CHAP-Challenge"):
                    chap_challenge=self["CHAP-Challenge"][0]
                else:
                    chap_challenge=self.authenticator
                
                hash=md5.new()
                hash.update(chap_password[0])
                hash.update(password)
                hash.update(chap_challenge)
                return hash.digest()==chap_password[1:]
        


	#Pap Methods

        def PwDecrypt(self, password):
                """Unobfuscate a RADIUS password

                RADIUS hides passwords in packets by using an algorithm
                based on the MD5 hash of the pacaket authenticator and RADIUS
                secret. This function reverses the obfuscation process.

                @param password: obfuscated form of password
                @type password:  string
                @return:         plaintext password
                @rtype:          string
                """

                buf=password
                pw=""

                last=self.authenticator
                while buf:
                        hash=md5.new(self.secret+last).digest()
                        for i in range(16):
                                pw+=chr(ord(hash[i]) ^ ord(buf[i]))

                        (last,buf)=(buf[:16], buf[16:])

                while pw.endswith("\x00"):
                        pw=pw[:-1]

                return pw


        def PwCrypt(self, password):
                """Obfuscate password
                
                RADIUS hides passwords in packets by using an algorithm
                based on the MD5 hash of the pacaket authenticator and RADIUS
                secret. If no authenticator has been set before calling PwCrypt
                one is created automatically. Changing the authenticator after
                setting a password that has been encrypted using this function
                will not work.

                @param password: plaintext password
                @type password:  string
                @return:         obfuscated version of the password
                @rtype:          string
                """
                if self.authenticator==None:
                        self.authenticator=self.CreateAuthenticator()

                buf=password
                if len(password)%16!=0:
                        buf+="\x00" * (16-(len(password)%16))

                hash=md5.new(self.secret+self.authenticator).digest()
                result=""

                last=self.authenticator
                while buf:
                        hash=md5.new(self.secret+last).digest()
                        for i in range(16):
                                result+=chr(ord(hash[i]) ^ ord(buf[i]))

                        last=result[-16:]
                        buf=buf[16:]

                return result


class AcctPacket(Packet):
        def __init__(self, code=AccountingRequest, id=None, secret="", authenticator=None, **attributes):
                """Constructor

                @param dict:   RADIUS dictionary
                @type dict:    pyrad.dictionary.Dictionary class
                @param secret: secret needed to communicate with a RADIUS server
                @type secret:  string
                @param id:     packet identifaction number
                @type id:      integer (8 bits)
                @param code:   packet type code
                @type code:    integer (8bits)
                @param packet: raw packet to decode
                @type packet:  string
                """
                Packet.__init__(self, code, id, secret, authenticator, **attributes)
                if attributes.has_key("packet"):
                    self.raw_packet=attributes["packet"]


        def CreateReply(self, **attributes):
                return AcctPacket(AccountingResponse, self.id,
                        self.secret, self.authenticator, **attributes)


        def VerifyAcctRequest(self):
            """Verify request authenticator
               
               @return: 0 if verification failed else 1
               @rtype: intger
            """
            assert(self.raw_packet)
            hash=md5.new(self.raw_packet[0:4] + 16*"\x00" + \
                        self.raw_packet[20:] + self.secret).digest()

            return hash==self.authenticator


        def RequestPacket(self):
                """Create a ready-to-transmit authentication request packet

                Return a RADIUS packet which can be directly transmitted
                to a RADIUS server.
                
                @return: raw packet
                @rtype:  string
                """

                attr=self._PktEncodeAttributes()

                if self.id==None:
                        self.id=self.CreateID()

                header=struct.pack("!BBH", self.code, self.id, (20+len(attr)))
                self.authenticator= md5.new(header[0:4] + 16 * "\x00" + attr
                                            + self.secret).digest()

                return header + self.authenticator + attr


def CreateID():
        """Generate a packet ID.

        @return: packet ID
        @rtype:  8 bit integer
        """
        global CurrentID

        CurrentID=(CurrentID+1)%256
        return CurrentID
