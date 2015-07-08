#!/usr/bin/python
from PIL import Image
from Crypto.Cipher import AES
from Crypto import Random
import getopt
import sys
import time


def gen_images(f):
    im = Image.open(f)
    pixels = list(im.getdata())
    p = bytearray(pixels)
    IV=Random.new().read(16)

    ebc_encryptor = AES.new("This is a key123", AES.MODE_ECB)
    cbc_encryptor = AES.new("This is a key123", AES.MODE_CBC, IV)
    cfb_encryptor = AES.new("This is a key123", AES.MODE_CFB, IV)

    encryptors = {"ebc": ebc_encryptor, "cbc": cbc_encryptor, "cfb": cfb_encryptor}

    for e in encryptors.keys():
        start = time.time()
        encryptor = encryptors[e]
        c = encryptor.encrypt(str(p))
        end = time.time()
        c_pixels = bytearray(c)
        c_pixels = list(c_pixels)
        im.putdata(c_pixels)
        print "Encrypted using %s in %s seconds" % (e, end-start)
        im.save("%s-%s" % (e, f))

def usage():
    print "image_encryptor.py"
    print "Encrypts the contents of a BMP using EBC, CBC, and CFB"
    print "Written by Scott Pack"
    print "Usage: ./image_encryptor.py -i <filename>"
        
def main():
    f = ""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "i:", ["help", "output="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        usage()
        sys.exit(2)
    output = None
    verbose = False
    for o, a in opts:
        if o == "-i":
            f = a

    if f is "":
        usage()
        exit()
    gen_images(f)


main()
