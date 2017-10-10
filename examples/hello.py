#!/usr/bin/python
import os
import sys
from papirus import Papirus

def main():
    papirus = Papirus()
    print("Clearing Papirus ...")
    papirus.clear()
    print("Finished!")

if __name__ == '__main__':
    main()
