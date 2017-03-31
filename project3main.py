# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 01:35:26 2017

@author: samme
"""
import solarsystem as ss
import planetclass as pclass

def main():
    # form the solar system
    sol = ss.solar('sol')
    
    # put some objects in the solar system
    sol.addplanet('sun', 1.989*10**30, 0, 0, 0, 0, 0, 0)
    
    sol.addplanet('earth',5.972*10**24,1.496*10**11,0,0,0,30000,0)
  
    sol.go()