from authlib.jose import jwt
from authlib.jose import errors as jerr
from time import time
KEY="tokenizer"





class services():
    def __init__(self,conn):
        self.conn=conn
    
    def createToken(self,data):
        header={'alg': 'HS256'}
        payload={'iss':'BLCKWD', 'sub':data, 'iat': int(time()), 'exp':int(time())+14*86400}
        return jwt.encode(header,payload,KEY)

    def isAuth(self,token):
        try:
            claim=jwt.decode(token,KEY)
            claim.validate()
            return claim
        except jerr.BadSignatureError:
            return False
        except jerr.ExpiredTokenError:
            return False


    def canView(self, claim):
        userId=claim.sub
        permissions=self.conn.getPermissionsUser(userId)
        if permissions[0]:
            return True
        return False
    
    def canWrite(self):
        pass

    def canCreate(self):
        pass