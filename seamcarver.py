#!/usr/bin/env python3

from picture import Picture
from math import sqrt

class SeamCarver(Picture):
    ## TO-DO: fill in the methods below
    def energy(self, i: int, j: int) -> float:
        '''
        Return the energy of pixel at column i and row j
        '''
        if i-1 < 0:
            p1x = self[self.width()-1, j]
            p2x = self[i+1,j]
            rgbx = {'rx':abs(p1x[0]-p2x[0]), 'gx':abs(p1x[1]-p2x[1]), 'bx':abs(p1x[2]-p2x[2])}
        elif i+1 == self.width():
            p1x = self[i-1, j]
            p2x = self[0,j]
            rgbx = {'rx':abs(p1x[0]-p2x[0]), 'gx':abs(p1x[1]-p2x[1]), 'bx':abs(p1x[2]-p2x[2])}
        else:
            p1x = self[i+1, j]
            p2x = self[i-1,j]
            rgbx = {'rx':abs(p1x[0]-p2x[0]), 'gx':abs(p1x[1]-p2x[1]), 'bx':abs(p1x[2]-p2x[2])}
        if j-1 < 0:
            p1y = self[i, self.height()-1]
            p2y = self[i,j+1]
            rgby = {'ry':abs(p1y[0]-p2y[0]), 'gy':abs(p1y[1]-p2y[1]), 'by':abs(p1y[2]-p2y[2])}
        elif j+1 == self.height():
            p1y = self[i, 0]
            p2y = self[i,j-1]
            rgby = {'ry':abs(p1y[0]-p2y[0]), 'gy':abs(p1y[1]-p2y[1]), 'by':abs(p1y[2]-p2y[2])}
        else:
            p1y = self[i, j+1]
            p2y = self[i,j-1]
            rgby = {'ry':abs(p1y[0]-p2y[0]), 'gy':abs(p1y[1]-p2y[1]), 'by':abs(p1y[2]-p2y[2])}
            #rgb= {'rx':abs(p1x[0]-p2x[0]), 'gx':abs(p1x[1]-p2x[1]), 'bx':abs(p1x[2]-p2x[2]), 'ry':abs(p1y[0]-p2y[0]), 'gy':abs(p1y[1]-p2y[1]), 'by':abs(p1y[2]-p2y[2])}
        
        e = sqrt((rgbx['rx']**2+rgbx['gx']**2+rgbx['bx']**2)+(rgby['ry']**2+rgby['gy']**2+rgby['by']**2))

        return e
        raise NotImplementedError

    def find_vertical_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        vertical seam
        '''
        energies= {}

        for y in range(self.height()):
            for x in range (self.width()):
                add = 0
                if y-1 < 0:
                    add = self.energy(x, y)
                    energies[x, y] = add
                elif x-1 < 0:
                    add = self.energy(x,y) + min(energies[x,y-1],energies[x+1,y-1]) 
                    energies[x, y] = add
                elif x+1 == self.width():
                    add = self.energy(x,y) + min(energies[x-1,y-1],energies[x,y-1])
                    energies[x, y] = add
                else:
                    add = self.energy(x,y) + min(energies[x-1,y-1],energies[x,y-1],energies[x+1,y-1])
                    energies[x, y] = add
        bottom = []
        for x in range(self.width()):
            bottom.append(energies[x,self.height()-1])
        
        min_index = bottom.index(min(bottom))
        vseam = [min_index]

        for y in reversed(range(self.height())):
            if y+-1 < 0:
                min_index += 0
            elif min_index-1 < 0:
                subprobs = [energies[min_index, y-1], energies[min_index+1, y-1]]
                if subprobs.index(min(subprobs)) == 0:
                    vseam.append(min_index)
                else:
                    min_index += 1
                    vseam.append(min_index)
            elif min_index+1 == self.width():
                subprobs = [energies[min_index, y-1], energies[min_index-1, y-1]]
                if subprobs.index(min(subprobs)) == 0:
                    vseam.append(min_index)
                else:
                    min_index -= 1
                    vseam.append(min_index)
            else:
                subprobs = [energies[min_index-1,y-1],energies[min_index,y-1],energies[min_index+1,y-1]]
                if subprobs.index(min(subprobs)) == 0:
                    min_index -= 1
                    vseam.append(min_index)
                elif subprobs.index(min(subprobs)) == 1:
                    vseam.append(min_index)
                else:
                    min_index += 1
                    vseam.append(min_index)
        return reversed(vseam)
    
        raise NotImplementedError

    def find_horizontal_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        horizontal seam
        '''
        raise NotImplementedError

    def remove_vertical_seam(self, seam: list[int]):
        '''
        Remove a vertical seam from the picture
        '''

        raise NotImplementedError

    def remove_horizontal_seam(self, seam: list[int]):
        '''
        Remove a horizontal seam from the picture
        '''
        raise NotImplementedError

class SeamError(Exception):
    pass
