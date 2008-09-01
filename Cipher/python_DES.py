import blockcipher
import pyDes

MODE_ECB = 1
MODE_CBC = 2
MODE_CFB = 3
MODE_OFB = 5
MODE_CTR = 6

def new(key,mode=blockcipher.MODE_ECB,IV=None,counter=None):
	return python_DES(key,mode,IV,counter)

class python_DES(blockcipher.BlockCipher):
	"""wrapper for pure python implementation pyDes.py
	
	EXAMPLE (test vectors from NESSIE):
	>>> import python_DES	
	>>> from binascii import hexlify, unhexlify
	>>> cipher = python_DES.new(unhexlify('7CA110454A1A6E57'))
	>>> ciphertext = cipher.encrypt(unhexlify('01A1D6D039776742'))
	>>> hexlify(ciphertext)
	'690f5b0d9a26939b'
	>>> plaintext = cipher.decrypt(ciphertext)
	>>> hexlify(plaintext)
	'01a1d6d039776742'
	"""
	def __init__(self,key,mode,IV,counter):
		self.cipher = pyDes.des(key)
		self.blocksize = self.cipher.block_size
		blockcipher.BlockCipher.__init__(self,key,mode,IV,counter)

def _test():
	import doctest
	doctest.testmod()

if __name__ == "__main__":
	_test()
