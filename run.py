import os
for file in ['check_string.py', 'DecodeExpression.py', 'decoder.py', 'exceptions.py', 'for_excercise.py', 'main.py', 'objects.py', 'output.py']:
#array = os.chdir(os.path.join("C:\Users\PC\Documents\Pro_calc"))
    a = open(file).read()
    with open(file, "w") as x:
        print(a.replace("\t", "    "), file=x)