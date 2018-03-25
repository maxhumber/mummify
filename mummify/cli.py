import mummify
import argparse

def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('function', choices=('history', 'switch'))
    parser.add_argument('id', nargs='?')
    args = parser.parse_args()
    if args.function == 'history':
        print(mummify.history())
    elif args.function == 'switch' and args.id is not None:
        mummify.switch(args.id)
    else:
        print('mummify id required')

if __name__ == '__main__':
    cli()
