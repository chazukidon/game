# -*- coding: utf-8 -*-

import pyxel

class APP:
  def __init__(self):
      pyxel.init(128, 128, title="pyxel",fps=60)
      
      pyxel.load('my_resource.pyxres')
      self.x,self.y=0,50
      self.direction=[0,0]
      pyxel.run(self.update, self.draw)
     
  def update(self):
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x+=1
            self.direction=[8,0]
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x-=1
            self.direction=[0,0]

  def draw(self):
      pyxel.cls(0)

      pyxel.blt(self.x, self.y, 0, self.direction[0], self.direction[1], 8, 8, 0)
      
      
      
APP()
