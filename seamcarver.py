#!/usr/bin/env python3

from picture import Picture
from math import sqrt
from PIL import Image

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
        #bottom-top approach; get energies of the bottom row first
        energies= []
        for x in range(self.width()):
            energies.append(self.energy(x, self.height()-1))
        
        #apply M(i, j) = e(i, j) + min(M(i-1, j-1),M(i, j-1), M(i+1, j-1)) among other cases, i.e. edges/borders; bottom-top direction
        for y in reversed(range(self.height())):
            for x in range (self.width()):
                add = 0
                if x-1 < 0 and y-1 >= 0:
                    add = min(self.energy(x,y-1),self.energy(x+1,y-1))
                elif x+1 == self.width() and y-1 >=0:
                    add = min(self.energy(x-1,y-1),self.energy(x,y-1))
                elif y-1 < 0:
                    add = self.energy(x, y)
                else:
                    add = min(self.energy(x-1,y-1),self.energy(x,y-1),self.energy(x+1,y-1))
                energies[x]+add

        #backtracking; store index of minimum energy from top-bottom
        m_index = energies.index(min(energies))
        vseam = [m_index]
        
        # Backtracking step
        for y in range(1, self.height()):  # Start from the second row
            subprobs = []
            # Consider three neighboring pixels from the previous row
            if m_index - 1 >= 0:
                subprobs.append(self.energy(m_index - 1, y))  # Left neighbor
            subprobs.append(self.energy(m_index, y))  # Center neighbor
            if m_index + 1 < self.width():
                subprobs.append(self.energy(m_index + 1, y))  # Right neighbor
            
            min_energy_index = subprobs.index(min(subprobs))  # Get the index of the minimum energy
            
            # Update the current column index based on the minimum energy
            if min_energy_index == 0:
                m_index -= 1  # Move left
            elif min_energy_index == 1:
                m_index  # Stay in the center
            else:
                m_index += 1  # Move right
            
            vseam.append(m_index)
                
        return vseam
        raise NotImplementedError

    def find_horizontal_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        horizontal seam
        '''
        #creates a rotated img, does not affect the original img itself
        img = SeamCarver(self.picture().transpose(Image.ROTATE_90)) #rotates the image so the columns and rows switch positions
        horizontal_seam = img.find_vertical_seam() #runs find_vertical_seam on the rotated image

        return horizontal_seam
        raise NotImplementedError

    def remove_vertical_seam(self, seam: list[int]):
        '''
        Remove a vertical seam from the picture
        '''
        
        for y in range(self.height()):
            seam_index = seam[y]  # Get the seam index for the current row
            
            # Shift all pixels in the row to the left of the seam
            for x in range(seam_index, self.width() - 1):
                self[x, y] = self[x + 1, y]
            
            # Remove the last pixel in the row
            del self[self.width() - 1, y]
            
        # After shifting, the width of the image decreases by 1
        self._width -= 1

        if self._width <= 0: 
            raise SeamError("Image width is zero.")

    def remove_horizontal_seam(self, seam: list[int]):
        '''
        Remove a horizontal seam from the picture
        '''
        raise NotImplementedError

class SeamError(Exception):
    pass
