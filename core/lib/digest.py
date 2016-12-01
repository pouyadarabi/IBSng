#According to rfc2617, but only implements empty qop
import md5
from core.lib.mschap.utils import str2hex


def DigestCalcA1(username, realm, passwd):
    """
   If the "algorithm" directive's value is "MD5" or is unspecified, then
   A1 is:

      A1       = unq(username-value) ":" unq(realm-value) ":" passwd

   where

      passwd   = < user's password >

    
    """
    return "%s:%s:%s"%(username, realm, passwd)

def DigestCalcHA1(username, realm, password, nonce):
    """
/* calculate H(A1) as per spec */
void DigestCalcHA1(
    IN char * pszAlg,
    IN char * pszUserName,
    IN char * pszRealm,
    IN char * pszPassword,
    IN char * pszNonce,
    IN char * pszCNonce,
    OUT HASHHEX SessionKey
    )
{
      MD5_CTX Md5Ctx;
      HASH HA1;

      MD5Init(&Md5Ctx);
      MD5Update(&Md5Ctx, pszUserName, strlen(pszUserName));
      MD5Update(&Md5Ctx, ":", 1);
      MD5Update(&Md5Ctx, pszRealm, strlen(pszRealm));
      MD5Update(&Md5Ctx, ":", 1);
      MD5Update(&Md5Ctx, pszPassword, strlen(pszPassword));
      MD5Final(HA1, &Md5Ctx);
      if (stricmp(pszAlg, "md5-sess") == 0) {
            MD5Init(&Md5Ctx);
            MD5Update(&Md5Ctx, HA1, HASHLEN);
            MD5Update(&Md5Ctx, ":", 1);
            MD5Update(&Md5Ctx, pszNonce, strlen(pszNonce));
            MD5Update(&Md5Ctx, ":", 1);
            MD5Update(&Md5Ctx, pszCNonce, strlen(pszCNonce));
            MD5Final(HA1, &Md5Ctx);
      };
      CvtHex(HA1, SessionKey);
};

    """
    HA1 = md5.new()

    HA1.update(username)
    HA1.update(":")

    HA1.update(realm)
    HA1.update(":")

    HA1.update(password)

    return str2hex(HA1.digest()).lower()



def DigestCalcResponse(HA1, nonce, method, digest_uri):
    """
/* calculate request-digest/response-digest as per HTTP Digest spec */
void DigestCalcResponse(
    IN HASHHEX HA1,           /* H(A1) */
    IN char * pszNonce,       /* nonce from server */
    IN char * pszNonceCount,  /* 8 hex digits */
    IN char * pszCNonce,      /* client nonce */
    IN char * pszQop,         /* qop-value: "", "auth", "auth-int" */
    IN char * pszMethod,      /* method from the request */
    IN char * pszDigestUri,   /* requested URL */
    IN HASHHEX HEntity,       /* H(entity body) if qop="auth-int" */
    OUT HASHHEX Response      /* request-digest or response-digest */
    )
{
      MD5_CTX Md5Ctx;
      HASH HA2;
      HASH RespHash;
       HASHHEX HA2Hex;

      // calculate H(A2)
      MD5Init(&Md5Ctx);
      MD5Update(&Md5Ctx, pszMethod, strlen(pszMethod));
      MD5Update(&Md5Ctx, ":", 1);
      MD5Update(&Md5Ctx, pszDigestUri, strlen(pszDigestUri));
      if (stricmp(pszQop, "auth-int") == 0) {
            MD5Update(&Md5Ctx, ":", 1);
            MD5Update(&Md5Ctx, HEntity, HASHHEXLEN);
      };
      MD5Final(HA2, &Md5Ctx);
       CvtHex(HA2, HA2Hex);

      // calculate response
      MD5Init(&Md5Ctx);
      MD5Update(&Md5Ctx, HA1, HASHHEXLEN);
      MD5Update(&Md5Ctx, ":", 1);
      MD5Update(&Md5Ctx, pszNonce, strlen(pszNonce));
      MD5Update(&Md5Ctx, ":", 1);
      if (*pszQop) {
          MD5Update(&Md5Ctx, pszNonceCount, strlen(pszNonceCount));
          MD5Update(&Md5Ctx, ":", 1);
          MD5Update(&Md5Ctx, pszCNonce, strlen(pszCNonce));
          MD5Update(&Md5Ctx, ":", 1);
          MD5Update(&Md5Ctx, pszQop, strlen(pszQop));
          MD5Update(&Md5Ctx, ":", 1);
      };
      MD5Update(&Md5Ctx, HA2Hex, HASHHEXLEN);
      MD5Final(RespHash, &Md5Ctx);
      CvtHex(RespHash, Response);
};
    """
    HA2 = md5.new()

    HA2.update(method)
    HA2.update(":")

    HA2.update(digest_uri)

    HA2Hex = str2hex(HA2.digest()).lower()

    RespHash = md5.new()
    RespHash.update(HA1)
    RespHash.update(":")

    RespHash.update(nonce)
    RespHash.update(":")

    RespHash.update(HA2Hex)
    return str2hex(RespHash.digest()).lower()
        