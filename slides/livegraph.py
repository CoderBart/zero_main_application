﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pi3d
import sys,os
from _thread import start_new_thread
import time


import numpy as np
import math

sys.path.insert(1, os.path.join(sys.path[0], '..'))

import config
import core.graphics as graphics
import core.peripherals as peripherals
import core.MinGraph as MinGraph


text = pi3d.PointText(graphics.pointFont, graphics.CAMERA, max_chars=500, point_size=128) 

#matsh = pi3d.Shader("mat_flat")

x_vals = np.linspace(0, 780, 780)
nextsensorcheck = time.time()

showvars = ['atmega_temp','mlxamb','mlxobj','sht_temp','act_temp','gputemp','cputemp']

if hasattr(peripherals.eg_object,'bmp280_temp'):
   showvars.append('bmp280_temp')


colors = [(1,0,0,1,1),
         (0,0.5,0,1,1),
         (0,0,1,1,1),
         (0.5,1,0.3,1,1),
         (1,0.3,0.7,1,2),
         (0,0.7,0.3,1,1),
         (0,0,0.5,1,1),
         (1,1,0.3,1,1)]


y_vals = np.zeros((len(showvars),780))


graph = MinGraph.MinGraph(x_vals, y_vals, 780, 460, 
              line_width=1,camera=graphics.CAMERA,shader=graphics.MATSH,colorarray=colors, xpos=0, ypos=0 , z = 1.0, ymax=50,ymin=10)


i = 0

for varname in showvars:

 legend = pi3d.TextBlock(-340, (200 - (i * 30)), 0.1, 0.0, 30, data_obj=peripherals.eg_object,text_format= varname + "  {:2.1f}", attr=varname,size=0.3, spacing="C", space=1.1, colour=colors[i])
 text.add_text_block(legend)
 i += 1

grapharea = pi3d.Sprite(camera=graphics.CAMERA,w=780,h=460,z=3.0, x =0, y = 0)
grapharea.set_shader(graphics.MATSH)
grapharea.set_material((1.0, 1.0, 1.0))
grapharea.set_alpha(0.6)


def inloop(textchange = False,activity = False, offset = 0):
     global nextsensorcheck 

     if (time.time() > nextsensorcheck) and offset == 0 and peripherals.touched() == False:
        peripherals.get_sensors()
        peripherals.get_infrared()
        nextsensorcheck = time.time() + 0.1
        text.regen()
        i = 0
        for varname  in showvars:
            y_vals[i][:-1] = y_vals[i][1:]
            y_vals[i][-1] =  getattr(peripherals.eg_object,varname)
            i += 1
        graph.update(y_vals)

     grapharea.draw()

     if offset != 0:
         #graphics.slider_change(graph, offset)
         offset = graphics.slider_change(text.text, offset)
     else:    
         graph.draw()
     text.draw()        
     return activity,offset



















