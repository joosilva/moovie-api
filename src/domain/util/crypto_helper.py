import bcrypt

FRASE_SEGURANCA = "python is a great lenguage"

class CryptoHelper():
    
    @staticmethod
    def criptografar(str: str) -> str:
        str_criptografada = (str + FRASE_SEGURANCA).encode("utf-8")
        
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(str_criptografada, salt).decode("utf-8")
        
        return hash
    
    
    @staticmethod
    def equals(str: str, hash: str) -> bool:
        str = (str + FRASE_SEGURANCA).encode("utf-8")
        
        hash = hash.encode("utf-8")
    
        return bcrypt.checkpw(str, hash)
    