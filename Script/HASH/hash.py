import hashlib

file = open("text.txt","rb")
fileHash = hashlib.sha256(file.read()).hexdigest()
print(fileHash)
print(len(fileHash)*4)


