n = 8
txt = open('text.txt', 'r')

def getBits(bits,n):
    flag = False
    incomplete = ""
    for e in str(bits):
        if flag:
            incomplete += e
        if e=="b":
            flag = True
    complete = "0"*(int(n/2)-len(incomplete))+incomplete
    return complete

xor = 0
for e in txt.readline():
    xor = xor^ord(e)

nl = bin(xor%10)
nh = bin(int(xor/10))
block = getBits(nh,n)+getBits(nl,n)

decimal_representation = int(block, 2)
hexadecimal_string = hex(decimal_representation)
print(hexadecimal_string)