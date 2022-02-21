import tkinter as tk
from PIL import ImageTk, Image
import constants as c
from Crypto.Cipher import AES
from base64 import b64encode, b64decode
from getpass import getpass
import json
import os
import sys

class MasterWindow(tk.Tk):
    def __init__(self,master=None):
        tk.Tk.__init__(self,master)
        self.geometry("300x400")
        self.resizable(width=False, height=False)
        self.title("PasswordLocalManager")
        self.iconbitmap(c.LOCK_ICO)
        #Creates a Tkinter-compatible photo image, which can
        #be used everywhere Tkinter expects an image object.
        img = ImageTk.PhotoImage(Image.open('lock.png'))
        #The Label widget is a standard Tkinter widget ç
        #used to display a text or image on the screen.
        etiqueta1 = tk.Label(image=img)
        #The Pack geometry manager packs widgets in rows or columns.
        etiqueta1.pack()



def AESEncryption(data, key = ''):
    if key == '':
        key = input('Introduce password: ')
    key = key.encode('UTF-8')
    #Here ask for password by gui
    header = b"header"
    data = data.encode('UTF-8')
    cipher = AES.new(key, AES.MODE_EAX)
    cipher.update(header)
    ciphertext, tag = cipher.encrypt_and_digest(data)

    json_k = [ 'nonce', 'header', 'ciphertext', 'tag' ]
    json_v = [ b64encode(x).decode('utf-8') for x in (cipher.nonce, header,
              ciphertext, tag) ]
    result = json.dumps(dict(zip(json_k, json_v)))
    return result

def AESDecryption(json_input, key = ''):
    try:
        if key == '':
            key = input('Introduce password: ')
        key = key.encode('UTF-8')
        b64 = json.loads(json_input)
        json_k = [ 'nonce', 'header', 'ciphertext', 'tag' ]
        jv = {k:b64decode(b64[k]) for k in json_k}

        cipher = AES.new(key, AES.MODE_EAX, nonce=jv['nonce'])
        cipher.update(jv['header'])
        plaintext = cipher.decrypt_and_verify(jv['ciphertext'], jv['tag'])
        return plaintext
    except (ValueError, KeyError):
        print("Incorrect decryption")



if __name__ == '__main__':
    # Win = MasterWindow()
    # Win.mainloop()

    while True:

        opt = int(input("1 - Decrypt&Encrypt\n2 - Decrypt\n3 - Encrypt\n"
                        "4 - Remove Password File\n0 - Exit\n"))

        if opt == 1:
            passwd = r'C:\Users\Jon\github\PasswordLocalManager\passwd.txt'
            encryp = r'C:\Users\Jon\github\PasswordLocalManager\encrypted.json'
            with open(encryp, 'r') as f:
                result = f.read()

            while True:
                key = getpass(prompt='Password:')
                confirm_key = getpass(prompt='Confirm Password:')
                if key == confirm_key:
                    break
                print("Different Password!")
            plaintext = AESDecryption(result, key)

            with open(passwd, 'wb') as f:
                 f.write(plaintext)
            print("File Decrypted")

            osCommandString = "notepad.exe " + passwd

            os.system(osCommandString)

            with open(passwd, 'r') as f:
                text = f.read()

            result = AESEncryption(text, key)

            with open(encryp, 'w') as f:
                f.write(result)
            print("File Encrypted")

            os.remove(passwd)
            print("File passwd.txt removed")

            exit()

        elif opt == 2:
            with open(r'C:\Users\Jon\github\PasswordLocalManager\encrypted.json'
                      ,'r') as f:
                result = f.read()

            plaintext = AESDecryption(result)

            with open(r'C:\Users\Jon\github\PasswordLocalManager\passwd.txt',
                      'wb') as f:
                 f.write(plaintext)
            print("File Decrypted")

            osCommandString = "notepad.exe passwd.txt"
            os.system(osCommandString)



        elif opt == 3:
            with open(r'C:\Users\Jon\github\PasswordLocalManager\passwd.txt',
                      'r') as f:
                text = f.read()

            result = AESEncryption(text)

            with open(r'C:\Users\Jon\github\PasswordLocalManager\encrypted.json'
                      ,'w') as f:
                f.write(result)
            print("File Encrypted")

        elif opt == 4:
            os.remove(r'C:\Users\Jon\github\PasswordLocalManager\passwd.txt')
            print("File passwd.txt removed")

        else:
            print("Saliendo...")
            exit()