import hashlib

file = open("13.jpg","rb")
fileHash = hashlib.sha256(file.read()).hexdigest()
print(fileHash)

