from exceptions import UncorrectStringError, UnknownSymbolError

def check_string(st):
    if not st:
        raise UncorrectStringError
    symbols = open("symbols.txt").read()
    for ch in st:
        if ch not in symbols:
            raise UnknownSymbolError(ch)

