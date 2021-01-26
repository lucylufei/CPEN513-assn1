
def draw_box(x, y, c, grid, colour, tag=""):
    """
    Draw a box on the canvas (c) at (x, y) coordinates at (grid) size with (colour)
    """
    c.create_rectangle(
        x * grid["width"], y * grid["height"],
        (x + 1) * grid["width"], (y + 1) * grid["height"],
        fill=colour,
        tag=tag
    )
    
def add_text(x, y, c, grid, text, colour="black", tag=""):
    """
    Add (text) on the canvas (c) at (x, y) coordinates with (grid) size in (colour) with (tag)
    """
    c.create_text(
        x * grid["width"] + grid["width"] / 2,
        y * grid["height"] + grid["height"] / 2,
        text=text,
        fill=colour,
        tag=tag
    )
    
def manhattan_distance(x1, y1, x2, y2):
    '''
    Calculate the manhattan distance between points (x1, y1) and (x2, y2)
    '''
    distance = abs(x1 - x2) + abs(y1 - y2)
    return distance
    