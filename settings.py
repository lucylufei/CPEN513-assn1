
# Settings
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

display_delay = 0.1

wire_selection = "optimized"
optimization_iterations = 50

algorithm = "astar"

filename = input("Infile: ")
output_style = "log"
if output_style == "log":
    output_file = open("{}_log.log".format(filename), "w+")
    
    
find_closest_drain = True