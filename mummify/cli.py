import mummify
import argparse
from pathlib import Path

def cli():
    parser = argparse.ArgumentParser()
    parser.add_argument('function', choices=('history', 'switch'))
    parser.add_argument('id', nargs='?')
    args = parser.parse_args()
    if args.function == 'history':
        if not Path('.mummify').is_dir():
            print('mummify not initialized')
            return
        print(mummify.history())
    elif args.function == 'switch' and args.id is not None:
        if not Path('.mummify').is_dir():
            print('mummify not initialized')
            return
        mummify.switch(args.id)
    else:
        print('mummify id required')

if __name__ == '__main__':
    cli()
