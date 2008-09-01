# wrapper for rijndael.py. rijndael.py can be found here:
#	http://bitconjurer.org/rijndael.py
# other possible python AES implementations:
#	http://psionicist.online.fr/code/rijndael.py.txt
#	http://jclement.ca/software/pyrijndael/

import blockcipher
from rijndael import rijndael

MODE_ECB = 1
MODE_CBC = 2
MODE_CFB = 3
MODE_OFB = 5
MODE_CTR = 6
MODE_XTS = 7

def new(key,mode=blockcipher.MODE_ECB,IV=None,counter=None):
	return python_AES(key,mode,IV,counter)

class python_AES(blockcipher.BlockCipher):
	"""Wrapper for pure python implementation rijndael.py

	EXAMPLE:
	----------
	>>> import python_AES
	>>> cipher = python_AES.new('0123456789012345')
	>>> cipher.encrypt('0123456789012345')
	'_}\\xf0\\xbf\\x10:\\x8cJ\\xe6\\xfa\\xad\\x99\\x06\\xac;*'
	>>> cipher.decrypt(_)
	'0123456789012345'

	CBC EXAMPLE (plaintext = 3 blocksizes):
	-----------------------------------------
	>>> from binascii import hexlify,unhexlify
	>>> import python_AES
	>>> key = unhexlify('2b7e151628aed2a6abf7158809cf4f3c')
	>>> IV = unhexlify('000102030405060708090a0b0c0d0e0f')
	>>> plaintext1 = unhexlify('6bc1bee22e409f96e93d7e117393172a')
	>>> plaintext2 = unhexlify('ae2d8a571e03ac9c9eb76fac45af8e51')
	>>> plaintext3 = unhexlify('30c81c46a35ce411e5fbc1191a0a52ef')
	>>> cipher = python_AES.new(key,python_AES.MODE_CBC,IV)
	>>> ciphertext = cipher.encrypt(plaintext1 + plaintext2 + plaintext3)
	>>> hexlify(ciphertext)
	'7649abac8119b246cee98e9b12e9197d5086cb9b507219ee95db113a917678b273bed6b8e3c1743b7116e69e22229516'
	>>> decipher = python_AES.new(key,python_AES.MODE_CBC,IV)
	>>> plaintext = decipher.decrypt(ciphertext)
	>>> hexlify(plaintext)
	'6bc1bee22e409f96e93d7e117393172aae2d8a571e03ac9c9eb76fac45af8e5130c81c46a35ce411e5fbc1191a0a52ef'

	OR: supply plaintext as seperate pieces:
	------------------------------------------
	>>> cipher = python_AES.new(key,python_AES.MODE_CBC,IV)
	>>> hexlify( cipher.encrypt(plaintext1 + plaintext2[:-2]) )
	'7649abac8119b246cee98e9b12e9197d'
	>>> hexlify( cipher.encrypt(plaintext2[-2:] + plaintext3) )
	'5086cb9b507219ee95db113a917678b273bed6b8e3c1743b7116e69e22229516'
	>>> decipher = python_AES.new(key,python_AES.MODE_CBC,IV)
	>>> hexlify(decipher.decrypt(ciphertext[:22]))
	'6bc1bee22e409f96e93d7e117393172a'
	>>> hexlify(decipher.decrypt(ciphertext[22:]))
	'ae2d8a571e03ac9c9eb76fac45af8e5130c81c46a35ce411e5fbc1191a0a52ef'

	CTR EXAMPLE:
	------------
	>>> from util import Counter
	>>> key = '2b7e151628aed2a6abf7158809cf4f3c'.decode('hex')
	>>> counter = Counter('f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff'.decode('hex'))
	>>> cipher = python_AES.new(key,python_AES.MODE_CTR,counter=counter)
	>>> plaintext1 = '6bc1bee22e409f96e93d7e117393172a'.decode('hex')
	>>> plaintext2 = 'ae2d8a571e03ac9c9eb76fac45af8e51'.decode('hex')
	>>> plaintext3 = '30c81c46a35ce411e5fbc1191a0a52ef'.decode('hex')
	>>> ciphertext = cipher.encrypt(plaintext1 + plaintext2 + plaintext3)
	>>> ciphertext.encode('hex')
	'874d6191b620e3261bef6864990db6ce9806f66b7970fdff8617187bb9fffdff5ae4df3edbd5d35e5b4f09020db03eab'
	>>> counter2 = Counter('f0f1f2f3f4f5f6f7f8f9fafbfcfdfeff'.decode('hex'))
	>>> decipher = python_AES.new(key,python_AES.MODE_CTR,counter=counter2)
	>>> decipher.decrypt(ciphertext).encode('hex')
	'6bc1bee22e409f96e93d7e117393172aae2d8a571e03ac9c9eb76fac45af8e5130c81c46a35ce411e5fbc1191a0a52ef'

	XTS EXAMPLE:
	cipher/decipher plaintext of 3 blocks, provided as a 2 pieces (31 bytes + 33 bytes)
		NIST SP 800-38A, 2001 ed. - F.5.1 test vector (page 62)
		http://csrc.nist.gov/publications/nistpubs/800-38a/sp800-38a.pdf
	------------
	>>> key = unhexlify('2b7e151628aed2a6abf7158809cf4f3c'*2)
	>>> plaintext1 = unhexlify('6bc1bee22e409f96e93d7e117393172a')
	>>> plaintext2 = unhexlify('ae2d8a571e03ac9c9eb76fac45af8e51')
	>>> plaintext3 = unhexlify('30c81c46a35ce411e5fbc1191a0a52ef')
	>>> cipher = python_AES.new(key,python_AES.MODE_XTS)
	>>> ciphertext = cipher.encrypt(plaintext1 + plaintext2[:15])
	>>> decipher = python_AES.new(key,python_AES.MODE_XTS)
	>>> deciphertext = decipher.decrypt(ciphertext)
	>>> hexlify(deciphertext)
	'6bc1bee22e409f96e93d7e117393172a'
	>>> ciphertext2 = cipher.encrypt(plaintext2[15:]+plaintext3)
	>>> deciphertext2 = decipher.decrypt(ciphertext2)
	>>> hexlify(deciphertext2)
	'ae2d8a571e03ac9c9eb76fac45af8e5130c81c46a35ce411e5fbc1191a0a52ef'
	"""
	def __init__(self,key,mode,IV,counter):
		if mode == MODE_XTS:
			assert len(key) == 32
			self.cipher = rijndael(key[:16], 16)
			self.cipher2 = rijndael(key[16:], 16)
		else:
			self.cipher = rijndael(key, 16)
		self.blocksize = 16
		blockcipher.BlockCipher.__init__(self,key,mode,IV,counter)

def _test():
	import doctest
	doctest.testmod()

if __name__ == "__main__":
	_test()
