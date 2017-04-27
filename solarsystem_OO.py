# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 19:12:49 2017

@author: samme
"""
import numpy as np
import matplotlib.pyplot as plt
import planetclass as pc

tempG = 6.67*10**(-11); # unmolested gravitational constant
yr = 365*60*60*24; # number of seconds in a year
B = 5.972*10**24; # mass of the earth in kg
AU = 1.496*10**11; # 1 AU in meters
Ms = 332946.0487 # mass of the sun in units of mass of the earth
GMs = 4*np.pi**2 * AU**3 / yr**2

def distance(P1, P2):
    '''
    distance(P1, P2) will determine the radius and vectorized distance between two planets
    the separation vector will point from P1 to P2
    '''
    pos1 = P1
    pos2 = P2
    separation = pos2 - pos1
    radius = np.dot(separation,separation)**0.5
    return radius, separation
    
# this is also the force in units of AU, M(earth), years. Thus the acc of the earth takes the same form since Me == 1
def acc(P1,P2,mass1):
    '''
    the sep vector points from P1 to P2. Thus we want the planet of interest to be input as P2, 
    this way the sep vec points from say, the sun to the earth
    '''
    r,sep = distance(P1,P2)
    x,y,z = sep
    ax = x / (r)**3
    ay = y / (r)**3
    az = z / (r)**3
    output = -np.array([ax,ay,az]) * 4*np.pi**2 * mass1 / Ms
    return output  
    

def load_data(planet_name):
    fout = 'planet_' + planet_name
    data = np.loadtxt(fout)
    x = data[:,0]
    y = data[:,1]
    z = data[:,2]
    return x,y,z
    
def make_planets(model = 'verlet'):
    if type(model) == str:
        pass
    elif model in range(['verlet','euler']):
        pass
    else:
        print('please enter the model as a string')
        input('verlet or euler: ')
        
    names = ['sun','mercury', 'venus', 'earth', 'mars', 'jupiter', 'saturn', 'uranus', 'neptune']
    mass = [Ms,.06, .82, 1, .11, 317.8, 95.2, 14.6, 17.2] #w.r.t earth mass
    location = [np.array([3.05*10**(-3),4.63*10**(-3),-1.49*10**(-4)]),
                np.array([-.391,-.107,.0269]),
                np.array([-.555,-.455,.0257]),
                np.array([-.899,-.435,-1.29*10**(-4)]),
                np.array([.396,1.49,.0212]),
                np.array([-5.17,-1.74,.123]),
                np.array([-1.32,-9.96,.226]),
                np.array([18.2,8.19,-.205]),
                np.array([28.4,-9.38,-.462])]
    velocity = [np.array([-3.73*10**(-6),6.49*10**(-6),8.37*10**(-8)]),
                np.array([1.82*10**-3,-2.59*10**-2,-2.28*10**-3]),
                np.array([1.27*10**-2,-1.57*10**-2,-9.49*10**-4]),
                np.array([7.24*10**-3,-1.55*10**-2,8.64*10**-7]),
                np.array([-1.30*10**-2,4.79*10**-3,4.19*10**-4]),
                np.array([2.32*10**-3,-6.79*10**-3,-2.36*10**-5]),
                np.array([5.23*10**-3,-7.50*10**-4,-1.95*10**-4]),
                np.array([-1.64*10**-3,3.40*10**-3,3.38*10**-5]),
                np.array([9.62*10**-4,3.00*10**-3,-8.38*10**-5])] #in AU/day
    period = [0,.24,.62,1,1.88,11.86,29.46,84.01,164.8] #years
    eccentricity = [0,.206,.007,.017,.093,.048,.054,.047,.009]    
    planets = []
    for i in np.arange(0,len(names)):
        planets.append(pc.planet())
        planets[i].name = names[i]
        planets[i].mass = mass[i]
        planets[i].pos = location[i]
        if i == 0:
            continue
        else:
            planets[i].vel = velocity[i] * 365
    return planets
    
def acc_update(planet_list,planet='all'):
    planets = planet_list
    accel = 0
    accell = 0
    if planet=='all':
        for i in np.arange(len(planets)):
            for j in np.arange(len(planets)):
                if i == j:
                    continue
                else:
                    accel += acc(planets[j].pos,planets[i].pos, planets[j].mass)
            planets[i].acc = accel
    else:
        for i in np.arange(len(planets)):
            if planets[i].name == planet:
                place = i
            else:
                continue
        for j in np.arange(len(planets)):
            if j == place:
                continue
            else:
                accell += acc(planets[j].pos,planets[place].pos,planets[j].mass)
        planets[place].acc = accell

def plot():
    planets = make_planets()
    for i in np.arange(len(planets)):
        x,y,z = load_data(planets[i].name)
        plt.figure('Verlet Method')
        #plt.xlim([-30,30])
        #plt.ylim([-30,30])
        plt.hold(True)
        plt.plot(x,y,label=planets[i].name)
        plt.xlabel('x-pos [AU]')
        plt.ylabel('y-pos [AU]')
        plt.legend()
        plt.title('Planetary Orbits From Verlet Integration')
    plt.show()
    
def SS_verlet(V0 = 2*np.pi, years = 1):
    N = 365 * years
    dt = 1/365
    planets = make_planets()
    acc_update(planets)
    for t in np.arange(N):
        for i in np.arange(len(planets)):
            planets[i].update()
            planets[i].pos = planets[i].pos_old + planets[i].vel_old * dt + 1/2 * dt**2 * planets[i].acc_old
            acc_update(planets,planet=planets[i].name)
            planets[i].vel = planets[i].vel_old + 1/2*(planets[i].acc_old + planets[i].acc) * dt
            if (t % N/10) % 1 == 0:
                planets[i].output()
            else:
                pass    

