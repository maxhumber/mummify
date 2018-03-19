import mummify
from fire import Fire

def cli():
    Fire({
        'find': mummify.find,
        'rewind': mummify.rewind
    })
