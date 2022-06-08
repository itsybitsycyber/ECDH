import math


class EllipticCurve:
	"""
	Implemention of an elliptic curve over a finite field Fp for prime p > 3.

	E:	y^2 = x^3 + ax + b,
	where a,b in Field p and the discriminant -16(4a^3 + 27b^2) is non-zero

	"""

	def __init__ (self,a,b,p):
		"""
		Initialises curve with given parameters
		"""
		self.a = a
		self.b = b
		self.p = p
		self.points = []


	def define_points(self):
		"""
		Difines the points of the curve
		"""
		self.points.append(secp256k1.INF_POINT)
		for x in range(self.p):
			for y in range(self.p):
				if self.equal_mod_p(y*y, x** 3 + self.a*x + self.b):
					self.points.append((x,y))

	def total_points(self):
		"""
		Returns the number of points on the curve
		"""
		return len(self.points)

	def discriminant(self):
		"""
		Returns the discriminant of the curve
		"""
		discriminant = -16*(4*(self.a ** 3) + 27 * self.b * self.b)
		return self.reduce_mod_p(discriminant)

	def valid_discriminant(self):
		"""
		Returns true of the discriminant is non zero
		"""
		return self.discriminant() != 0

	def reduce_mod_p(self, x):
		return x % self.p

	def equal_mod_p(self, x, y):
		return self.reduce_mod_p(x-y) == 0

	def extended_gcd(self,a, b):
		"""
		Implementation of the Extended Euclidean Algorithm
		"""
		if a == 0:
			return b, 0, 1
		else:
			gcd, x, y = self.extended_gcd(b % a, a)
			return gcd, y - (b // a) * x, x

	def inverse_mod_p(self,x):
		"""
		Returns the modular inverse
		"""
	    if x == 0:
	        raise ZeroDivisionError('division by zero')

	    if x < 0:
	        return self.p - self.inverse_mod_p(-x)

	    gcd, k, y = self.extended_gcd(self.p, x)


	    return k % self.p

	def addition(self, P1, P2):
		"""
		Calculates the sum of two points on the curve and returns the new point
		"""

		if P1 == secp256k1.INF_POINT:
			return P2
		if P2 == secp256k1.INF_POINT:
			return P1


		a = self.a
		p = self.p
		x1 = P1[0]
		y1 = P1[1]
		x2 = P2[0]
		y2 = P2[1]

		if self.equal_mod_p(x1,x2) and self.equal_mod_p(y1,-y2):
			s = 0
		if (x1==x2):
			s = ((3*(x1**2) + a) * self.inverse_mod_p(2*y1))%p
		else:
			s = ((y2-y1) * self.inverse_mod_p(x2-x1))%p
		x3 = (s**2 - x1 - x2)%p
		y3 = (s*(x1 - x3) - y1)%p
		return (x3, y3)

	def associativity(self):
		"""
		Checks if associativity holds among addition of points on the curve
		"""
		n = len(self.points)
		for i in range (n):
			for j in range(n):
				for k in range(n):
					P = self.addition(self.points[i], self.addition(self.points[j], self.points[k]))
					Q = self.addition(self.addition(self.points[i], self.points[j]), self.points[k])
					if P != Q:
						return False
		return True

	def multiply(self, n, P):
		"""
		Implements double-and-add-method for modular multiplication
		"""
		Q = secp256k1.INF_POINT
		binary_n = tobinary(n)
		for x in binary_n:
			if x == 1:
				Q = self.addition(P,Q)
			P = self.addition(P,P)
		return Q


def tobinary(n):
	"""
	Returns binary representation of decimal number
	"""
	while(n>=0):
		i = 0
		if n==0:
			return n
		binary_digits = []
		r = int(math.log(n,2))
		for l in range(0,r+1):
			if n % 2 == 1:
				binary_digits.append(1)
				n=int(n/2)
			else:
				binary_digits.append(0)
				n=int(n/2)
		return binary_digits


def isprime(num):
	"""
	Determines if given input number is prime
	"""
	flag = False
	if num > 1:
	    for i in range(2, num):
	        if (num % i) == 0:
	            flag = True
	            break

	if flag:
	    return False
	else:
	    return True
