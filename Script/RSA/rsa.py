'''
    Author: Team 7 - Crypto asignature (ESCOM - IPN)
    This is an implementation using cryptodome library for digital signatures with RSA
'''
import os, base64, binascii
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256
from Crypto.Signature.pkcs1_15 import PKCS115_SigScheme
from Crypto.Cipher import PKCS1_OAEP

class RSA_sign:
    '''
    A class used for signing files, generate keys from RSA and verify signing files

    Attributes
    ----------
    private_key : RSA
        The keys from RSA cipher, includes private and public keys
    public_key : RSA.public_key
        The public key from RSA cipher
    ext : str
        Extension for output keyfiles
    separator : str
        Our separator, this is used when a output file signed we can separate the signature from data.
        This will be use for verify documents

    Methods
    -------
    generate_key(key_size, file_name)
        This function is used to generate a key pair for RSA cipher.
    read_private_key(file_name)
        This function is used for read private key from a file.
    read_public_key(file_name)
        This function is used for read public key from a file.
    signing_data(data, file_name)
        This function generates a output file signed with the data provide.
        The output file have an extention '.txt'.
        The hash is generate by base64.
    signing_data(data, file_name, ext)
        This function generates a output file signed with the data provide.
        The output file have an extention provide in the variable 'ext'.
        The hash is generate by base64.
    verify_signature(signature, ignore)
        This function verify data of a signature, and the output will be if a signed file is valid.
    '''
    private_key = None
    public_key = None
    ext = '.key'
    separator = '\n\n\\'
    
    def __init__(self):
        print('Initialize')
        
    def generate_key(self, key_size, file_name):
        '''
        This function is used to generate a key pair for RSA cipher.
        Note: The filename can be a username.
        TODO: store in base64 ?

        Parameters
        ----------
        key_size : int
            Key size for RSA. This can have value of 1024, 2048 or 3072
        file_name : str
            Output file name for keys
        '''
        self.private_key = RSA.generate(key_size)

        # Private key
        file = open(file_name + self.ext, 'wb')
        file.write(self.private_key.export_key())
        file.close()
        
        # Public key
        self.public_key = self.private_key.publickey()
        file = open('public_' + file_name + self.ext, 'wb')
        file.write(self.public_key.export_key())
        file.close()

    def read_private_key(self, file_name):
        '''
        This function is used for read private key from a file.

        Parameters
        ----------
        file_name : str
            File name to read
        '''
        file = open(file_name + self.ext, 'r')
        self.private_key = RSA.import_key(file.read())
        file.close()

    def read_public_key(self, file_name):
        '''
        This function is used for read public key from a file.

        Parameters
        ----------
        file_name : str
            File name to read
        '''
        file = open('public_' + file_name + self.ext, 'r')
        self.public_key = RSA.import_key(file.read())
        file.close()

    def signing_data(self, data, file_name):
        '''
        This function generates a output file signed with the data provide.
        The output file have an extention '.txt'.
        Verify with private key.
        Note: Image bytes need to send in base64.

        Parameters
        ----------
        data : bytes array
            Data that will be sign
        file_name : str
            File name to read
        '''
        self.signing_data(data, file_name, ".txt")
        
    def signing_data(self, data, file_name, ext):
        '''
        This function generates a output file signed with the data provide.
        The output file have an extention provide in the variable 'ext'.
        Verify with private key. The hash is generate by base64.

        Parameters
        ----------
        data : bytes array
            Data that will be sign
        file_name : str
            File name to read
        ext : str
            Extension for output file
        '''
        data = base64.encodebytes(data)
        
        data_hash = SHA256.new()
        data_hash.update(data)
        
        signer = PKCS115_SigScheme(self.private_key)
        signature = signer.sign(data_hash)
        
        signed_file = open('contract_' + file_name + ext, "wb")
        signed_file.write(base64.decodebytes(data))
        signed_file.write(self.separator.encode('utf-8'))
        
        signed_file.write(binascii.hexlify(signature))
        signed_file.close()

    def verify_signature(self, signature, ignore = 0):
        '''
        This function verify data of a signature, and the output will be if a signed file is valid.
        Verify with public key. The hash is generate by base64.

        Parameters
        ----------
        signature : str
            Data from signature file
        ignore : int
            Variable for ignore some digital signatures from the final of signature.
            This is used for many signatures.
            Default value is 0.

        Returns
        -------
        bool
            File signature is valid
        '''
        parts = signature.split(bytes(self.separator, 'utf-8'))

        data = b''
        # In case that found more separator
        # Always the last part will be the sign or signs, others parts will be data from the file
        for i in range(len(parts) - 1 - ignore):
            data += parts[i]
            if(i != len(parts) - 2 - ignore):
                data += bytes(self.separator, 'utf-8')
        data = base64.encodebytes(data)
        sign = parts[len(parts) - 1 - ignore]
        sign = binascii.unhexlify(sign)

        # We need the hash of data file for sign a file
        data_hash = SHA256.new()
        data_hash.update(data)
        
        verification = PKCS115_SigScheme(self.public_key)
        try:
            verification.verify(data_hash, sign)
            print('Success')
            return True
        except (ValueError, TypeError) as exception:
            print('Invalid')
            return False

    '''
        Functions for this project (Digital art)
        Just when the contact did signature for the three actors
    '''
    def verify_signature_artist(self, signature):
        self.verify_signature(signature, 2)

    def verify_signature_client(self, signature):
        self.verify_signature(signature, 1)

    def verify_signature_notary(self, signature):
        self.verify_signature(signature, 0)

'''
    TEST
'''
# ext = '.jpg'

# print('Generate keys')
# rsa = RSA_sign()
# rsa.generate_key(2048, 'my_key')

# print('Read keys')
# rsa.read_private_key('my_key')
# rsa.read_public_key('my_key')

# print('Read text')
# img = open('test2.jpg', 'rb') # read bytes
# img_bytes = img.read()

# print('Firmando')
# rsa.signing_data(img_bytes, 'myContract', ext)

# print('Verificando 1 - Firma del artista cuando nadie ha firmado')
# signed_file_aux = open('contract_' + 'myContract' + ext, "rb") # Name of the sign document
# signed = signed_file_aux.read()
# rsa.verify_signature(signed)
# img.close()
# signed_file_aux.close()




# # Second Person
# print('\nSecond Person')
# rsa2 = RSA_sign()
# rsa2.generate_key(2048, 'my_key2')

# print('Read keys 2')
# rsa2.read_private_key('my_key2')
# rsa2.read_public_key('my_key2')

# print('Read text 2')
# img = open('contract_' + 'myContract' + ext, 'rb') # read bytes
# img_bytes = img.read()

# print('Firmando 2')
# rsa2.signing_data(img_bytes, 'myContract_2', ext)

# print('Verificando 2 - Firma del cliente (cuando ya firmo el artista)')
# signed_file_aux = open('contract_' + 'myContract_2' + ext, 'rb')
# rsa2.verify_signature(signed_file_aux.read())

# signed_file_aux.close()
# img.close()

# print('\nVerificando 3 - Firma del artista (cuando ya firmo el cliente)')
# signed_file_aux = open('contract_' + 'myContract_2' + ext, 'rb') # Name of the sign document
# signed = signed_file_aux.read()

# rsa.verify_signature(signed, 1)

# signed_file_aux.close()
