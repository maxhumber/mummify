import mummify
from fire import Fire

def cli():
    Fire({
        'switch': mummify.switch
    })
