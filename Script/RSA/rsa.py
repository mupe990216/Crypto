import os, base64, binascii
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Cipher import PKCS1_OAEP

class RSA_sign:
    '''

    '''
    private_key = None;
    public_key = None;
    ext = '.key'
    separator = '\n\n'
    
    def __init__(self):
        print('initialize');
    '''
        file_name can be username
        TODO: store in base64?
    '''
    def generate_key(self, key_size, file_name):
        '''Generate: 1024 or 2048 or 3072'''
        self.private_key = RSA.generate(key_size)

        '''private'''
        file = open(file_name + self.ext, 'wb')
        file.write(self.private_key.export_key())
        file.close()
        
        '''public'''
        self.public_key = self.private_key.publickey()
        file = open('public_' + file_name + self.ext, 'wb')
        file.write(self.public_key.export_key())
        file.close()

    def read_private_key(self, file_name):
        file = open(file_name + self.ext, 'r');
        self.private_key = RSA.import_key(file.read())

    def read_public_key(self, file_name):
        file = open('public_' + file_name + self.ext, 'r');
        self.public_key = RSA.import_key(file.read())

    '''
        Signing data with private key
    '''
    def signing_data(self, data, file_name):
        data_hash = SHA256.new()
        data_hash.update(data)
        
        signer = PKCS115_SigScheme(self.private_key)
        signature = signer.sign(data_hash)
        
        signed_file = open('contract_' + file_name + ".txt", "wb")
        signed_file.write(data)
        signed_file.write(self.separator.encode('utf-8'))
        
        signed_file.write(binascii.hexlify(signature))
        signed_file.close()

    '''
        Verify with public key
    '''
    def verify_signature(self, signature):
        parts = signature.split(self.separator)

        data = ""
        # In case that found more separator
        # Always the last part will be the sign, others will be data
        for i in range(len(parts) - 1):
            data += parts[i]
        sign = parts[len(parts)-1]

        sign = binascii.unhexlify(sign)        data_hash = SHA256.new(data.encode('utf-8'))
        verification = PKCS115_SigScheme(self.public_key)
        try:
            verification.verify(data_hash, sign)
            print('Success')
        except (ValueError, TypeError) as exception:
            print('Invalid')

'''
    TEST
'''

print('Generate keys');
rsa = RSA_sign()
rsa.generate_key(2048, 'my_key')

print('Read keys')
rsa.read_private_key('my_key')
rsa.read_public_key('my_key')

print('Read text')
txt = open('test.txt', 'rb') # read bytes
txt_bytes = txt.read()

print('Firmando')
rsa.signing_data(txt_bytes, 'myContract')

print('Verificando');
signed_file_aux = open('contract_' + 'myContract' + ".txt") # Name of the sign document

rsa.verify_signature(signed_file_aux.read())

txt.close()
signed_file_aux.close()

# Second Person
'''  
rsa2 = RSA_sign()
rsa2.generate_key(2048, 'my_key2')
print('Firmando 2')
rsa2.signing_data(b'Hello World', 'myContract_2')

print('Verificando');
signed_file_aux = open('contract_' + 'myContract' + ".sign")
rsa.verify_signature(b'Hello World', signed_file_aux.read())
'''
