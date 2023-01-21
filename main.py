import random
import math
import sys
import pygame
import os

window_width=600
window_height=200

pygame.init()
window=pygame.display.set_mode((window_width,window_height))
pygame.display.set_caption("DINO")

class BG:
    def __init__(self,x):
        self.width=window_width
        self.height=window_height
        self.x=x
        self.y=0
        self.set_texture()
        self.bg_show()
    
    def set_texture(self):
        bg_path=os.path.join("assets/images/bg.png")
        self.texture=pygame.image.load(bg_path)
        self.texture=pygame.transform.scale(self.texture,(self.width,self.height))
    
    def bg_show(self):
        window.blit(self.texture,(self.x,self.y))

    def update_screen(self,dx):
        self.x+=dx
        if self.x<=-window_width:
            self.x=window_width

class DINO:
    def __init__(self):
        self.width=40
        self.height=40
        self.x=25
        self.y=125
        self.texture_num=0
        self.dy=0.5
        self.gravity=1
        self.jumping=False
        self.jump_pos=40
        self.falling=False
        self.fall_pos=self.y
        self.on_ground=True
        self.set_texture()
        self.dino_show()
    
    def set_texture(self):
        dino_path=os.path.join(f"assets/images/dino{self.texture_num}.png")
        self.texture=pygame.image.load(dino_path)
        self.texture=pygame.transform.scale(self.texture,(self.width,self.height))
    
    def dino_show(self):
        window.blit(self.texture,(self.x,self.y))
    
    def update(self,loop):
        #jumping
        if self.jumping:
            self.y-=self.dy
            if self.y<=self.jump_pos:
                self.fall()
        #falling
        elif self.falling:
            self.y+=self.gravity*self.dy
            if self.y>=self.fall_pos:
                self.stop()
        #walking
        elif self.on_ground and loop%70==0:
            self.texture_num=(self.texture_num+1) % 3
            self.set_texture()
    
    def jump(self):
        self.jumping=True
        self.on_ground=False
    
    def fall(self):
        self.falling=True
        self.jumping=False
    
    def stop(self):
        self.falling=False
        self.on_ground=True

class CACTUS:
    def __init__(self,x):
        self.width=40
        self.height=40
        self.x=x
        self.y=125
        self.set_texture()
        self.cactus_show()

    def set_texture(self):
        cactus_path=os.path.join("assets/images/cactus.png")
        self.texture=pygame.image.load(cactus_path)
        self.texture=pygame.transform.scale(self.texture,(self.width,self.height))
    
    def cactus_show(self):
        window.blit(self.texture,(self.x,self.y))

    def update(self,dx):
        self.x+=dx

class COLLISION:
    def check_collision(self,dino_obj,cactus_obj):
        dist=math.sqrt((dino_obj.x-cactus_obj.x)**2 + (dino_obj.y-cactus_obj.y)**2)
        return dist<30

class SCORE:
    def __init__(self,hs):
        self.hs=hs
        self.act_s=0
        self.font=pygame.font.SysFont('monospace',20)
        self.color=(0,0,0)
        self.score_show()

    def score_show(self):
        self.label=self.font.render(f'HI:{self.hs} {self.act_s}',True,self.color)
        label_width=self.label.get_rect().width
        window.blit(self.label,(window_width-label_width-20,10))

    def check_hs(self):
        if self.act_s>=self.hs:
            self.hs=self.act_s

    def update(self,loop):
        self.act_s=loop//70
        self.check_hs( )

    def reset_score(self):
        self.act_s=0

class GAME:
    def __init__(self,hs=0):
        self.bg=[BG(0),BG(window_width )]
        self.dino=DINO()
        self.collision=COLLISION()
        self.score=SCORE(hs)
        self.obstacles=[]
        self.dx=0.35
        self.playing=False
    
    def game_start(self):
        self.playing=True

    def game_over(self):
        self.playing=False

    def spawn_cactus(self):
        
        #list with obstacles
        
        if len(self.obstacles)>0:
            prev_obstacle=self.obstacles[-1]
            x=random.randint(int(prev_obstacle.x)+40+80 , window_width+int(prev_obstacle.x)+40+80)
       
        #empty list
        
        else:
            x=random.randint(window_width+100,1000)
       
        #append the new cactus
        
        cactus=CACTUS(x)
        self.obstacles.append(cactus)
    
    def spawn_check(self,loop):
        return loop % 50==0

    def restart(self):
        self.__init__(hs=self.score.hs)

def main():

    game=GAME()
    dino=game.dino

    loop=0
    clock=pygame.time.Clock()

    while True:

        if game.playing:

            loop+=1

    #------------------------------------------------------------
            for bg in game.bg:
                bg.update_screen(-game.dx)
                bg.bg_show()
    #-----------------------------------------------------------        
            dino.update(loop)
            dino.dino_show()
    #------------------------------------------------------------
            if game.spawn_check(loop):
                game.spawn_cactus()
            
            for cactus in game.obstacles:
                cactus.update(-game.dx)
                cactus.cactus_show()

                #COLLISION
                if game.collision.check_collision(dino,cactus):
                    game.game_over()
    #------------------------------------------------------------
            game.score.update(loop)
            game.score.score_show()
    #----------------------------------------------------------
    
        for event in  pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.KEYDOWN:
                if event.key==pygame.K_SPACE:
                    if dino.on_ground:
                        dino.jump()
                    if not game.playing:
                        game.game_start()
                if event.key==pygame.K_r:
                    game.restart()
                    dino=game.dino
                    loop=0

        clock.tick(5000)        
        pygame.display.update()

main()
