import queue
import numpy as np
import pyxel
#飽きた
class Maze:
    def __init__(self):
        
        self.maze_size=3
        self.maze_height,self.maze_width=43,43
        self.maze=np.ones((self.maze_height,self.maze_width))
        self.sch_candidate=queue.Queue()
        self.dig_history=np.array([])
        
    def output_dig_candidate(self,dig_idx):
        dig_direciton_candidate=np.array([[-2,0],[0,-2],[0,2],[2,0]])
        np.random.shuffle(dig_direciton_candidate)
        dig_candidate=[]
        for i in dig_direciton_candidate:
            idx=i+dig_idx
            if 0<=idx[0]<self.maze_height and 0<=idx[1]<self.maze_width and self.maze[tuple(idx)]==1:
                dig_candidate.append(np.array([i//2+dig_idx,idx]))
        
        return dig_candidate

    def dig(self,dig_idx):
        candidiate=self.output_dig_candidate(dig_idx)
        for idx in candidiate:
            history_append_idx=idx[1,0]*self.maze_width+idx[1,1]
            
            if np.size(np.where(self.dig_history==history_append_idx))==0:
                for i in idx:
                    self.maze[tuple(i)]=0
            
                self.dig_history=np.append(self.dig_history,history_append_idx)
                self.dig(idx[1])

    def make_maze(self):
        if np.count_nonzero(self.maze)==self.maze_width*self.maze_height:
            dig_idx=np.array([np.random.choice(list(range(1,self.maze_height,2))),np.random.choice(list(range(1,self.maze_width,2)))])
            self.maze[tuple(dig_idx)]=0
            self.dig(dig_idx)
            self.output_sch_candidate(np.array([1,1]))
    
    def draw_maze(self):
        for y in range(self.maze_height):
            for x in range(self.maze_width):
                if self.maze[x,y]==0:
                    pyxel.rect(x*self.maze_size,y*self.maze_size,self.maze_size,self.maze_size,7)

    
    def output_sch_candidate(self,sch_idx):
        sch_direciton_candidate=np.array([[-1,0],[0,-1],[0,1],[1,0]])
        for i in sch_direciton_candidate:
            idx=i+sch_idx
            if 0<idx[0]<self.maze_height and 0<idx[1]<self.maze_width and  self.maze[tuple(idx)]==0:
                self.sch_candidate.put(idx)
        # print(self.sch_candidate.qsize())
        # print(self.sch_candidate.get())
        # print(self.sch_candidate.qsize())
    def solve_maze(self,sch_idx):
        if np.all(sch_idx==)
        if  self.sch_candidate.empty() is False:
            next_sch_idx=self.sch_candidate.get()
            

class Player:
    def __init__(self):
        pass



class Game(Maze):
    def __init__(self):
        Maze.__init__(self)
        pyxel.init(129,129,fps=60)
        pyxel.run(self.update,self.draw)
        
    def update(self):
        self.make_maze()
        if pyxel.btnp(pyxel.KEY_SPACE):
            Maze.__init__(self)  
    def draw(self):
        pyxel.cls(0)
        self.draw_maze()

        # pyxel.text(50,10,'GAME CLEAR!!!',3)
        # pyxel.text(51,10,'GAME CLEAR!!!',7)

Game()