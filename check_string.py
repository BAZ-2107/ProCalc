from exceptions import CheckStringError

def check_string(st):
    if not st:
        raise CheckStringError("Входная строка не должна быть пустой")
    symbols = open("txt/symbols.txt", encoding="utf-8").read()
    for ch in st:
        if ch not in symbols:
            raise CheckStringError(f"Найден неизвестный символ: <{ch}>")

