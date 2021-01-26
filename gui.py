import os
from tkinter import *
from tkinter.ttk import *
from infile_parser import *
from lee_moore import *
from astar import *


print("Importing file...")
dimensions, blocks, wires = parse_file("benchmarks/{}.infile".format(filename))
print("Import complete. ")

# Setup tkinter GUI interface
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
        add_text(pin[0], pin[1], c, grid, chr(wire + 64))

if algorithm == "astar":
    # A* algorithm
    print("Running A* algorithm...")
    alg = AStarAlg(c, dimensions, grid, blocks, wires)
elif algorithm == "leemoore":
    # Lee-Moore algorithm
    print("Running Lee-Moore algorithm...")
    alg = LeeMooreAlg(c, dimensions, grid, blocks, wires)
else:
    raise Exception

# Add buttons to the GUI
button_frame = Frame(root, width=screensize["width"])
run_button = Button(button_frame, text ="Connect 1 Pin", command=alg.run_algorithm)
start_button = Button(button_frame, text ="Init", command=alg.start_algorithm)
next_button = Button(button_frame, text ="Step", command=alg.next_step, state="disabled")
debug_button = Button(button_frame, text ="Debug", command=alg.debug)
go_button = Button(button_frame, text="Run Once", command=alg.run)
benchmark_button = Button(button_frame, text="Optimize", command=alg.benchmark)
reset_button = Button(button_frame, text="Reset", command=alg.reset)

# Add buttons to algorithm
alg.run_button = run_button
alg.start_button = start_button
alg.next_button = next_button

button_frame.pack()
start_button.grid(row=0, column=0)
next_button.grid(row=0, column=1)
run_button.grid(row=0, column=2)
debug_button.grid(row=0, column=3)
go_button.grid(row=0, column=4)
reset_button.grid(row=0, column=5)
benchmark_button.grid(row=0, column=6)

# Run GUI
root.mainloop()


    