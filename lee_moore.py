import numpy as np
import time
from settings import *
from util import *

class LeeMooreAlg:
    """
    Implementation of the Lee Moore Algorithm
    """
    def __init__(self, canvas, dimensions, grid, blocks, wires):
        """
        Initialize variables
        """
        self.c = canvas
        self.grid = grid
        self.blocks = blocks
        self.wires = wires
        self.dimensions = dimensions
        
        self.run_button = None
        self.start_button = None
        self.next_button = None
        
        # Initialize map (an array representation of the grid)
        self.map = np.zeros((dimensions["x"], dimensions["y"]))
        for block in self.blocks:
            self.map[block[0], block[1]] = -1
        for wire in self.wires:
            for pin in self.wires[wire]:
                self.map[pin[0], pin[1]] = wire
        print(self.map)

    def start_algorithm(self):
        """
        Initialize the algorithm by choosing a wire and the source/drain pins, then adding the first
        grid to the expansion list
        """
        print("Running Lee Moore algorithm...")
        # Disable "run" button
        if self.run_button is not None:
            self.run_button["state"] = "disabled"
            self.next_button["state"] = "normal"
            self.start_button["state"] = "disabled"
        
        # 1. Choose a start and end
        self.set_source_sink()
        
        # 2. Add source to expansion list
        self.expansion_list = [(1, self.current_source)]
        
        # Set path to be not yet found
        self.path = [-1, -1]
        
        
    def label_box(self, x, y, num):
        """
        Label a grid box with (num) at (x, y) coordinates
        """
        # If the map shows 0, the block is empty
        if (self.map[x, y] == 0.0):
            # Update map
            self.map[x, y] = -1 * num
            # Update expansion list
            self.expansion_list.append((num, [x, y]))
            # Add label
            add_text(x, y, self.c, self.grid, num, tag="numbers")
            # Update canvas
            self.c.update()
            time.sleep(display_speed)
        

    def clear_canvas(self):
        """
        Clear the canvas of numbers used in the algorithm and reset map to prepare for next wire
        """
        # Clear all number text
        self.c.delete("numbers")
        
        # Clear completed pins/wire from list
        try:
            self.wires[self.current_wire].remove(self.current_drain)
        except ValueError:
            # The drain might not be a pin
            pass
        self.wires[self.current_wire].remove(self.current_source)        
        if (len(self.wires[self.current_wire]) == 0):
            del self.wires[self.current_wire]
            
        # Reset map to 0 for all empty blocks
        for row in range(self.map.shape[0]):
            for col in range(self.map.shape[1]):
                if self.map[row, col] < -1:
                    self.map[row, col] = 0
                    
        # Reset run button
        if self.run_button is not None:
            self.run_button["state"] = "normal"
            self.start_button["state"] = "normal"
            self.next_button["state"] = "disabled"
            
        print(self.map)
        print(self.wires)
        
        
    def next_step(self):
        """
        Perform next step of the Lee-Moore Algorithm (step through algorithm)
        """
        print("Expansion List: {}".format(self.expansion_list))
        
        # Check that the expansion list is not empty
        if(len(self.expansion_list) > 0):
            # Sort and pop the lowest number entry
            self.expansion_list.sort()
            expansion_number, next_box = self.expansion_list.pop(0)
            print("Next grid: {}".format(next_box))
            
            num = expansion_number + 1
            
            # Check top, left, right, bottom blocks
            for x, y in [
                (next_box[0], next_box[1]-1),
                (next_box[0]-1, next_box[1]),
                (next_box[0]+1, next_box[1]),
                (next_box[0], next_box[1]+1)
            ]:
                if (x in range(self.dimensions["x"]) and y in range(self.dimensions["y"])):
                
                    # Label the block
                    self.label_box(x, y, num)
                    
                    # Check for matching wire
                    if self.map[x, y] == self.current_wire and [x, y] != self.current_source:
                        # If drain is found, the expansion list can be cleared
                        self.expansion_list.clear()
                        print("Drain reached! Drain: {}".format([x, y]))
                        self.current_drain = [x, y]
                        
                        # Find next box to connect drain to
                        for x, y in [
                            (x, y-1),
                            (x-1, y),
                            (x+1, y),
                            (x, y+1)
                        ]:
                            if self.map[x, y] < -1:
                                self.path = [x, y]
                                break
                        break
            
        # If the expansion list is empty but no path is found, there is no solution
        elif self.path == [-1, -1]:
            print("No solution found!")
            self.clear_canvas()
            return -1
            
        # Otherwise, a path has been found
        else:
            # Draw the wire
            draw_box(self.path[0], self.path[1], self.c, self.grid, wire_colour_palette[self.current_wire])
            self.c.update()
            time.sleep(display_speed)
            
            num = self.map[self.path[0], self.path[1]]
            # Update map
            self.map[self.path[0], self.path[1]] = self.current_wire
            
            # Find next box for the wire
            for x, y in [
                (self.path[0], self.path[1]-1),
                (self.path[0]-1, self.path[1]),
                (self.path[0]+1, self.path[1]),
                (self.path[0], self.path[1]+1)
            ]:
                if self.map[x, y] > num and self.map[x, y] < -1:
                    self.path = [x, y]
                    break
                
            # If no next box found, the routing is complete
            if self.map[self.path[0], self.path[1]] == self.current_wire:
                print(self.path)
                print("Done routing wire {w} from {s}".format(w=self.current_wire, s=self.current_source))
                self.clear_canvas()
                return 1
        return 0
            

    def run_algorithm(self):
        """
        Run the Lee-Moore algorithm for a set of 2 pins
        """
        print("Running Lee Moore algorithm...")
        
        # Initialize
        self.start_algorithm()
        self.start_button["state"] = "disabled"
        self.next_button["state"] = "disabled"
        
        # Loop until a path is found
        while(1):
            result = self.next_step()
            if result != 0:
                break
        
    
    def set_source_sink(self):
        """
        Choose pins for the source and the sink
        """
        # Arbitrarily select an available source/sink
        self.current_wire = next(iter(self.wires))
        self.current_source = self.wires[self.current_wire][0]
        
        print("Source: {s}".format(s=self.current_source))