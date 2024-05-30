import numpy
from pyweb import pydom
from pyscript import when, PyWorker

LAWNGREEN = (124, 252, 0)
BROWN = (193, 154, 107)

class Game:
    def __init__(self):
        self.time = 1
        self.start, self.week_line, self.leftover_line = pydom["p#output"], pydom["p#week"], pydom["p#leftover"]
        self.start.html = "Play"
        self.week, self.leftover = 0, 0
        self.grid, self.lifespans = numpy.array([]), numpy.array([[7 for _ in range(20)] for _ in range(20)])
        self.make_board()
        self.rate = 80000
        self.reset()

    def reset(self):
        self.week += 1
        self.leftover = 256
        self.week_line.html = f"Week {self.week}"
        self.leftover_line.html = f"{self.leftover} gallons remaining"

        self.lifespans -= 1

        for row in range(20):
            for column in range(20):
                self.change_color(row, column)

    def make_board(self):
        new_grid = []

        for row_number in range(20):
            row = []

            for column_number in range(20):
                cell = pydom[f"span#_{row_number}cell{column_number}"][0]
                cell.style["background-color"] = "lawngreen"
                cell.style["color"] = "lawngreen"
                row.append(cell)

            new_grid.append(row)

        self.grid = numpy.array(new_grid)

    def get_color(self, value, exceed=True):
        if not (0 <= (alpha := (6 - value) / 6) <= 1):
            alpha = 1 if exceed or value > 1 else 0

        color = "#" + "".join([hex(int(LAWNGREEN[index] + (BROWN[index] - LAWNGREEN[index]) * alpha))[2:] for index in range(3)])
        self.start.html = f'Play * {self.time}, {color}'
        return color

    def change_color(self, row: int, column: int, exceed=True):
        # print(f"{row=} {column=} {color=}")
        cell = self.grid[row][column]
        print(type(cell), type(self.grid))
        color = self.get_color(self.lifespans[row][column], exceed)
        cell.style["background-color"] = color
        cell.style["color"] = color

    def press(self, event):
        self.time += 1
        self.start.html = f'Play * {self.time}'
        # self.change_color(int(event.target.getAttribute("data-y")), int(event.target.getAttribute("data-x")),
        #                   self.get_color(random.randint(0, 6)))

        iteration = 0

        while not worker.sync.stop() and self.leftover > 0:
            if iteration % self.rate == 0:
                self.leftover -= 1
                print(self.leftover)
                self.leftover_line.html = f"{self.leftover} gallons remaining"
                row, column = int(event.target.getAttribute("data-y")), int(event.target.getAttribute("data-x"))
                self.lifespans[row][column] += 1
                self.change_color(row, column, exceed=False)

            iteration += 1

        if worker.sync.stop:
            print("read end")

        if self.leftover == 0:
            print(self.lifespans)
            self.reset()

    # def release(self, event):
    #     print("END")
    #     self.subtract = False

game = Game()
worker = PyWorker("./assets/worker.py", type="pyodide")
worker.sync.stop = (lambda: 0)

@when("mousedown", "span")
def down(event):
    game.press(event)