from src.domain.util import crypto_helper, data_generator

class BaseService():
    
    @property
    def crypto(self):
        return crypto_helper.CryptoHelper()

    @property
    def data_generator(self):
        return data_generator.DataGenerator()
