
def parse_file(filename):
    """
    Parse '*.infile'
    Input: filename
    Output: dimensions, blocks, wires
    """
    blocks = []
    wires = {}
    
    f = open(filename, "r")
    
    # Read first line as dimensions
    line = f.readline()
    x_max, y_max = line.strip().split(" ")
    print("Dimensions: {x} x {y}".format(x=x_max, y=y_max))
    dimensions = {"x": int(x_max), "y": int(y_max)}
    
    # Read second line as number of blocks
    line = f.readline()
    num_blocks = int(line.strip())
    print("Number of blocks: {}".format(num_blocks))
    
    # Read all the blocks
    for i in range(num_blocks):
        line = f.readline()
        x, y = line.strip().split(" ")
        blocks.append([int(x), int(y)])
        
    # Check that the number of blocks read is expected
    assert len(blocks) == num_blocks
        
    # Read next line as number of wires
    line = f.readline()
    num_wires = int(line.strip())
    print("Number of wires: {}".format(num_wires))
    
    # Read each wire
    for i in range(num_wires):
        line = f.readline()
        # Start numbering wires from 1
        wires[i + 1] = []
        num_pins = int(line.strip().split(" ")[0])
        # Add pins for each wire
        for j in range(num_pins):
            x = line.strip().split(" ")[j * 2 + 1]
            y = line.strip().split(" ")[j * 2 + 2]
            wires[i + 1].append([int(x), int(y)])
            
        print("Wire {x}: {y}".format(x=i+1, y=wires[i+1]))
        
    f.close()
    
    return dimensions, blocks, wires