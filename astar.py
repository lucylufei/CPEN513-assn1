from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox 
import numpy as np
import time
import random
import copy
from settings import *
from util import *

np.set_printoptions(threshold=np.inf)

class AStarAlg:
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
        self.original_wires = copy.deepcopy(wires)
        self.dimensions = dimensions
        
        self.run_button = None
        self.start_button = None
        self.next_button = None
        
        self.drain_list = {}
        
        # Count number of successful connections
        self.failed_pins = 0
        # Count total number of pins
        self.total_pins = 0
        # Count length of wires
        self.total_wire_length = 0
        
        # Count number of successful wires
        self.successful_wires = {}
        
        # Initialize map (an array representation of the grid)
        self.map = np.zeros((dimensions["x"], dimensions["y"]))
        for block in self.blocks:
            self.map[block[0], block[1]] = -1
        for wire in self.wires:
            for pin in self.wires[wire]:
                self.map[pin[0], pin[1]] = wire
        print(self.map)
        
        # Initialize map of previous steps
        self.reverse_pointer_map = [[(-1, -1) for i in range(dimensions["y"])] for j in range(dimensions["x"])]
        
        # Initialize to a random wire order
        self.optimal_wire_order = list(self.wires.keys())
        random.shuffle(self.optimal_wire_order)
        self.next_optimal_wire_order = self.optimal_wire_order.copy()
        print("Initial wire order: {}".format(self.optimal_wire_order))
        output_file.write("Initial wire order: {}\n".format(self.optimal_wire_order))
        self.optimal_wire_order_index = 0

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
        if self.set_source_sink() == 0:
            return 0
        
        # 2. Add source to expansion list
        self.expansion_list = [(1, self.current_source)]
        
        # Set path to be not yet found
        self.path = [-1, -1]
        
        
    def label_box(self, x, y, num, x1=-1, y1=-1):
        """
        Label a grid box with (num) at (x, y) coordinates
        """
        # If the map shows 0, the block is empty
        if (self.map[x, y] == 0.0):
            # Update map
            self.map[x, y] = -1 * num
            # Update expansion list
            self.expansion_list.append((num, [x, y]))
            # Update reverse pointer
            assert self.reverse_pointer_map[x][y] == (-1, -1)
            self.reverse_pointer_map[x][y] = [x1, y1]
            # Add label
            add_text(x, y, self.c, self.grid, num, tag="numbers")
            # Update canvas
            self.c.update()
            time.sleep(display_delay)
        

    def clear_canvas(self):
        """
        Clear the canvas of numbers used in the algorithm and reset map to prepare for next wire
        """
        # Clear all number text
        self.c.delete("numbers")
        
        self.map[self.current_source[0], self.current_source[1]] = self.current_wire * 1000
        self.drain_list[self.current_wire].add((self.current_source[0], self.current_source[1]))
        self.wires[self.current_wire].remove(self.current_source)        
        if (len(self.wires[self.current_wire]) == 1):
            if self.current_wire in self.successful_wires:
                assert(self.successful_wires[self.current_wire] == False)
            else:
                self.successful_wires[self.current_wire] = True
            del self.wires[self.current_wire]
            self.total_pins += 1
            self.optimal_wire_order_index += 1
            
        # Reset map to 0 for all empty blocks
        for row in range(self.map.shape[0]):
            for col in range(self.map.shape[1]):
                if self.map[row, col] < -1:
                    self.map[row, col] = 0
                    
        # Reset reverse pointers
        self.reverse_pointer_map = [[(-1, -1) for i in range(self.dimensions["y"])] for j in range(self.dimensions["x"])]
                    
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
            num, next_box = self.expansion_list.pop(0)
            print("Next grid: {}".format(next_box))
            
            
            # Check top, left, right, bottom blocks
            for x, y in [
                (next_box[0], next_box[1]-1),
                (next_box[0]-1, next_box[1]),
                (next_box[0]+1, next_box[1]),
                (next_box[0], next_box[1]+1)
            ]:
                if (x in range(self.dimensions["x"]) and y in range(self.dimensions["y"])):
                
                    # Find drain
                    if find_closest_drain:
                        num = manhattan_distance(x, y, self.current_drain[0], self.current_drain[1])
                        for drains in self.drain_list[self.current_wire]:
                            closest_drain = manhattan_distance(x, y, drains[0], drains[1])
                            if closest_drain < num:
                                num = closest_drain
                    else:
                        num = manhattan_distance(x, y, self.current_drain[0], self.current_drain[1])
                    
                    # Label the block
                    self.label_box(x, y, num, next_box[0], next_box[1])
                    
                    # Check for matching wire
                    if self.map[x, y] == (self.current_wire * 1000) and [x, y] != self.current_source:
                        # If drain is found, the expansion list can be cleared
                        self.expansion_list.clear()
                        print("Drain reached! Drain: {}".format([x, y]))
                        self.current_drain = [x, y]
                        
                        self.path = [next_box[0], next_box[1]]
                        break
            
        # If the expansion list is empty but no path is found, there is no solution
        elif self.path == [-1, -1]:
            print("No solution found!")
            output_file.write("No solution found for wire {w} on pin {p}.\n".format(w=self.current_wire, p=self.current_source))
            self.successful_wires[self.current_wire] = False
            self.failed_pins += 1
            self.clear_canvas()
            # Prioritize wire
            self.next_optimal_wire_order.insert(0, self.next_optimal_wire_order.pop(self.next_optimal_wire_order.index(self.current_wire)))
            return -1
            
        # Otherwise, a path has been found
        else:
            # Draw the wire
            draw_box(self.path[0], self.path[1], self.c, self.grid, wire_colour_palette[self.current_wire], tag="wire")
            self.c.update()
            time.sleep(display_delay)
            
            num = self.map[self.path[0], self.path[1]]
            # Update map
            self.map[self.path[0], self.path[1]] = self.current_wire * 1000
            self.drain_list[self.current_wire].add((self.path[0], self.path[1]))
            self.total_wire_length += 1
            
            # Find next box for the wire
            self.path = self.reverse_pointer_map[self.path[0]][self.path[1]]
                
            # If no next box found, the routing is complete
            if self.map[self.path[0], self.path[1]] == (self.current_wire * 1000):
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
        if self.start_algorithm() == 0:
            return 0
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
        if len(self.wires) == 0:
            print("No more wires to route!")
            return 0
        
        # Select a wire
        if wire_selection == "in_order":
            self.current_wire = next(iter(self.wires))
        elif wire_selection == "random":
            self.current_wire = random.choice(list(self.wires.keys()))
        elif wire_selection == "optimized":
            self.current_wire = self.optimal_wire_order[self.optimal_wire_order_index]
        else:
            raise Exception
        print("Routing wire {}...".format(self.current_wire))
        
        # Arbitrarily select an available source/sink
        self.current_source = random.choice(self.wires[self.current_wire][1:])
        
        if find_closest_drain:
            print("Searching for closest drain...")
            shortest_distance = self.dimensions["x"] * self.dimensions["y"]
            indices = np.where(self.map == self.current_wire * 1000)
            print("Possible drains: {}".format(list(zip(indices[0], indices[1]))))
            
            if len(list(zip(indices[0], indices[1]))) == 0:
                self.current_drain = self.wires[self.current_wire][0]
                # TODO: Choose closest pin for drain and then move to front of array
            else:    
                for index in list(zip(indices[0], indices[1])):
                    distance = manhattan_distance(self.current_source[0], self.current_source[1], index[0], index[1])
                    if distance < shortest_distance:
                        self.current_drain = index
                        shortest_distance = distance
                
                assert shortest_distance != self.dimensions["x"] * self.dimensions["y"]
                print("Closest drain found at {}".format(self.current_drain))
            
        else:
            self.current_drain = self.wires[self.current_wire][0]
            # TODO: Choose random pin for drain and then move to front of array
        
        self.map[self.current_drain[0], self.current_drain[1]] = self.current_wire * 1000
        try:
            self.drain_list[self.current_wire].add((self.current_drain[0], self.current_drain[1]))
        except KeyError:
            self.drain_list[self.current_wire] = set()
            self.drain_list[self.current_wire].add((self.current_drain[0], self.current_drain[1]))
        
        print("Source: {s}, Drain: {d}".format(s=self.current_source, d=self.current_drain))
        self.total_pins += 1
        
        
    def debug(self):
        print(self.map)
        print(self.reverse_pointer_map)
        
    def run(self):
        self.start_button["state"] = "disabled"
        self.next_button["state"] = "disabled"
        self.run_button["state"] = "disabled"
                
        while True:
            if self.run_algorithm() == 0:
                break
        
        total_wires = 0
        connected_wires = 0
        for wire in self.successful_wires:
            total_wires += 1
            if self.successful_wires[wire] == True:
                connected_wires += 1
         
        if output_style == "alert":
            messagebox.showinfo("Done",
                "Routing complete \n{x} of {y} wires successfully connected. \n{z} of {w} pins missing.".format(
                    x=connected_wires,
                    y=total_wires,
                    z=self.failed_pins,
                    w=self.total_pins
                )
            )  
        elif output_style == "log":
            output_file.write("Routing complete \n{x} of {y} wires successfully connected. \n{z} of {w} pins missing.\n".format(
                    x=connected_wires,
                    y=total_wires,
                    z=self.failed_pins,
                    w=self.total_pins)
            )
            output_file.write("Total wire length: {}\n".format(self.total_wire_length))
            output_file.write(np.array2string(self.map, precision=2, separator=',', suppress_small=True))
            output_file.write("\n")
            
    def reset(self):
        # Remove wires
        self.c.delete("wire")
        
        # Remove numbers
        self.c.delete("numbers")
        
        # Reset variables
        self.total_pins = 0
        self.failed_pins = 0
        self.successful_wires.clear()
        self.total_wire_length = 0
        self.path = [-1, -1]
        self.drain_list = {}
        self.optimal_wire_order_index = 0
        self.optimal_wire_order = self.next_optimal_wire_order.copy()
        print("New wire order: {}".format(self.optimal_wire_order))
        output_file.write("New wire order: {}\n".format(self.optimal_wire_order))
        self.wires = copy.deepcopy(self.original_wires)
        print(self.wires)
        
        # Reinitialize map (an array representation of the grid)
        self.map = np.zeros((self.dimensions["x"], self.dimensions["y"]))
        for block in self.blocks:
            self.map[block[0], block[1]] = -1
        for wire in self.wires:
            for pin in self.wires[wire]:
                self.map[pin[0], pin[1]] = wire
        print(self.map)
        
        # Reset reverse pointers
        self.reverse_pointer_map = [[(-1, -1) for i in range(self.dimensions["y"])] for j in range(self.dimensions["x"])]
        
        # Reset buttons
        self.start_button["state"] = "normal"
        self.next_button["state"] = "disabled"
        self.run_button["state"] = "normal"
        
    def benchmark(self):
        for i in range(optimization_iterations):
            self.run()
            if self.failed_pins == 0:
                print("Successful route found!")
                break
            self.reset()
            
        output_file.close()