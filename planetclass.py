# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 17:39:13 2017

@author: samme
"""
import numpy as np

class planet():
    def __init__(self, name, mass, x, y, z, vx, vy, vz):
        self.name = name
        self.mass = mass
        self.position = np.array([x,y,z])
        self.velocity = np.array([vx,vy,vz])
        self.acceleration = np.array([0,0,0])
        self.KE = 0
        self.PE = 0
        
    def kinetic_energy(self):
        self.KE = 1/2 * self.mass * np.dot(self.velocity,self.velocity)
        print(self.KE)
        
    def location(self):
        print('x: ' + str(self.position[0]))
        print('y: ' + str(self.position[1]))
        print('z: ' + str(self.position[2]))
    def output(self):
        file = open('planet_' + self.name + '.txt', 'w')
        s = '{0} {1} {2}'.format(self.position[0], self.position[1], self.position[2])
        file.write(s)
        file.close()