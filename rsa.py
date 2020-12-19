import random
def gcd(a, b):
    while b!=0:
        a, b = b, a%b
    return a

def decrypt(pk, ciphertext):
    #Unpack the key into its components
    key, n = pk
    #Generate the plaintext based on the ciphertext and key using a^b mod m
    plain = [chr(((int(char,16) ** key) % n)) for char in ciphertext]
    #Return the array of bytes as a string
    return ''.join(plain)

#암호화 시도
def encrypt(pk, plaintext):
    #Unpack the key into it's components
    key, n = pk
    #Convert each letter in the plaintext to numbers based on the character using a^b mod m
    cipher = [hex(ord(char) ** key % n)[2:]  for char in plaintext]
    #Return the array of bytes
    return cipher

def get_private_key(e, tot):
    k=1
    while (e*k)%tot != 1 or k == e:
        k+=1
    return k

def get_public_key(tot):
    e=2
    while e<tot and gcd(e, tot)!=1:
        e += 1
    return e

def getS():
    out = []
    chk = True
    for i in range(2,30):
        chk = True
        for j in range(2,i):
            if i%j == 0:
                chk = False
        if chk:
            out.append(i)
    return out
def getRsa():
    decimals = getS()
    p = random.choice(decimals)
    q = random.choice(decimals)
    while p == q: # 소수 선별
        q = random.choice(decimals)
    n = p*q # n 구하기
    totient = (p-1)*(q-1)               # L
    e = get_public_key(totient)         #E  #공개키
    d = get_private_key(e, totient)     #D  #개인키
        
    return n,e,d#n / 공개키 / 개인키
'''
# Input message to be encrypted
m = input("Enter the text to be encrypted:")

# Step 1. Choose two prime numbers
p = 13
q = 23

print("Two prime numbers(p and q) are:", str(p), "and", str(q))

# Step 2. Compute n = pq which is the modulus of both the keys
n = p*q #299     N 구하기
print("n(p*q)=", str(p), "*", str(q), "=", str(n))

# Step 3. Calculate totient
totient = (p-1)*(q-1)   #264    #L 구하기
print("(p-1)*(q-1)=", str(totient))
    
# Step 4. Find public key e
e = get_public_key(totient) #299 / 5    #E
print("Public key(n, e):("+str(n)+","+str(e)+")")

# Step 5. Find private key d
d = get_private_key(e, totient) # 299 / 53  #D
print("Private key(n, d):("+str(n)+","+str(d)+")")

# Step 6.Encrypt message
encrypted_msg = encrypt((e,n), m)
print('Encrypted Message:', ''.join(map(lambda x: str(x), encrypted_msg)))

print(encrypted_msg)
# Step 7.Decrypt message
print('Decrypted Message:', decrypt((d,n),encrypted_msg))
'''
