import argparse
from pathlib import Path
import subprocess
import mummify
from .main import colour


def cli():
    """The command line interface for mummify

    Commands:

    - mummify history
    - mummify switch
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("function", choices=("history", "switch"))
    parser.add_argument("id", nargs="?")
    args = parser.parse_args()
    if not Path(".mummify").is_dir():
        return "mummify not enabled"
    if args.function == "history":
        return mummify.history()
    if args.function == "switch" and args.id is not None:
        mummify.switch(args.id)
    else:
        return colour('mummify id required')


if __name__ == "__main__":
    cli()
