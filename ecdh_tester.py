from ECDH import ECDH
import secp256k1


if __name__ == "__main__":


    # init values for sepc256k1 curve
    a = secp256k1.A
    b = secp256k1.B
    p = secp256k1.P
    points = secp256k1.POINTS
    x = secp256k1.X
    y = secp256k1.Y

    # init curve
    ecdh = ECDH(a, b, p, points, x, y)

    # generate public and private keys for sender
    private_key_a = ecdh.generate_private_key()
    A = ecdh.generate_public_key(private_key_a)

    # generate public and private keys for receiver
    private_key_b = ecdh.generate_private_key()
    b = ecdh.generate_public_key(private_key_b)

    # calculate shared secret
    abP = ecdh.calculate_secret(private_key_a, private_key_b)

    # get message input
    print("Enter message to encrypt: \n")
    message =  '\n'.join(iter(input, ""))

    # encrypt message with shared secret and AES
    encrypted = ecdh.encryption(message, str(abP[0]))
    print("Encrypting message with shared secret...")
    print(encrypted[1].hex())

    # decrypt message with shared secret and AES
    decrypted_message = ecdh.decryption(encrypted,str(abP[0]))
    print("Decrypting message with shared secret...")
    print(decrypted_message)
