import time
import tkinter as tk
from threading import Thread
from tkinter import ttk

MIN_SPEED = 1
MAX_SPEED = 100

class Life:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Game of Life")

        self.grid_size = 20
        self.cell_size = 20

        self.running = False
        self.speed = (MIN_SPEED + MAX_SPEED) // 2

        self.iteration = 0

        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]

        self.create_widgets()

        self.root.mainloop()


    def create_widgets(self):
        # control buttons
        self.start_button = ttk.Button(self.root, text="Start", command=self.start)
        self.start_button.grid(row=0, column=0, pady=10)

        self.stop_button = ttk.Button(self.root, text="Stop", command=self.stop)
        self.stop_button.grid(row=0, column=1)

        self.reset_button = ttk.Button(self.root, text="Reset", command=self.reset)
        self.reset_button.grid(row=0, column=2)

        # speed slider
        tk.Label(self.root, text="Speed:").grid(row=1, column=0)
        self.speed_scale = tk.Scale(self.root, from_=MIN_SPEED, to=MAX_SPEED, resolution=1, orient="horizontal", command=self.update_speed)
        self.speed_scale.set(self.speed)
        self.speed_scale.grid(row=1, column=1)

        # iteration label
        self.iteration_label = tk.Label(self.root, text="Iteration: 0")
        self.iteration_label.grid(row=3, column=0, sticky="w")

        # grid canvas
        self.canvas = tk.Canvas(self.root, width=self.grid_size * self.cell_size,
                                height=self.grid_size * self.cell_size, bg="white")
        self.canvas.grid(row=2, column=0, columnspan=3, padx=5, pady=5)

        self.canvas.bind("<Button-1>", self.toggle_cell)

        self.draw_grid()

    def toggle_cell(self, event):
        x = event.x // self.cell_size
        y = event.y // self.cell_size

        if 0 <= x < self.grid_size and 0 <= y < self.grid_size:
            self.grid[y][x] = 1 - self.grid[y][x]
            if self.grid[y][x]:
                color = "black"
            else:
                color = "white"
            #x = self.canvas.find_closest(event.x, event.y)
            self.update_canvas_cell(y, x)

    def draw_grid(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                x1 = j * self.cell_size
                x2 = x1 + self.cell_size
                y1 = i * self.cell_size
                y2 = y1 + self.cell_size

                if self.grid[i][j]:
                    color = "black"
                else:
                    color = "white"

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray", tags=f"{i}-{j}")

    def update_canvas_cell(self, row, col):
        color = "black" if self.grid[row][col] else "white"
        self.canvas.itemconfig(f"{row}-{col}", fill=color)

    def redraw_canvas(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                self.update_canvas_cell(i, j)

    def start(self):
        if not self.running:
            self.running = True
            Thread(target=self.simulation, daemon=True).start()

    def stop(self):
        self.running = False

    def  reset(self):
        self.grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]
        self.iteration = 0
        self.iteration_label.config(text=f"Iteration: {self.iteration}")

        self.canvas.delete("all")
        self.draw_grid()

    def update_speed(self, value):
        self.speed = int(float(value))

    def simulation(self):
        while self.running:
            self.iteration += 1

            new_grid = [[0 for _ in range(self.grid_size)] for _ in range(self.grid_size)]

            for y in range(self.grid_size):
                for x in range(self.grid_size):
                    alive = self.count_alive_neighbours(x, y)

                    if self.grid[y][x] == 1 and alive in (2, 3):
                        new_grid[y][x] = 1
                    elif self.grid[y][x] == 0 and alive == 3:
                        new_grid[y][x] = 1

            self.grid = new_grid
            self.redraw_canvas()
            self.iteration_label.config(text=f"Iteration: {self.iteration}")
            print(self.speed)
            time.sleep((MAX_SPEED + 1 - self.speed)/ (1.0*MAX_SPEED))

    def count_alive_neighbours(self, x, y):
        count = 0

        #left
        if x > 0:
            count += self.grid[y][x-1]
        #right
        if x < self.grid_size - 1:
            count += self.grid[y][x+1]
        #top
        if y > 0:
            count += self.grid[y-1][x]
        #bottom
        if y < self.grid_size - 1:
            count += self.grid[y+1][x]
        #top left
        if x > 0 and y > 0:
            count += self.grid[y-1][x-1]
        #top right
        if x < self.grid_size - 1 and y > 0:
            count += self.grid[y-1][x+1]
        #bottom left
        if x > 0 and y < self.grid_size - 1:
            count += self.grid[y+1][x-1]
        #bottom right
        if x < self.grid_size - 1 and y < self.grid_size - 1:
            count += self.grid[y+1][x+1]

        return count

if __name__ == '__main__':
    life = Life()
