import crypt
import random
import re
import types
import random

def getPasswords(_count,_type,_len):
    """
        generate _count password of _type, and return a list of Password instances
        _type(integer): password contains 1: alphabets only, 2: digits only, 3:alphabets + digits
    """
    if _type==1:
        chars="abcdefghijklmnopqrstuvwxyz"
    elif _type==2:
        chars="123456789"
    else:
        chars="abcdefghijkmnpqrstuvwxyz23456789" #don't include 1&l , 0&o they are hard to distinguish
    
    return map(lambda x:Password(generateRandomPassword(chars,_len)),range(_count))
    
def generateRandomPassword(chars,_len):
    """
        generate a random password from characters in "chars" and length of "_len"
    """
    return "".join(map(lambda x:chars[random.randint(0,len(chars)-1)],range(_len)))
    

class Password:
    pass_chars_match=re.compile("[^A-Za-z0-9_\-]")
    def __init__(self,password):
        self.password=password

    def __eq__(self,password_obj):
        if type(password_obj)==types.StringType:
            password_obj=Password(password_obj)

        if self.isMd5Hash():
            enc_pass=self.getMd5Crypt()
            return enc_pass==password_obj.getMd5Crypt(enc_pass)
        elif password_obj.isMd5Hash():
            enc_pass=password_obj.getMd5Crypt()
            return enc_pass==self.getMd5Crypt(enc_pass)
        else:
            return self.getPassword()==password_obj.getPassword()

    def checkPasswordChars(self):
        """
            Check Password characters
            return "1" if it's OK and "0" if it's not
        """
        if not len(self.password):
            return 0
        if self.pass_chars_match.search(self.password) != None:
            return 0
        return 1

    def getMd5Crypt(self,salt=None): 
        """
            md5crypt "self.password" with "salt", 
            If "salt" is None,a new salt will be randomly generated and used
            If "text" is already md5crypted, return it, else return crypted pass
        """
        if self.isMd5Hash():
            return self.password
        else:
            return self.__md5Crypt(salt)
        
    def getPassword(self):
        return self.password

    def __md5Crypt(self,salt):
        if salt==None:
            salt=self.__generateRandomSalt()
        return crypt.crypt(self.password,salt)


    def __generateRandomSalt(self):
        salt='$1$'
        for i in range(8):
            rand=random.randint(0,61)
            if rand<10:
                salt+=str(rand)
            elif rand<36:
                salt+=chr(rand-10+65)
            else:
                salt+=chr(rand-36+97)
        salt += '$'
        return salt

    def isMd5Hash(self):
        if self.password[0:3]=='$1$':
            return 1
        return 0