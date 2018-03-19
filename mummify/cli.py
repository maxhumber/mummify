import mummify
from fire import Fire

def find(identifier):
    mummify.find(identifier)

def main():
    Fire({'find': find})

if __name__ == '__main__':
    main()
