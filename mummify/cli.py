import mummify
from fire import Fire

def cli():
    Fire({
        'rewind': mummify.rewind
    })
