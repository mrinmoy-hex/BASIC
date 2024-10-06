import interpreter

while True:
    text = input('basic >>> ')
    result, error = interpreter.run('<stdin>', text)

    if error:
        print(error.__str__())
    else:
         print(result)