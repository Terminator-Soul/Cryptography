import sys
import os

file_end = {
    ".png": b"\x00\x00\x00\x00\x49\x45\x4e\x44\xae\x42\x60\x82",
    ".jpg": b"\x3f\xff\xd9",
}


def retrieve_secret(filename, file_extension):
    if not file_extension in file_end:
        print("Format not supported!")
    else:
        with open(f"{filename}{file_extension}", "rb") as f:
            buff = bytes(f.read())
            index = buff.index(file_end[file_extension])

            return buff[index + len(file_end[file_extension]) :].decode("utf-8")


def append_secret(filename, file_extension, secret):
    with open(f"{filename}{file_extension}", "ab") as f:
        f.write(bytes(secret, encoding="utf-8"))


def clear_secret(filename, file_extension):

    if not file_extension in file_end:
        print("Format not supported!")
    else:
        buff = ""
        with open(f"{filename}{file_extension}", "rb+") as f:
            buff = bytes(f.read())
            index = buff.index(file_end[file_extension])

            f.truncate(index + len(file_end[file_extension]))


if __name__ == "__main__":
    request = sys.argv[1]
    filename, file_extension = os.path.splitext(sys.argv[2])

    if request == "r":
        secret = retrieve_secret(filename, file_extension)
        print(secret)

    elif request == "a":
        append_secret(filename, file_extension, sys.argv[3])

    elif request == "c":
        clear_secret(filename, file_extension)

    else:
        print("[!] Wrong request, please use 'r' or 'a'")
