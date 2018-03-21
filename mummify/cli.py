import mummify
from fire import Fire

#TODO: remove fire depends? no depends possible?
def cli():
    Fire({
        'switch': mummify.switch,
        'history': mummify.history
    })
