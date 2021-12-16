import hashlib

def hash_of_object(bytes_of_object):
    return hashlib.sha256(bytes_of_object.encode()).hexdigest()
