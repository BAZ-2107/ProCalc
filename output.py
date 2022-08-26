def out(st):
    with open("info.txt", "a", encoding="utf-8") as file:
        print(st, file=file)
