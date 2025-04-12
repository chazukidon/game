import pyxel
import sys
import numpy as np

sys.setrecursionlimit(10**6)

class Field:
    def __init__(self,field_width,field_height):

        self.field_width=field_width
        self.field_height=field_height
        self.field_size=16
 
        self.field=np.ones((self.field_height,self.field_width),dtype=int)
        self.around_idx=np.array([[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]])
        self.dig_history=np.array([],dtype=int)
        self.mines_have_idx=np.array([],dtype=int)
        self.flag_idx=np.array([],dtype=int)

    def output_around_mines_pcs(self,sch_idx):
        return sum([1 for idx in self.around_idx if 0<=idx[0]+sch_idx[0]<self.field_height and  0<=idx[1]+sch_idx[1]<self.field_width and self.field[tuple(idx+sch_idx)]==2])

    def dig(self,sch_idx):
        self.field[tuple(sch_idx)]=0
        around_pcs=self.output_around_mines_pcs(sch_idx)
        if around_pcs==0:
            for idx in self.around_idx:
                if 0<=idx[0]+sch_idx[0]<self.field_height and  0<=idx[1]+sch_idx[1]<self.field_width and (idx+sch_idx)[0]*self.field_width+(idx+sch_idx)[1] not in self.dig_history:
                    self.dig_history=np.append(self.dig_history,(idx+sch_idx)[0]*self.field_width+(idx+sch_idx)[1])
                    self.dig(idx+sch_idx)
        else:
            self.mines_have_idx=np.append(self.mines_have_idx,sch_idx[0]*self.field_width+sch_idx[1])

class App(Field):
    
    def __init__(self,mines_n):

        self.field_x=(pyxel.width-self.field_width*self.field_size-70)//2
        self.field_y=(pyxel.height-self.field_height*self.field_size)//2
        self.pause=False
        self.gameclear=False
        self.gameover=False
        self.text_color=0
        self.pit_color=6
        self.line_color=12
        self.mines_n=mines_n
        self.flag_n=self.mines_n
        self.play_time=0
        self.m='0'
        self.s='0'
        self.ms='0'
        
    
    def mouse_event(self):
        
        x=(pyxel.mouse_x-self.field_x)//self.field_size
        y=(pyxel.mouse_y-self.field_y)//self.field_size
        order_idx=int(y*self.field_width+x)
        
        if 0<=x<self.field_width and 0<=y<self.field_height:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) and order_idx not in self.flag_idx:
            
            
                if self.field[y,x]==2:
                    self.gameover=True 
                else:
                    if np.count_nonzero(self.field)==self.field_width*self.field_height :
                        self.mines_idx=np.array([[i//self.field_width,i%self.field_width] for i in np.random.choice([i for i in range(0,self.field_width*self.field_height) if  i not in [order_idx]+[order_idx%self.field_width+j[1]+(order_idx//self.field_width+j[0])*self.field_width for j in self.around_idx if 0<=order_idx%self.field_width+j[1]<self.field_width and 0<=order_idx//self.field_width+j[0]<self.field_height]],self.mines_n,replace=False)])
                        for idx in self.mines_idx:
                            self.field[tuple(idx)]=2
                        self.play_time=0
                    self.dig(np.array([y,x]))
                    
            elif pyxel.btnp(pyxel.MOUSE_BUTTON_RIGHT):
                if order_idx not in self.flag_idx:
                    if self.field[y,x]!=0:
                        self.flag_idx=np.append(self.flag_idx,order_idx)
                        self.flag_n-=1
                else:
                    self.flag_idx=self.flag_idx[self.flag_idx!=order_idx]
                    self.flag_n+=1
        if pyxel.btnp(pyxel.MOUSE_BUTTON_MIDDLE):
            self.pause=True
            
    def draw_field(self):
        pyxel.cls(7)
        for y in range(self.field_height):
            for x in range(self.field_width):
                if self.field[y,x]==0:
                    if y*self.field_width+x in self.mines_have_idx:
                        pyxel.text(self.field_size//2-1+x*self.field_size+self.field_x,self.field_size//2-2+y*self.field_size+self.field_y,str(self.output_around_mines_pcs(np.array([y,x]))),self.text_color)
                    else:
                        pyxel.rect(x*self.field_size+self.field_x,y*self.field_size+self.field_y,self.field_size,self.field_size,self.pit_color)
                if y*self.field_width+x in self.flag_idx:
                    pyxel.blt(x*self.field_size+self.field_x, y*self.field_size+self.field_y, 0, 0, 0, 16, 16, 0)
    def draw_line(self):            
        for x in range(self.field_width+1):  
            pyxel.line(x*self.field_size+self.field_x,self.field_y,x*self.field_size+self.field_x,self.field_height*self.field_size+self.field_y,self.line_color)
        for y in range(self.field_height+1):
            pyxel.line(self.field_x,y*self.field_size+self.field_y,self.field_width*self.field_size+self.field_x,y*self.field_size+self.field_y,self.line_color)
        pyxel.line(self.field_width*self.field_size+self.field_x*2,0,self.field_width*self.field_size+self.field_x*2,pyxel.height,0)
    def draw_menu(self):
        pyxel.cls(7)
        pyxel.text(pyxel.width//2-40,pyxel.height//2-30,'Press E:easy mode',0)
        pyxel.text(pyxel.width//2-40,pyxel.height//2,'Press M:middle mode',0)
        pyxel.text(pyxel.width//2-40,pyxel.height//2+30,'Press H:hard mode',0)
    def draw_gameclear(self):
        self.text_color=0
        self.pit_color=10
        self.line_color=12
        self.draw_field()
        self.draw_line()
        pyxel.text(self.field_width*self.field_size+self.field_x*2+13,10,'GAME CLEAR!!',0)
    def draw_gameover(self):

            self.text_color=0
            self.pit_color=14
            self.line_color=15
            self.draw_field()
            for y,x in self.mines_idx:
                if self.field[y,x]==2:
                    pyxel.blt(x*self.field_size+self.field_x, y*self.field_size+self.field_y, 0, [16,32,48][(y+x)%3], 0, 16, 16,0)
            self.draw_line()
            pyxel.text(self.field_width*self.field_size+self.field_x*2+17,10,'GAME OVER',0)

    def draw_pause(self):
            self.text_color=13
            self.pit_color=7
            self.line_color=13
            self.draw_field()

            for y in range(self.field_height):
                for x in range(self.field_width):
                    if y*self.field_width+x in  self.flag_idx:
                        pyxel.blt(x*self.field_size+self.field_x, y*self.field_size+self.field_y, 0, 0, 16, 16, 16, 0)
            self.draw_line()
            pyxel.text(self.field_width*self.field_size+self.field_x*2+25,10,'pause',0)
            pyxel.blt(self.field_width*self.field_size+self.field_x*2+15, pyxel.height-12, 0, 24, 16, 8, 8, 0)
            
            pyxel.text(self.field_width*self.field_size+self.field_x*2+30,pyxel.height-10,str(self.flag_n),0)
            pyxel.text(self.field_width*self.field_size+self.field_x*2+10,pyxel.height-20,'time',0)

            pyxel.text(self.field_width*self.field_size+self.field_x*2+30,pyxel.height-20,(2-len(self.m))*'0'+self.m+':'+(2-len(self.s))*'0'+self.s+':'+(2-len(self.ms))*'0'+self.ms,0)

    
    def draw_info(self):
        pyxel.blt(self.field_width*self.field_size+self.field_x*2+15, pyxel.height-12, 0, 16, 16, 8, 8, 0)
        pyxel.text(self.field_width*self.field_size+self.field_x*2+30,pyxel.height-10,str(self.flag_n),0)
        pyxel.text(self.field_width*self.field_size+self.field_x*2+10,pyxel.height-20,'time',0)
        pyxel.text(self.field_width*self.field_size+self.field_x*2+30,pyxel.height-20,(2-len(self.m))*'0'+self.m+':'+(2-len(self.s))*'0'+self.s+':'+(2-len(self.ms))*'0'+self.ms,0)



    
class Play(App):
    def __init__(self):

        self.menu=True
        pyxel.init(560,314,fps=100)

        pyxel.load('sample.pyxres')
        pyxel.mouse(True)
        
        pyxel.run(self.update,self.draw)

    def update(self):
        if self.menu:
            if pyxel.btnp(pyxel.KEY_E):
                Field.__init__(self,9,9)
                App.__init__(self,10)
                self.menu=False
            elif  pyxel.btnp(pyxel.KEY_M):
                Field.__init__(self,16,16)
                App.__init__(self,40)
                self.menu=False
            elif pyxel.btnp(pyxel.KEY_H):
                Field.__init__(self,30,19)
                App.__init__(self,99)
                self.menu=False

        else:
            for idx in self.flag_idx:
                if self.field[idx//self.field_width,idx%self.field_width]==0:
                    self.flag_idx=self.flag_idx[self.flag_idx!=idx]
                    self.flag_n+=1 

            if self.pause:
                if pyxel.btnp(pyxel.MOUSE_BUTTON_MIDDLE):
                    self.pause=False
                    self.text_color=0
                    self.pit_color=6
                    self.line_color=12
                
            elif self.gameover is False and self.gameclear is False:

                self.mouse_event()
                if np.count_nonzero(self.field)==self.mines_n:
                    self.gameclear=True
                elif np.size(np.where(self.field==1))//2!=self.field_width*self.field_height:
                    self.play_time+=1
                    self.m=str((self.play_time//100)//60)
                    self.s=str((self.play_time//100)%60)
                    self.ms=str(self.play_time%100)
        
            if pyxel.btnp(pyxel.KEY_R):
                self.menu=True
                
        
    def draw(self):
        if self.menu:
            self.draw_menu()
        elif self.gameover:
            self.draw_gameover()
            self.draw_info()
        elif self.gameclear:
            self.draw_gameclear()
            self.draw_info()
        elif self.pause:
            self.draw_pause()
        
        else:
            self.draw_field()
            self.draw_line()
            self.draw_info()
Play()