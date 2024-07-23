#player1
from threading import Thread
import sys,time,socket
import pygame
import re

pygame.init()
pygame.mixer.init()
class rungame:
    def __init__(self):

        #self.sound=pygame.mixer.music.load('C:/Users/MAC/AppData/Roaming/Sublime Text/Linjinrongdage/pygame/lu.wav')
        self.end=False
        self.endre=re.compile(r'type(\w)*')
        self.start1=False

        self.start2=False
        self.start2re=re.compile(r'start2True')
        self.startre=re.compile(r'start2(\w)*')
        self.screen=pygame.display.set_mode((800,800))#,pygame.FULLSCREEN)
        self.setting=setting()
        self.player1=player1(self)
        self.player2=player2(self)
        self.white=(255,255,255)
        self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.client=None
        self.address=None
        self.handout2re=re.compile(r'handout2(True|False)')
        self.handoutcontrol=False
        self.handoutstart=None
        self.handoutend=None
        # self.recvallb=recvallb()
        #bleed
        self.bleed=bleed(self)
        self.bleed1re=re.compile(r'bleed1(\d)*')
        self.bleed2re=re.compile(r'bleed2(\d)*')
        #hand
        self.handout1=handout1(self)
        self.handout2=handout2(self)
        #
        self.player1group=pygame.sprite.Group()
        self.player2group=pygame.sprite.Group()
        self.player1handgroup=pygame.sprite.Group()
        self.player2handgroup=pygame.sprite.Group()
        #
        self.button=Button(self)
        #
        self.zobi=False
        self.a=False
        self.mousepos=None
        self.zobi=False
        self.rezobi01=re.compile(r'zobi01(\w)*')
        self.rezobi11=re.compile(r'zobi11(\d)*')
        self.rezobi21=re.compile(r'zobi21(\d)*')
        pygame.display.set_caption("MINE")
    def run_game(self):
        self.sockbind()
        self.controlsprite()
        while True:
            self.sockserverrun()
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                    #self.socketserverpygame.sock.close()
                if event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_RIGHT:
                        self.player1.controlright()
                    elif event.key==pygame.K_LEFT:
                        self.player1.controlleft()
                    elif event.key==pygame.K_q:
                        pygame.quit()
                        sys.exit()
                    elif event.key==pygame.K_UP and (self.setting.up==False and self.setting.down==False):
                        self.player1.controljump()
                        self.bleed.bleedlong2=10
                    elif event.key==pygame.K_SPACE and self.player1.handout1==False and self.handoutstart==None:
                        self.handoutstart=time.time()
                        self.setting.player1hand=True
                        # self.recvallb.handout1=True
                        self.player1.handout1=True
                    elif event.key==pygame.K_a:
                        self.a=True
                elif event.type==pygame.MOUSEBUTTONDOWN:
                    mousexy=pygame.mouse.get_pos()
                    if self.button.rect.collidepoint(mousexy) and self.start1==False:
                        self.start1=True
                    elif self.a:
                        self.zobi=True
                        self.mousepos=pygame.mouse.get_pos()


                elif event.type==pygame.KEYUP:
                    if event.key==pygame.K_RIGHT:
                        self.player1.controlrightstop()
                    elif event.key==pygame.K_LEFT:
                        self.player1.controlleftstop()
                    elif event.key==pygame.K_SPACE:
                        self.setting.player1hand=False
                        self.player1.handout1=False
            if self.start1 and self.start2:
                print(pygame.mouse.get_pos())
                self.screen.fill(self.white)
                self.showsprite()
                self.collidefind()
                self.controlhandsprite()
                self.bleed.drawbleed()
                self.handoutcontrol2()
                self.mousecontrol()
            else:
                self.button.buttonshow()
            pygame.time.Clock().tick(50)
            #pygame.mixer.set_volume(0.2)
            #self.sound.play()
            pygame.display.flip()
            pygame.display.update()
            self.sockserverrun()
    def mousecontrol(self):
        if self.zobi:
            self.mousepos=pygame.mouse.get_pos()
            self.handoutstart=None
    def handoutcontrol2(self):
        self.handoutend=time.time()
        if self.handoutstart:
            if (self.handoutend-self.handoutstart)>2:
                self.handoutstart=None
    def controlhandsprite(self):
        if self.player1.handout1 and len(self.player1handgroup)==0:
            self.player1handgroup.add(self.handout1)
        elif self.player1.handout1==False:
            for i in self.player1handgroup:
                self.player1handgroup.remove(i)
        if self.player2.handout2 and len(self.player2handgroup)==0:
            self.player2handgroup.add(self.handout2)
        elif self.player2.handout2==False:
            for i in self.player2handgroup:
                self.player2handgroup.remove(i)
    def collidefind(self):
        if self.end:
            if self.bleed.bleedlong1>self.bleed.bleedlong2:
                self.font=pygame.font.SysFont('SimHei',48)
                self.win=self.font.render('胜利',True,self.setting.black,self.setting.white)
                self.winrect=self.win.get_rect()
                self.winrect.center=self.screen.get_rect().center
                self.screen.blit(self.win,self.winrect)
                pygame.display.flip()
                pygame.display.update()
                pygame.time.wait(1000)
                pygame.quit()
                sys.exit()
            elif self.bleed.bleedlong2>self.bleed.bleedlong1:
                self.font=pygame.font.SysFont('SimHei',48)
                self.notwin=self.font.render('失败',True,self.setting.black,self.setting.white)
                self.notwinrect=self.notwin.get_rect()
                self.notwinrect.center=self.screen.get_rect().center
                self.screen.blit(self.notwin,self.notwinrect)
                pygame.display.flip()
                pygame.display.update()
                pygame.time.wait(1000)
                pygame.quit()
                sys.exit()
            # pygame.quit()
            # sys.exit()
        # if self.player1.handout1 and len(self.player1handgroup)>0:
        #     if pygame.sprite.groupcollide(self.player1handgroup,self.player2group,True,False):
        #         self.bleed.bleedlong2-=1
        # if self.player2.handout2 and len(self.player2handgroup)>0:
        #     if pygame.sprite.groupcollide(self.player2handgroup,self.player1group,True,False):
        #         self.bleed.bleedlong1-=1
    def controlsprite(self):
        self.player1group.add(self.player1)
        # self.player1handgroup.add(self.handout1)
        self.player2group.add(self.player2)
        # self.player2handgroup.add(self.handout2)
    def showsprite(self):
        for i in self.player1group:
            i.draw_player1()
            i.move()
            i.jump()
        for i in self.player1handgroup:
            i.handfight()
        for i in self.player2group:
            i.draw_player2()
        for i in self.player2handgroup:
            i.drawplayer2hand()
    def sockbind(self):
        try:
            self.sock.bind((self.setting.host,self.setting.port))
            self.sock.listen(10000)
            print(f'[*] Listen on {self.setting.host}:{self.setting.port}')
            self.client,self.address=self.sock.accept()
            print(f'Received from {self.address[0]}:{self.address[1]}')
        except:
            pass
        # try:
        #     self.sock.bind((self.setting.host,self.setting.port))
        #     self.sock.listen(10000)
        #     print(f'[*] Listen on {self.setting.host}:{self.setting.port}')
        #     self.client,self.address=self.sock.accept()
        #     print(f'Received from {self.address[0]}:{self.address[1]}')
        #     self.sock.settimeout(0.001)
        # except:
        #     pass
    def sockserverrun(self):
        print(self.player2.rect)
        # try:







        try:

            #self.sock.settimeout(0.001)
            try:
                request=self.client.recv(2024)
                #self.sock.settimeout(0.001)
                print(f'[*] Received from {request.decode("utf-8")}')
                print(self.player2.handout2)
            except:
                pass

            if self.handout2re.search(request.decode('utf-8')).group()=='handout2True':

                self.player2.handout2=True
                print(self.handout2re.search(request.decode('utf-8')).group())

            elif self.handout2re.search(request.decode('utf-8')).group()=='handout2False':
                self.player2.handout2=False
                print(self.handout2re.search(request.decode('utf-8')).group())
            if re.compile(r'rectx(\d)*').search(request.decode('utf-8')).group():#=='rectx':
                if re.compile(r'rectx(\d)*').search(request.decode('utf-8')).group()!='rectx':
                    self.player2.rect.x=float(re.compile(r'rectx(\d)*').search(request.decode('utf-8')).group()[5:])
            if re.compile(r'recty(\d)*').search(request.decode('utf-8')).group():#=='recty':
                if re.compile(r'recty(\d)*').search(request.decode('utf-8')).group()!='recty':
                    self.player2.rect.y=float(re.compile(r'recty(\d)*').search(request.decode('utf-8')).group()[5:])
            if self.bleed1re.search(request.decode('utf-8')).group():
                if self.bleed.bleedlong1==0.0:
                    self.bleed.bleedlong1=100
                    self.font=pygame.font.SysFont('SimHei',48)
                    self.notwin=self.font.render('失败',True,self.setting.black,self.setting.white)
                    self.notwinrect=self.notwin.get_rect()
                    self.notwinrect.center=self.screen.get_rect().center
                    self.screen.blit(self.notwin,self.notwinrect)
                    pygame.display.flip()
                    pygame.display.update()
                    pygame.time.wait(1000)
                    pygame.quit()
                    sys.exit()
                else:
                    self.bleed.bleedlong1=float(self.bleed1re.search(request.decode('utf-8')).group()[6:])
            if self.bleed2re.search(request.decode('utf-8')).group():
                if self.bleed.bleedlong2==0.0:

                    self.font=pygame.font.SysFont('SimHei',48)
                    self.win=self.font.render('胜利',True,self.setting.black,self.setting.white)
                    self.winrect=self.win.get_rect()
                    self.winrect.center=self.screen.get_rect().center
                    self.screen.blit(self.win,self.winrect)
                    pygame.display.flip()
                    pygame.display.update()
                    pygame.time.wait(1000)
                    pygame.quit()
                    sys.exit()
                else:
                    self.bleed.bleedlong2=float(self.bleed2re.search(request.decode('utf-8')).group()[6:])
                    print(self.bleed.bleedlong2)
            if self.startre.search(request.decode('utf-8')).group():
                if self.startre.search(request.decode('utf-8')).group()[6:10]=='True':
                    self.start2=True
            if self.endre.search(request.decode('utf-8')).group():
                if self.endre.search(request.decode('utf-8')).group()[4:8]=='True':
                    self.end=True
            if self.rezobi01.search(request.decode('utf-8')).group():
                if self.rezobi01.search(request.decode('utf-8')).group()[6:10]=='True':
                    None
                    #self.player1.rect.x=float(self.rezobi11.search(request.decode('utf8')).group()[6:])
                    #self.player1.rect.y=float(self.rezobi21.search(request.decode('utf-8')).group()[6:])
            # elif request.decode('utf-8')=='rect2rightTrue':
            #     self.player2.rectright=True

            #     print('rect2rightTrue')
            # elif request.decode('utf-8')=='rect2rightFalse':
            #     self.player2.rectright=False
            # elif request.decode('utf-8')=='rect2leftTrue':
            #     self.player2.rectleft=True
            # elif request.decode('utf-8')=='rect2leftFalse':
            #     self.player2.rectleft=False
            print('yes')
            sendtoo='handout1'+str(self.player1.handout1)+'rectx'+str(self.player1.rect.x)\
            +'recty'+str(self.player1.rect.y)+'bleed1'+str(self.bleed.bleedlong1)\
            +'bleed2'+str(self.bleed.bleedlong2)+'start1'+str(self.start1)+\
            'start2'+str(self.start2)+'type'+str(self.end)
            if self.a and self.zobi and self.mousepos!=None:

                sendtoo+='zobi02'+str(self.zobi)+'zobi12'+str(self.mousepos[0])+'zobi22'+str(self.mousepos[1])
                print(sendtoo)
            else:
                sendtoo+='zobi02'+str(self.zobi)
            print(self.start1)
            print(sendtoo)
            self.client.sendall(sendtoo.encode())
        except:
            pass


class setting:
    def __init__(self):
        self.white=(255,255,255)
        self.black=(0,0,0)
        self.bleed1=(0,0,255)
        self.bleed2=(0,255,0)
        self.recthand=10
        self.recthandlong=30
        self.rectwidthheight=50
        self.player1color=(100,100,100)
        self.player1speed=4
        self.g=0.98
        self.up=False
        self.uptime=50
        self.down=False
        self.player1hand=False
        #player2
        self.player2color=(250,0,0)
        self.host='192.168.0.108'
        self.port=8000
class player1(pygame.sprite.Sprite):
    def __init__(self,run):
        super().__init__()
        self.handout1=False
        self.screen=run.screen
        self.setting=run.setting
        self.rectright=False
        self.rectleft=False
        self.rect=pygame.Rect(0,0,self.setting.rectwidthheight,self.setting.rectwidthheight)
        self.rect.bottomright=self.screen.get_rect().bottomright
        #self.sound=pygame.mixer.Sound('luyin.wav')
    def draw_player1(self):
        pygame.draw.rect(self.screen,self.setting.player1color,self.rect)
    def controlright(self):

        self.rectright=True
    def controlrightstop(self):
        self.rectright=False
    def controlleft(self):
        self.rectleft=True
    def controlleftstop(self):
        self.rectleft=False
    def move(self):
        if self.rectright and self.rect.right<self.screen.get_rect().right:
            self.rect.x+=self.setting.player1speed
        elif self.rectleft and self.rect.left>self.screen.get_rect().left:
            self.rect.x-=self.setting.player1speed
    def controljump(self):
        if self.setting.up!=True:
            self.setting.up=True
    def jump(self):
        if self.setting.up==True and self.setting.uptime>0:
            self.rect.y-=(self.setting.g*self.setting.uptime)
            self.setting.uptime-=2
        elif self.setting.up==True and self.setting.uptime==0:
            self.setting.down=True
            self.setting.up=False
        if self.setting.down==True and self.setting.uptime<50:
            self.rect.y+=(self.setting.g*self.setting.uptime)
            self.setting.uptime+=2
        elif self.setting.down==True and self.setting.uptime==50:
            self.setting.down=False
            self.setting.uptime=50
            self.rect.bottom=self.screen.get_rect().bottom
        # if self.setting.up==True and self.rect.y>self.screen.get_rect().bottom:
        #     self.setting.uptime=0
        #     self.setting.up=False
            assert self.setting.down==False and self.setting.up==False
class handout1(pygame.sprite.Sprite):
    def __init__(self,run):
        super().__init__()
        self.setting=run.setting
        self.screen=run.screen
        self.player1=run.player1
        self.rect=pygame.Rect(0,0,self.setting.recthandlong,self.setting.recthand)
    def handfight(self):
        if self.setting.player1hand==True:


            self.rect.midright=self.player1.rect.midleft

            pygame.draw.rect(self.screen,self.setting.player1color,self.rect)
            self.sound=pygame.mixer.Sound('player1hand.wav')
            self.sound.set_volume(0.1)

            self.sound.play()



class player2(pygame.sprite.Sprite):
    def __init__(self,run):
        super().__init__()
        self.handout2=False
        ##

        self.screen=run.screen
        self.setting=setting()
        self.rect=pygame.Rect(0,0,self.setting.rectwidthheight,self.setting.rectwidthheight)
        self.rect.bottomleft=self.screen.get_rect().bottomleft
        self.rectright=False
        self.rectleft=False
    def draw_player2(self):

        pygame.draw.rect(self.screen,self.setting.player2color,self.rect)


class handout2(pygame.sprite.Sprite):
    def __init__(self,run):
        super().__init__()
        self.screen=run.screen
        self.setting=run.setting
        self.player2=run.player2
        self.rect=pygame.Rect(0,0,self.setting.recthandlong,self.setting.recthand)

    def drawplayer2hand(self):
        if self.player2.handout2==True:

            self.rect.midleft=self.player2.rect.midright
            pygame.draw.rect(self.screen,self.setting.player2color,self.rect)
            self.sound=pygame.mixer.Sound('player2hand.wav')
            self.sound.set_volume(0.1)
            self.sound.play()
        #self.move()

    #def move(self):
        # print(self.rectright,self.rectleft)
        # if self.rectright and self.rect.right<self.screen.get_rect().right:
        #     self.rect.x+=self.setting.player1speed
        # elif self.rectleft and self.rect.left>self.screen.get_rect().left:
        #     self.rect.x-=self.setting.player1speed
# class recvallb:
#     def __init__(self):
#         self.datarecv=None
#         self.setting=setting()
#         self.handout1=False
#         self.sock=socket.socket(socket.sbAF_INET,socket.SOCK_STREAM)
#     def recvall(self):
#         print('go')
#         self.sock.connect((self.setting.host,self.setting.port))
#         self.hand1outcontrol()
#         try:
#             self.datarecv=self.socketserverpygame.sock.recv(1024).decode()
#             print(self.datarecv)
#             if self.datarecv=='handout1True':
#                 player2().player2handout=True
#             elif self.datarecv=='handout1False':
#                 player2().palyer2handout=False
#         except:
#             pass
#     def hand1outcontrol(self):
#         print(self.handout1)
#         if self.handout1==True:
#             self.sock.sendall(b'handout1True')
class Button(pygame.sprite.Sprite):
    def __init__(self,run):
        super().__init__()
        self.screen=run.screen
        self.setting=run.setting
        self.color=(30,30,30)
        self.bcolor=(200,200,200)
        self.width,self.height=50,20
        self.font=pygame.font.SysFont('SimHei',48)
        self.rect=pygame.Rect(0,0,self.width,self.height)
        self.rect.center=self.screen.get_rect().center
        self.text=self.font.render('开始',True,self.color,self.bcolor)
        self.textrect=self.text.get_rect()
        self.textrect.center=self.rect.center
    def buttonshow(self):

        self.screen.fill(self.bcolor,self.rect)
        self.screen.blit(self.text,self.textrect)
class bleed:
    def __init__(self,run):
        self.bleedlong2=100
        self.bleedwidth2=10
        self.bleedlong1=100
        self.bleedwidth1=10
        self.setting=setting()
        self.screen=run.screen

    def drawbleed(self):
        self.rect2=pygame.Rect(0,0,self.bleedlong2,self.bleedwidth2)
        self.rect2.topleft=self.screen.get_rect().topleft
        pygame.draw.rect(self.screen,self.setting.bleed2,self.rect2)
        self.rect1=pygame.Rect(0,0,self.bleedlong1,self.bleedwidth1)
        self.rect1.topright=self.screen.get_rect().topright
        pygame.draw.rect(self.screen,self.setting.bleed1,self.rect1)

if __name__=='__main__':
    # t=Thread(target=recvallb().recvall(),args=(10,))
    # t.start()
    run=rungame()
    run.run_game()

