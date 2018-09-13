def decorator_demo(old_function):
    def new_function(a, b):
        print("input", a, b)
        return old_function(a, b)
    return new_function


@decorator_demo
def square_sum(a, b):
    return a**2 + b**2


@decorator_demo
def square_diff(a, b):
    return a**2 - b**2

if __name__ == "__main__":
    print(square_sum(3, 4))
    print(square_diff(3, 4))
