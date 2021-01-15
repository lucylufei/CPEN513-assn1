import os
from tkinter import *
from settings import *
from infile_parser import *
from lee_moore import *


def draw_box(x, y, c, grid, colour):
    c.create_rectangle(
        x * grid["width"], y * grid["height"],
        (x + 1) * grid["width"], (y + 1) * grid["height"],
        fill=colour
    )
    
def add_text(x, y, c, grid, text, colour="black"):
    c.create_text(
        x * grid["width"] + grid["width"] / 2,
        y * grid["height"] + grid["height"] / 2,
        text=text,
        fill=colour
    )

# filename = input("Infile: ")
filename = "stdcell"
print("Importing file...")
dimensions, blocks, wires = parse_file("benchmarks/{}.infile".format(filename))
print("Import complete. ")

root = Tk()
grid = {"width": screensize["width"] / dimensions["x"], "height": screensize["height"] / dimensions["y"]}
frame = Frame(root, width=screensize["width"], height=screensize["height"])
frame.pack()
c = Canvas(frame, bg=background_colour, width=screensize["width"], height=screensize["height"])
c.pack()

print("Drawing grid...")
for x in range(dimensions["x"]):
    c.create_line(x * grid["width"], 0, x * grid["width"], screensize["height"], fill=line_colour)
for y in range(dimensions["y"]):
    c.create_line(0, y * grid["height"], screensize["width"], y * grid["height"], fill=line_colour)
    
print("Adding blocks...")
for block in blocks:
    draw_box(block[0], block[1], c, grid, block_colour)
    
print("Adding pins...")
for wire in wires:
    for pin in wires[wire]:
        draw_box(pin[0], pin[1], c, grid, wire_colour_palette[wire])
        add_text(pin[0], pin[1], c, grid, chr(wire + 65))


button_frame = Frame(root, width=screensize["width"], height=100)
start_button = Button(button_frame, text ="Start", command=start_algorithm)
next_button = Button(button_frame, text ="Next", command=next_step)
run_button = Button(button_frame, text ="Run", command=run_algorithm)

button_frame.pack()
start_button.grid(row=0, column=0)
next_button.grid(row=0, column=1)
run_button.grid(row=0, column=2)


root.mainloop()
