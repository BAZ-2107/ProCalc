class B:
    pass

class A:
    def update(self):
        self = B()

w = A()
w.update()
print(type(w).__name__)