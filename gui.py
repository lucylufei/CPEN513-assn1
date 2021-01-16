import os
from tkinter import *
from tkinter.ttk import *
from infile_parser import *
from lee_moore import *

# filename = input("Infile: ")
filename = "kuma"
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

# Lee-Moore algorithm
leemore = LeeMooreAlg(c, dimensions, grid, blocks, wires)

# Add buttons to the GUI
button_frame = Frame(root, width=screensize["width"])
run_button = Button(button_frame, text ="Connect 1 Pin", command=leemore.run_algorithm)
start_button = Button(button_frame, text ="Start", command=leemore.start_algorithm)
next_button = Button(button_frame, text ="Next", command=leemore.next_step, state="disabled")
debug_button = Button(button_frame, text ="Debug", command=leemore.debug)
go_button = Button(button_frame, text="Go", command=leemore.run)

# Add buttons to algorithm
leemore.run_button = run_button
leemore.start_button = start_button
leemore.next_button = next_button

button_frame.pack()
start_button.grid(row=0, column=0)
next_button.grid(row=0, column=1)
run_button.grid(row=0, column=2)
debug_button.grid(row=0, column=3)
go_button.grid(row=0, column=4)

# Run GUI
root.mainloop()


    