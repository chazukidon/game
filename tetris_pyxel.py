import pyxel 
import numpy as np
import PyxelUniversalFont as puf
        
        
class Tetorimino:
    def __init__(self,field,score,erase_column_n):
        self.field=field
        self.field_x=self.field.shape[1]
        self.field_y=self.field.shape[0]
        self.score=score
        self.erase_column_n=erase_column_n
        self.erase_column=[]
        self.tetorimino_size=30
        #z,s,o,i,l,j,t
        self.tetoriminos=[([0,0,1,1],[0,1,1,2]),
                          ([0,0,1,1],[1,2,1,0]),
                          ([0,0,1,1],[0,1,0,1]),
                          ([0,0,0,0],[0,1,2,3]),
                          ([0,1,1,1],[0,0,1,2]),
                          ([0,1,1,1],[2,2,1,0]),
                          ([0,1,1,1],[1,0,1,2])]
        
        
        if np.count_nonzero(self.field)==0:
            self.tetorimino_type=np.random.randint(0,7)
            self.next_tetorimino_type=np.random.randint(0,7)
        else:
            self.tetorimino_type=self.next_tetorimino_type
            self.next_tetorimino_type=np.random.randint(0,7)
            
        self.tetorimino_color_codes=[8,11,10,6,9,5,2]
        self.tetorimino=self.tetoriminos[self.tetorimino_type]
        self.tetorimino_x=3
        self.tetorimino_y=0
        self.fall_speed=48
        self.moving=True
        self.falling_pause=False
        self.movable_count=0
        
    def rotation(self):
            
        if pyxel.btnp(pyxel.KEY_SPACE):
            
            tetorimino=list(max(self.tetorimino[1])-np.array(self.tetorimino[1])),self.tetorimino[0]
            if 9<max(tetorimino[1])+self.tetorimino_x:
                self.tetorimino_x-=max(tetorimino[1])+self.tetorimino_x-self.field_x+1
        
            if 19<max(tetorimino[0])+self.tetorimino_y:
                self.tetorimino_y-=max(tetorimino[0])+self.tetorimino_y-self.field_y+1

            shift_candidate=[(0,0),(0,1),(0,-1),(-1,0),(1,0)]
            for x,y in shift_candidate:
                tetorimino=np.array(tetorimino[0])+y,np.array(tetorimino[1])+x
                if max(tetorimino[1])+self.tetorimino_x<=self.field_x-1 and max(tetorimino[0])+self.tetorimino_y<=self.field_y-1 and all(0 ==self.field[np.array(tetorimino[0])+self.tetorimino_y,np.array(tetorimino[1])+self.tetorimino_x]):
                    self.tetorimino=tetorimino
                    return

            
    def fall(self):
        if pyxel.frame_count%self.fall_speed==0 and max(self.tetorimino[0])+self.tetorimino_y<=self.field_y-2 and all(0 ==self.field[np.array(self.tetorimino[0])+self.tetorimino_y+1,np.array(self.tetorimino[1])+self.tetorimino_x]):
            self.tetorimino_y+=1
        
    def move(self):
        
        if pyxel.btn(pyxel.KEY_DOWN):
            while max(self.tetorimino[0])+self.tetorimino_y<=self.field_y-2 and all(0 ==self.field[np.array(self.tetorimino[0])+self.tetorimino_y+1,np.array(self.tetorimino[1])+self.tetorimino_x]):
                    self.tetorimino_y+=1
                    self.score+=1
                
        if 0!=self.tetorimino_x and pyxel.btnp(pyxel.KEY_LEFT,10,2) and all(0 ==self.field[np.array(self.tetorimino[0])+self.tetorimino_y,np.array(self.tetorimino[1])+self.tetorimino_x-1]):
            self.tetorimino_x-=1
        if max(self.tetorimino[1])+self.tetorimino_x!=self.field_x-1 and pyxel.btnp(pyxel.KEY_RIGHT,10,2) and all(0 ==self.field[np.array(self.tetorimino[0])+self.tetorimino_y,np.array(self.tetorimino[1])+self.tetorimino_x+1]):
            self.tetorimino_x+=1
    
    def erase(self):
        self.erase_column=[i for i in range(self.field_y) if np.count_nonzero(self.field[i])==self.field_x]
        self.erase_column_n+=len(self.erase_column)

        if len(self.erase_column)!=0:

            self.field=np.delete(self.field,self.erase_column,0)
            self.field=np.append([[0]*self.field_x]*len(self.erase_column),self.field,axis=0)

     
    def tetorimino_addition(self):
        self.field[np.array(self.tetorimino[0])+self.tetorimino_y,np.array(self.tetorimino[1])+self.tetorimino_x]=self.tetorimino_color_codes[self.tetorimino_type]



class App(Tetorimino):
    def __init__(self):
        self.gameover=False
        self.pause=False
        self.time=0

    
    def game_judge(self):
       if np.count_nonzero(self.field[1])!=0:
           
           self.pause=False
           self.gameover=True
        
    def moving_judge(self):
        
        if self.falling_pause and self.movable_count==10:
            self.moving=False
        else:
            for i in range(4):
                
                if self.tetorimino[0][i]+self.tetorimino_y==self.field_y-1 or  self.field[self.tetorimino[0][i]+self.tetorimino_y+1,self.tetorimino[1][i]+self.tetorimino_x]!=0:
                    self.falling_pause=True
                    self.movable_count+=1
                    return
            self.falling_pause=False
            self.movable_count=0
    
    def home_draw(self):
        pyxel.cls(0)
        writer = puf.Writer("misaki_gothic.ttf")
        tetris='TETRIS'
        if pyxel.frame_count==0:
            self.tetris_color_code=np.array([8,9,10,11,6,2])
            
        elif pyxel.frame_count%50==0:
            self.tetris_color_code= np.roll(self.tetris_color_code, 1)
        # else:
           


        for i in range(6):
            writer.draw(120+i*35, 220, tetris[i],70, self.tetris_color_code[i])
        writer.draw(145, 500,'PRESS S TO START',20 , 13)

    def pause_draw(self):
        pyxel.cls(0)
        writer = puf.Writer("misaki_gothic.ttf")
        writer.draw(130, 200, "Pause", 70, 3)
        writer.draw(185, 320, "Lv:"+str(self.erase_column_n//10+1), 30, 5)
        writer.draw(140, 370, "SCORE:"+str(self.score), 30, 5)
        writer.draw(155, 420, "TIME:{0}:{1}:{2}".format((self.time//60)//60,(self.time//60)%60,self.time%60), 30, 5)
    
    def gameover_draw(self):
        pyxel.cls(0)
        writer = puf.Writer("misaki_gothic.ttf")
        writer.draw(110, 200, "GAME OVER", 50, 8)
        writer.draw(185, 320, "Lv:"+str(self.erase_column_n//10+1), 30, 5)
        writer.draw(140, 370, "SCORE:"+str(self.score), 30, 5)
        writer.draw(155, 420, "TIME:{0}:{1}:{2}".format((self.time//60)//60,(self.time//60)%60,self.time%60), 30, 5)
    
    
    
    def field_draw(self):
        for i in range(self.field_y-20,self.field_y):
            for j in range(self.field_x):
                if self.field[i,j]!=0:
                    pyxel.rect(j*self.tetorimino_size,(i-(self.field_y-20))*self.tetorimino_size,self.tetorimino_size,self.tetorimino_size,self.field[i,j])
    def tetorimino_draw(self):
        for i in range(4):
            pyxel.rect((self.tetorimino[1][i]+self.tetorimino_x)*self.tetorimino_size,(self.tetorimino[0][i]+self.tetorimino_y-(self.field_y-20))*self.tetorimino_size,self.tetorimino_size,self.tetorimino_size,self.tetorimino_color_codes[self.tetorimino_type])
    def fall_draw(self):
        tetorimino_y=self.tetorimino_y
        while max(self.tetorimino[0])+tetorimino_y<=self.field_y-2 and all(0 ==self.field[np.array(self.tetorimino[0])+tetorimino_y+1,np.array(self.tetorimino[1])+self.tetorimino_x]):
            tetorimino_y+=1
        if tetorimino_y>self.tetorimino_y+max(self.tetorimino[0]):
            for i in range(4):
                pyxel.rectb((self.tetorimino[1][i]+self.tetorimino_x)*self.tetorimino_size,(self.tetorimino[0][i]+tetorimino_y-(self.field_y-20))*self.tetorimino_size,self.tetorimino_size,self.tetorimino_size,self.tetorimino_color_codes[self.tetorimino_type])
    
    def line_draw(self):
        for i in range(10):
            pyxel.line(i*self.tetorimino_size,0,i*self.tetorimino_size,600,0)
        for j in range(20):
            pyxel.line(0,j*self.tetorimino_size,300,j*self.tetorimino_size,0)   

        
    def info_draw(self):

        next_tetorimino=self.tetoriminos[self.next_tetorimino_type]
        frame_width=120
        frame_height=90
        flame_x=(pyxel.width-300-frame_width)//2
        flame_y=40
        next_tetorimino_size=25
        next_tetorimino_x=(frame_width-(max(next_tetorimino[1])+1)*next_tetorimino_size)//2+flame_x+300
        next_tetorimino_y=(frame_height-(max(next_tetorimino[0])+1)*next_tetorimino_size)//2+flame_y
        for i in range(4):
            pyxel.rect(next_tetorimino[1][i]*next_tetorimino_size+next_tetorimino_x,next_tetorimino[0][i]*next_tetorimino_size+next_tetorimino_y,next_tetorimino_size,next_tetorimino_size,self.tetorimino_color_codes[self.next_tetorimino_type])
        for i in range(max(next_tetorimino[0])+2):
            pyxel.line(300,next_tetorimino_y+i*next_tetorimino_size,pyxel.width,next_tetorimino_y+i*next_tetorimino_size,0)
        for i in range(max(next_tetorimino[1])+2):
            pyxel.line(next_tetorimino_x+i*next_tetorimino_size,0,next_tetorimino_x+i*next_tetorimino_size,pyxel.height,0)
        pyxel.rectb(300+flame_x,flame_y,frame_width,frame_height,7) 
        pyxel.line(300,0,300,600,7)

        writer = puf.Writer("misaki_gothic.ttf")
        writer.draw(300+flame_x, flame_y-18, "NEXT", 18, 13)
        
        writer.draw(320, 450, "Lv:"+str(self.erase_column_n//10+1), 20, 3)
        writer.draw(320, 550, "TIME:{0}:{1}:{2}".format((self.time//60)//60,(self.time//60)%60,self.time%60), 20, 3)
        writer.draw(320, 500, "SCORE:"+str(self.score), 20, 3)
        
class Game(App):
    def __init__(self): 
        pyxel.init(450,600,fps=60)
        App.__init__(self)
        Tetorimino.__init__(self,np.zeros((22,10),dtype=int),0,0)
        self.game_progress=False
        pyxel.run(self.update,self.draw)


    def update(self):
        if self.game_progress:
            if self.gameover is False and pyxel.btnp(pyxel.KEY_UP):
                    self.pause=not self.pause
            if self.pause is False:
            
                if self.gameover and  pyxel.btnp(pyxel.KEY_R):
                    self.gameover=False
                    Tetorimino.__init__(self,np.zeros((self.field_y,self.field_x),dtype=int),0,0)
                    App.__init__(self)
                
                elif self.gameover is False:
                    self.time+=1

                    if self.moving:
                        self.fall()
                        self.move()
                        self.rotation()
                        self.erase()
                        if len(self.erase_column)!=0:
                            score_board=[100,300,500,800]
                            self.score+=score_board[len(self.erase_column)-1]
                        self.fall_speed=max(48-5*(self.erase_column_n//10),5)
                        self.moving_judge()
                    else:
                        self.game_judge()
                        self.tetorimino_addition()
                        Tetorimino.__init__(self,self.field,self.score,self.erase_column_n)
        elif pyxel.btnp(pyxel.KEY_S):
            self.game_progress=True
            
    def draw(self): 
        
        if self.game_progress is False:
            self.home_draw()
        elif self.gameover:
            self.gameover_draw()
            
        elif self.pause:
            self.pause_draw()
        else:
            pyxel.cls(0)
            self.field_draw()

            self.tetorimino_draw()
            self.line_draw()     
            self.fall_draw()
            self.info_draw()
Game()