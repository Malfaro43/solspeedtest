import pygame
from pygame import mixer
import sys
import time
import pandas as pd
import random
import json


class Test:
    def __init__(self):
        self.active = False
        self.nor = False
        self.current = 0
        self.netwpm = ''
        self.rawwpm = ''
        self.accuracy = ''
        self.total_char = 0
        self.gen_len = 10
        #words or quotes
        self.words_active = True
        self.quotes_active = False
        self.words_surf = info_font.render('words', True, '#0047AB')
        self.quotes_surf = info_font.render('quotes', True, '#7393B3')
        self.words_rect = pygame.Rect(869, 10, 47, 19)
        self.quotes_rect = pygame.Rect(929, 10, 54, 19)
        #generation length surfaces
        self.five = info_font.render('5', True, '#7393B3')
        self.ten = info_font.render('10', True, '#0047AB')
        self.fifteen = info_font.render('15', True, '#7393B3')
        self.thirty  = info_font.render('30', True, '#7393B3')
        self.five_rect = pygame.Rect(869, 30, 15, 19)
        self.ten_rect = pygame.Rect(889, 30, 20, 19)
        self.fifteen_rect = pygame.Rect(919, 30, 20, 19)
        self.thirty_rect = pygame.Rect(946, 30, 20, 19)
        #quotes options
        self.normal_active = True
        self.asol_active = False
        self.normal_surf = info_font.render('normal', True, '#0047AB')
        self.asol_quote_surf = info_font.render('asol', True, '#7393B3')
        self.normal_rect = pygame.Rect(869, 30, 58, 19)
        self.asol_rect = pygame.Rect(939, 30, 40, 19)
        #result surfaces
        self.netwpm_surf = wpm_font.render(self.netwpm, True, '#7393B3')
        self.rawwpm_surf = wpm_font.render(self.rawwpm, True, '#7393B3')
        self.accuracy_surf = wpm_font.render(self.accuracy, True, '#7393B3')
        self.result_surf = title_font.render('', True, '#6082B6')
        #password generation
        self.psuedo = []
        self.gen_pass()
        self.psuedo_surf = {i:[list(self.psuedo)[i], 'uncompleted'] for i in range(len(self.psuedo))}
        self.psuedo_split = self.psuedo.split(' ')
        self.number = {}
        self.nowordbreak()
       
        self.xdistance = 25
        self.ydistance = 160
        #cursor
        self.ycurse = 190
        self.cursecurrent = 0
        self.cursor = pygame.Rect(self.xdistance, 380, 18, 3)
        #self.reset()

    def nowordbreak(self):
        a = 50
        c = a
        b = True
        if len(self.psuedo) >= a:
            while b:
                try:
                    if self.psuedo[a] != ' ':
                            if self.psuedo[c] == ' ':
                                self.number[c+1] = True
                            else:
                                c -= 1
                    else:
                        self.number[c+1] = True

                except:
                    b = False
                    break
                a += 50
                c = a


    def draw(self):
        if self.nor == False:
            self.cursor = pygame.Rect((25+18*self.cursecurrent), self.ycurse, 18, 3)
            pygame.draw.rect(screen, '#6F8FAF', self.cursor, border_radius = 15)
            try:
                if self.number[self.current]:
                    self.cursecurrent = 0
                    self.ycurse += 35
                    self.number[self.current] = False
            except: pass
            
            for i in range(len(self.psuedo_surf)):
                try:
                    self.number[i]
                    self.xdistance = 25
                    self.ydistance += 35
                except: pass
                if self.psuedo_surf[i][1] == 'uncompleted':
                    temp = test_font.render(self.psuedo[i][0], True, '#7393B3')
                    screen.blit(temp, (self.xdistance, self.ydistance))
                elif self.psuedo_surf[i][1] == 'completed':
                    temp = test_font.render(self.psuedo[i][0], True, '#0047AB')
                    screen.blit(temp, (self.xdistance, self.ydistance))
                elif self.psuedo_surf[i][1] == 'incorrect':
                    temp = test_font.render(self.psuedo[i][0], True, '#DC143C')
                    screen.blit(temp, (self.xdistance, self.ydistance))
                self.xdistance += 18

        self.xdistance = 25
        self.ydistance = 160
        screen.blit(self.words_surf, (870, 10))
        screen.blit(self.quotes_surf, (930, 10))

        if self.words_active:
            screen.blit(self.five, (870, 30))
            screen.blit(self.ten, (890, 30))
            screen.blit(self.fifteen, (920, 30))
            screen.blit(self.thirty, (947, 30))
        
        if self.quotes_active:
            screen.blit(self.normal_surf, (870, 30))
            screen.blit(self.asol_quote_surf, (940, 30))
    
    def gen_pass(self):
        if self.words_active:
            for i in range(self.gen_len):
                self.psuedo.append(str(random.choice(random_words.word[:300])))
            self.psuedo = ' '.join(self.psuedo)
        if self.quotes_active:
            if self.normal_active:
                while True:
                    self.psuedo = random.choice(normal_quotes.quote[:400])
                    if len(self.psuedo) <= 248:
                        break
            if self.asol_active:
                self.psuedo = random.choice(asol_quotes)
                if self.psuedo == 'Boop.':
                    boop.play()


    def start(self):
        self.wpm_surf = wpm_font.render('', True, '#7393B3')
        self.active = True
        self.start_time = time.time()

    def end(self):
        correct_c = sum([1 for i in self.psuedo_surf if self.psuedo_surf[i][1] == 'completed'])
        incorrect_c = sum([1 for i in self.psuedo_surf if self.psuedo_surf[i][1] == 'incorrect'])
        self.result_surf = title_font.render('Results', True, '#6082B6')
        self.nor = True
        self.end_time = time.time()
        self.rawwpm = str(round((len(self.psuedo_surf)/5)/((self.end_time - self.start_time)/60)))
        self.netwpm = str(round(int(self.rawwpm) - (incorrect_c/((self.end_time-self.start_time)/60))))
        if int(self.netwpm) < 0: self.netwpm = '0'
        self.accuracy = 'Accuracy: ' + str(round((correct_c/self.total_char)*100)) + '%'
        self.accuracy_surf = wpm_font.render(self.accuracy, True, '#7393B3')
        self.netwpm_surf = wpm_font.render('Net WPM: ' + self.netwpm, True, '#7393B3')
        self.rawwpm_surf = wpm_font.render('Raw WPM: ' + self.rawwpm, True, '#7393B3')
        self.active = False

    def reset(self):                     
        self.current = 0
        self.total_char = 0
        self.psuedo = []
        self.nor = False
        self.active = False
        self.gen_pass()
        self.psuedo_surf = {i:[list(self.psuedo)[i], 'uncompleted'] for i in range(len(self.psuedo))}
        self.result_surf = title_font.render('', True, '#6082B6')
        self.accuracy_surf = wpm_font.render('', True, '#7393B3')
        self.rawwpm_surf = wpm_font.render('', True, '#7393B3')
        self.netwpm_surf = wpm_font.render('', True, '#7393B3')
        self.cursecurrent = 0
        self.ycurse = 190
        self.number = {}
        self.nowordbreak() 

pygame.init()
SIZE = width, height = 1000, 700
WHITE = 255, 255, 255
BLACK = 0, 0, 0
GREY = '#A9A9A9'
screen = pygame.display.set_mode(SIZE)
pygame.display.set_caption("Stellar Typing")
clock = pygame.time.Clock()
title_font = pygame.font.SysFont('courier', 70)
test_font = pygame.font.SysFont('courier', 30)
wpm_font = pygame.font.SysFont('courier', 40)
result_font = pygame.font.SysFont('courier', 39)
info_font = pygame.font.SysFont('courier', 15)
title_surf = title_font.render('Stellar Typing', True, '#6082B6')
random_words = pd.read_csv('dependencies/unigram_freq.csv')
normal_quotes = pd.read_csv('dependencies/quotes.csv')
asol = pygame.image.load('dependencies/asol.png')
pygame.display.set_icon(pygame.transform.scale(asol, (88, 88)))
asol = pygame.transform.scale(asol, (80, 80))
bg_img = pygame.image.load('dependencies/asolbg.png')
bg_img = pygame.transform.scale(bg_img, (600, 500))
with open('dependencies/asol_quotes.json') as f:
   asol_quotes = json.load(f)
sound = pygame.mixer.Sound('dependencies/asolvoice.ogg')
boop = pygame.mixer.Sound('dependencies/boop.ogg')
test1 = Test()
info_text = ['* A minamilistic typing software dedicated to Aurelion Sol', '* If any bugs are found contact aurelion.sol971@gmail.com', '* Click Tab to restart the test']
info_surf = [info_font.render(i, True, '#0047AB') for i in info_text]



while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: pygame.quit(), sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if test1.words_rect.collidepoint(event.pos):
                test1.words_surf = info_font.render('words', True, '#0047AB')
                test1.quotes_surf = info_font.render('quotes', True, '#7393B3')
                test1.words_active = True
                test1.quotes_active = False
                test1.reset()

            if test1.quotes_rect.collidepoint(event.pos):
                test1.words_surf = info_font.render('words', True, '#7393B3')
                test1.quotes_surf = info_font.render('quotes', True, '#0047AB')
                test1.quotes_active = True
                test1.words_active = False
                test1.reset()

            if test1.five_rect.collidepoint(event.pos) and test1.words_active:
                test1.gen_len = 5
                test1.five = info_font.render('5', True, '#0047AB')
                test1.ten = info_font.render('10', True, '#7393B3')
                test1.fifteen = info_font.render('15', True, '#7393B3')
                test1.thirty  = info_font.render('30', True, '#7393B3')
                test1.reset()

            if test1.ten_rect.collidepoint(event.pos) and test1.words_active:
                test1.gen_len = 10
                test1.five = info_font.render('5', True, '#7393B3')
                test1.ten = info_font.render('10', True, '#0047AB')
                test1.fifteen = info_font.render('15', True, '#7393B3')
                test1.thirty  = info_font.render('30', True, '#7393B3')
                test1.reset()

            if test1.fifteen_rect.collidepoint(event.pos) and test1.words_active:
                test1.gen_len = 15
                test1.five = info_font.render('5', True, '#7393B3')
                test1.ten = info_font.render('10', True, '#7393B3')
                test1.fifteen = info_font.render('15', True, '#0047AB')
                test1.thirty  = info_font.render('30', True, '#7393B3')
                test1.reset()

            if test1.thirty_rect.collidepoint(event.pos) and test1.words_active:
                test1.gen_len = 30
                test1.five = info_font.render('5', True, '#7393B3')
                test1.ten = info_font.render('10', True, '#7393B3')
                test1.fifteen = info_font.render('15', True, '#7393B3')
                test1.thirty  = info_font.render('30', True, '#0047AB')
                test1.reset()
            
            if test1.normal_rect.collidepoint(event.pos) and test1.quotes_active:
                test1.normal_surf = info_font.render('normal', True, '#0047AB')
                test1.asol_quote_surf = info_font.render('asol', True, '#7393B3')
                test1.normal_active = True
                test1.asol_active = False
                test1.reset()

            if test1.asol_rect.collidepoint(event.pos) and test1.quotes_active:
                sound.play()
                test1.normal_surf = info_font.render('normal', True, '#7393B3')
                test1.asol_quote_surf = info_font.render('asol', True, '#0047AB')
                test1.asol_active = True
                test1.normal_active = False
                test1.reset()
            

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_TAB:
                test1.reset()

            elif test1.active == False and test1.psuedo_surf[0][1] == 'uncompleted':
                test1.start()

            if test1.active is True:
                try:      

                    if event.key == pygame.K_BACKSPACE:
                        try:
                            test1.number[test1.current]
                            #test1.cursecurrent = test1.pastcursor[-1] 
                            #test1.cursecurrent.pop()
                            #test1.ycurse -= 35
                            #test1.number[test1.current] = True
                            #test1.current -= 1
                        
                        except:
                            if test1.current != 0:
                                test1.current -= 1
                                test1.cursecurrent -= 1
                                test1.psuedo_surf[test1.current][1] = 'uncompleted'

                            else: pass

                    elif event.key == pygame.K_LSHIFT or event.key == pygame.K_RSHIFT: pass

                    elif event.unicode == test1.psuedo_surf[test1.current][0]:
                        test1.psuedo_surf[test1.current][1] = 'completed'
                        test1.current += 1
                        test1.cursecurrent +=1
                        test1.total_char += 1

                    elif event.unicode != test1.psuedo_surf[test1.current][0]:
                        test1.psuedo_surf[test1.current][1] = 'incorrect'
                        test1.current += 1
                        test1.cursecurrent += 1
                        test1.total_char += 1

                except: pass

    screen.fill(WHITE)
    if test1.asol_active and test1.quotes_active:
        #screen.fill((30,28,63))
        screen.blit(bg_img, (200, 70))
    screen.blit(title_surf, (10, 10))
    screen.blit(asol, (615, 3))
    screen.blit(info_surf[0], (10, 620))
    screen.blit(info_surf[1], (10, 640))
    screen.blit(info_surf[2], (10, 660))
    test1.draw()

    if test1.psuedo_surf[len(test1.psuedo_surf)-1][1] != 'uncompleted' and test1.nor == False:
        test1.end()
    screen.blit(test1.result_surf, (365, 190))
    screen.blit(test1.netwpm_surf, (380, 320)) 
    screen.blit(test1.rawwpm_surf, (380, 380))
    screen.blit(test1.accuracy_surf, (380, 440))

    pygame.display.flip()
    clock.tick(144)