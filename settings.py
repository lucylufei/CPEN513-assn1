
# GUI settings
screensize = {
    "width": 1000, 
    "height": 500
}

background_colour = "white"
line_colour = "black"
block_colour = "gray"
wire_colour_palette = [
    "pink",
    "plum", 
    "turquoise",
    "lightblue",
    "salmon",
    "lightgreen",
    "lavender",
    "DarkSeaGreen",
    "coral"
]

# The interval (in seconds) at which numbers are displayed and cells are coloured in the GUI. 
display_delay = 0

# Setting for order of the wires. Possible options: in_order, random, optimized, override
wire_selection = "optimized"
# Number of iterations to optimize for
optimization_iterations = 50

# Special setting to test out a hardcoded order (used with wire_selection is set to "override")
override_wire_order = [4, 3, 1, 2]

# Algorithm. Possible options: astar, leemoore
algorithm = "leemoore"

# Infile file name
filename = input("Infile: ")

# Toggle for alert at the end of routing. 
output_style = "log"

# Log file
output_file = open("./logs/{f}_{t}.log".format(f=filename, t=algorithm), "w+")

# A* configuration for calculating the Manhattan distance
find_closest_source = True