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

    with open("config.json",
              'r') as f:
        json_input = f.read()
    config_file_json = b64 = json.loads(json_input)

    encrypted_file = config_file_json['ENCRYPTED_FILE']
    passwd_file = config_file_json['PASSWD_FILE']
    config_file = config_file_json['CONFIG_FILE']

    print(" ___                              _   _                 _ \n"
          "| _ \__ _ _______ __ _____ _ _ __| | | |   ___  __ __ _| |\n"
          "|  _/ _` (_-<_-< V  V / _ \ '_/ _` | | |__/ _ \/ _/ _` | |\n"
          "|_| \__,_/__/__/\_/\_/\___/_| \__,_| |____\___/\__\__,_|_|\n"
          "	       __  __                                            \n"
          "	      |  \/  |__ _ _ _  __ _ __ _ ___ _ _                \n"
          "	      | |\/| / _` | ' \/ _` / _` / -_) '_|               \n"
          "	      |_|  |_\__,_|_||_\__,_\__, \___|_|                 \n"
          "	                            |___/                        \n"
          "                                                by l4thras\n")

    while True:
        opt = int(input("1 - Decrypt&Encrypt\n2 - Decrypt\n3 - Encrypt\n"
                        "4 - Remove Password File\n5 - Configuration\n"
                        "0 - Exit\n"))

        if opt == 1:
            try:
                with open(encrypted_file, 'r') as f:
                    result = f.read()
                while True:
                    key = getpass(prompt='Password:')
                    confirm_key = getpass(prompt='Confirm Password:')
                    if key == confirm_key:
                        break
                    print("Different Password!")

                plaintext = AESDecryption(result, key)
            except FileNotFoundError:
                with open(encrypted_file, 'w') as f:
                    pass
                plaintext = b"# NEW PASSWORD FILE"
                key = ''

            with open(passwd_file, 'wb') as f:
                 f.write(plaintext)
            print("File Decrypted")

            osCommandString = "notepad.exe " + passwd_file
            os.system(osCommandString)

            with open(passwd_file, 'r') as f:
                text = f.read()

            result = AESEncryption(text, key)

            with open(encrypted_file, 'w') as f:
                f.write(result)
            print("File Encrypted")

            os.remove(passwd_file)
            print("File passwd.txt removed")

            exit()

        elif opt == 2:
            with open(encrypted_file, 'r') as f:
                result = f.read()

            plaintext = AESDecryption(result)

            with open(passwd_file, 'wb') as f:
                 f.write(plaintext)
            print("File Decrypted")

            osCommandString = "notepad.exe " + passwd_file
            os.system(osCommandString)

        elif opt == 3:
            with open(passwd_file, 'r') as f:
                text = f.read()

            result = AESEncryption(text)

            with open(encrypted_file, 'w') as f:
                f.write(result)
            print("File Encrypted")

        elif opt == 4:
            os.remove(passwd_file)
            print("File passwd.txt removed")

        elif opt == 5:
            osCommandString = "notepad.exe " + config_file
            os.system(osCommandString)

        else:
            print("Saliendo...")
            exit()
