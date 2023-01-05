import sys

from pypsd.reader import read_psd


def main():
    if len(sys.argv) != 2:
        print("Expected arguments: file.psd")
        return

    read_psd(sys.argv[1])


if __name__ == "__main__":
    main()
