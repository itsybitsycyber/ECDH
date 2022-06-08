"""
Parameters defined for  the secp256k1 curve.
A curve is of the form

    y^2 = x^3+ax+b where mod(p)

where a is represented by A, b is represented by B,
p is represented by P (modulo for the curve)
POINTS is the group order for the curve
X and Y are the x and y co-ordinates of the generator point G
given in hexadecimal

"""
A = 0
B = 7
P = 115792089237316195423570985008687907853269984665640564039457584007908834671663
POINTS = 115792089237316195423570985008687907852837564279074904382605163141518161494337
X = "979BE667EF9DCBBAC55A06295CE870B07029BFCDB2DCE28D959F2815B16F81798"
Y = "483ADA7726A3C4655DA4FBFC0E1108A8FD17B448A68554199C47D08FFB10D4B8"
INF_POINT = None
