from pyscript import sync, when

@when("mouseup", "span")
def up(event):
    sync.stop = (lambda: 1)
    print("END")