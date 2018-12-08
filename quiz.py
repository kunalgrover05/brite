from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABcCVRW6CJJYiaSM4BeSperc_u61jUMqG7wuyhN2QgJ1lAO5kbIKwb6jI72juPgyttR5gdD-wVgxkK9B8guqGi4Dlp8kd97jycG7sOLKiP1zC6quTv6hRjko8Y3BNfyZ9Hsbq-Me6HXMiFu1D4INMN9ZXAv81y2ukoaWiC3hMWyZQ7cyFg='

def main():
    f = Fernet(key)
    print(f.decrypt(message))


if __name__ == "__main__":
    main()

