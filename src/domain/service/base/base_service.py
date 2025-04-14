from src.domain.util import crypto_helper

class BaseService():
    
    @property
    def crypto(self):
        return crypto_helper.CryptoHelper()
