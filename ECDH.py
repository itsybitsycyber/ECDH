from Crypto.Cipher import AES
from EC import EllipticCurve
import secp256k1
from random import SystemRandom
import hashlib

class ECDH:
    """
	Implementing ECDH with an elliptic curve over a finite field Fp for prime p > 3.

    A proof of concept implementation of Diffie Hellman key exchange using Elliptic
    Curve Cryptography to generate public and private keys for each user and compute
    a shared secret used by AES-256 to encrypt and decrypt messages.
    Curve used to calculate public and private keys is the secp256k1 curve.
	"""

    def __init__ (self, a, b, p, n_of_points, x, y):
        """
	    Initialises an elliptic curve with given parameters.
        """
        self.ec = EllipticCurve(a, b, p)
        self.n_of_points = n_of_points
        self.P = (int(x,16),int(y,16))

    def generate_private_key(self):
        """
	    Returns a private key found by generating a random number.
        """
        return SystemRandom().getrandbits(256)% self.n_of_points

    def generate_public_key(self, a):
        """
	    Returns a public key found by multiplying the private key with prime P.
        """
        return self.ec.multiply(a,self.P)

    def calculate_secret(self, a, b):
        """
	    Returns the secret found by multiply the private keys with prime P.
        """
        return self.ec.multiply(a*b,self.P)

    def compute_hash(self, message):
        """
	    Returns the digest of the SHA-256 hash function for use as the key in our AES-256 encryption.
        """
        result = hashlib.sha256(message.encode())
        return result.digest()

    def encryption(self, message, secret):
        """
        Returns a ciphertext given a message and a secret. Using symmetric AES-256 and the x-coordinate of the shared secret as a key.
    	"""
        data = message.encode("utf8")
        key = self.compute_hash(secret)
        cipher = AES.new(key,AES.MODE_EAX)
        nonce = cipher.nonce
        ciphertext,tag = cipher.encrypt_and_digest(data)
        return(nonce,ciphertext,tag)

    def decryption(self, ciphertext, secret):
        """
        Returns the original message decrypted by AES-256 using the shared secret as a key.
        The input ciphertext is a tuple consisting of a nonce, ciphertext and a tag.
	    An attacker must solve the ECDLP in they wish to obtain the key.
        """
        key = self.compute_hash(secret)
        cipher = AES.new(key,AES.MODE_EAX, nonce = ciphertext[0])
        plaintext = cipher.decrypt(ciphertext[1])
        return plaintext.decode("utf8")
