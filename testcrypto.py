from cryptography.fernet import Fernet
import pickle

# with open('crypto_pass.bin', 'wb') as file_object:  #Save key in file
#     pickle.dump(key,file_object)
with open ('crypto_pass.bin', 'rb') as fp:
    key = pickle.load(fp)
    print(key)

crypto_suite = Fernet(key)
#Save from credentials file to encrypted in bin file with pickle
# file5 = open('Credentials', 'r') 
# Lines = file5.readlines() 
# crypt_text = [crypto_suite.encrypt(text.encode('utf-8')) for text in Lines]
# print(crypt_text)
# with open('credentials.bin', 'wb') as file_object:  
#     pickle.dump(crypt_text,file_object)

with open ('credentials.bin', 'rb') as fp:
    credentials = pickle.load(fp)
    print([crypto_suite.decrypt(crendential).decode('utf-8').strip() for crendential in credentials])