import numpy as np
import time
from settings import *
from util import *

class LeeMooreAlg:
    def __init__(self, canvas, dimensions, grid, blocks, wires):
        self.c = canvas
        self.grid = grid
        self.blocks = blocks
        self.wires = wires
        self.dimensions = dimensions
        
        # Initialize map
        self.map = np.zeros((dimensions["x"], dimensions["y"]))
        for block in self.blocks:
            self.map[block[0], block[1]] = -1
        for wire in self.wires:
            for pin in self.wires[wire]:
                self.map[pin[0], pin[1]] = wire
        print(self.map)

    def start_algorithm(self):
        print("Running Lee Moore algorithm...")
        
        # 1. Choose a start and end
        self.set_source_sink()
        
        # 2. Add source to expansion list
        self.expansion_list = [(1, self.current_source)]
        
        self.path = [-1, -1]
        
        
    def label_box(self, x, y, num):
        if (x in range(self.dimensions["x"]) and y in range(self.dimensions["y"])):
            if (self.map[x, y] == 0.0):
                self.map[x, y] = -1 * num
                self.expansion_list.append((num, [x, y]))
                add_text(x, y, self.c, self.grid, num, tag="numbers")
                self.c.update()
                # time.sleep(1)
        

    def clear_canvas(self):
        self.c.delete("numbers")
        self.wires[self.current_wire].remove(self.current_source)        
        self.wires[self.current_wire].remove(self.current_drain)
        if (len(self.wires[self.current_wire]) == 0):
            del self.wires[self.current_wire]
            
        for row in range(self.map.shape[0]):
            for col in range(self.map.shape[1]):
                if self.map[row, col] < -1:
                    self.map[row, col] = 0
            
        print(self.map)
        print(self.wires)
        
        
    def next_step(self):
        print("Expansion List: {}".format(self.expansion_list))
        if(len(self.expansion_list) > 0):
            self.expansion_list.sort()
            expansion_number, next_box = self.expansion_list.pop(0)
            print("Next grid: {}".format(next_box))
            
            num = expansion_number + 1
            
            # Check top, left, right, bottom
            for x, y in [
                (next_box[0], next_box[1]-1),
                (next_box[0]-1, next_box[1]),
                (next_box[0]+1, next_box[1]),
                (next_box[0], next_box[1]+1)
            ]:
                self.label_box(x, y, num)
                if [x, y] == self.current_drain:
                    self.expansion_list.clear()
                    print("Drain reached!")
                    
                    # Find next box
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
        
        elif self.path is [-1, -1]:
            print("No solution found!")
            
        else:
            draw_box(self.path[0], self.path[1], self.c, self.grid, wire_colour_palette[self.current_wire])
            num = self.map[self.path[0], self.path[1]]
            self.map[self.path[0], self.path[1]] = self.current_wire
            
            # Find next box
            for x, y in [
                (self.path[0], self.path[1]-1),
                (self.path[0]-1, self.path[1]),
                (self.path[0]+1, self.path[1]),
                (self.path[0], self.path[1]+1)
            ]:
                if self.map[x, y] > num and self.map[x, y] < -1:
                    self.path = [x, y]
                    break
                
            if self.map[self.path[0], self.path[1]] == self.current_wire:
                print("Done routing wire {w} from {s} to {d}".format(w=self.current_wire, s=self.current_source, d=self.current_drain))
                self.clear_canvas()
                return 1
        return 0
            

    def run_algorithm(self):
        print("Running Lee Moore algorithm...")
        
        self.start_algorithm()
        while(1):
            result = self.next_step()
            if result == 1:
                break
        
    
    def set_source_sink(self):
        # Randomly select an available source/sink
        self.current_wire = next(iter(self.wires))
        self.current_source = self.wires[self.current_wire][0]
        self.current_drain = self.wires[self.current_wire][1]
        
        print("Source: {s}, Drain: {d}".format(s=self.current_source, d=self.current_drain))