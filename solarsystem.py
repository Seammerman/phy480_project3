# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 19:57:38 2017

@author: samme
"""

import numpy as np
import planetclass as pclass

class solar:
    def __init__(self, name):
        self.name = name
        self.planets = []
        self.G = 6.67*10**(-11)
        self.dt = 1 # years
        self.N = np.size(self.planets)
        self.temp_pos = self.temp_vel = self.temp_acc = np.array([0,0,0])
        
    def addplanet(self,planetname, mass, x, y, z, vx, vy, vz):
        temp_name = planetname
        planetname = pclass.planet(temp_name, mass, x, y, z, vx, vy, vz)
        self.planets.append(planetname)
        
    # Interactive functions
    def distance(self,planet1, planet2):
        pos1 = planet1.position
        pos2 = planet2.position
        separation = pos2 - pos1
        radius = np.dot(separation,separation)
        return radius, separation
        
    def force(self,planet1, planet2):
        radius, separation = self.distance(planet1, planet2)
        unit_vec = separation / radius
        F = self.G * planet1.mass * planet2.mass / radius**2 * unit_vec
        return F
        
    # temporary X[i+1] functions
    def next_pos(self,planet):
        self.temp_pos = []
        self.temp_pos = planet.position + self.dt * planet.velocity + 1/2 * self.dt**2 * planet.acceleration
    def next_vel(self,planet):
        self.temp_vel = []
        self.temp_vel = planet.velocity + self.dt * 1/2 *(temp_acc + planet.acceleration)
    def next_acc(self,planet):
        self.temp_acc = []
        for jj in np.arange(0,self.N):
            if self.planets[jj].name == planet.name:
                continue
            self.temp_acc += 1/self.planets[jj].mass * self.force(planet,self.planets[jj])
            
    # update functions
    def update_pos(self,planet):
        planet.output()
        planet.position = self.temp_pos
    def update_vel(self,planet):
        planet.velocity = self.temp_vel
    def update_acc(self,planet):
        planet.acceleration = self.temp_acc
        

    # main solver
    def go(self):
        if np.size(self.planets) == self.N:
            pass
        else:
            self.N = np.size(self.planets)
        for j in np.arange(0,self.N):
            # designate the planet
            P = self.planets[j]
            # generate X[i+1] vectors
            self.next_pos(P)
            self.next_acc(P)
            self.next_vel(P)
            
            # update planet objects
            self.update_pos(P)
            self.update_acc(P)
            self.update_vel(P)
    