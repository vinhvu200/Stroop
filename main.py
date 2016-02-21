import os
import sys

import kivy
from kivy.uix.screenmanager import ScreenManager, Screen, WipeTransition
from kivy.app import App
from kivy.lang import Builder

from random import Random
from kivy.clock import Clock
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty
from kivy.uix.popup import Popup

from kivy.core.audio import SoundLoader

class StroopGame(Screen):
    #RGBA values
    red = [200, 0, 0, .8]
    green = [0, 140, 0, .5]
    blue = [0, 0, 200, .45]
    yellow = [255, 255, 0, .85]
    purple = [128, 0, 128, .5]
    
    #All colors
    color = ['Red', 'Green', 'Blue',
                'Yellow', 'Purple']
    
    #check if colors have been used
    color_check = {'Red': False,
                'Green': False,
                'Blue': False,
                'Yellow': False,
                'Purple': False
                }
    
    #match color to RGBA value
    RGBA_color = {'Red': red,
                    'Green': green,
                    'Blue': blue,
                    'Yellow': yellow,
                    'Purple': purple
                }

    #Random object
    a = Random()
    
    #Score and Time
    Score = 0
    Time = 5
    Count_down_timer = 3
    
    color_button1 = ObjectProperty(None)
    color_button2 = ObjectProperty(None)
    color_button3 = ObjectProperty(None)
    color_button4 = ObjectProperty(None)
    reset_button = ObjectProperty(None)
    score_button = ObjectProperty(None)
    timer_button = ObjectProperty(None)
    color_direction_button = ObjectProperty(None)
    start_button = ObjectProperty(None)
    count_down_button = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(StroopGame, self).__init__(**kwargs)           
        
        #bindings
        #self.reset_button.bind(on_press=self.reset)
        #self.start_button.bind(on_press=Clock.schedule_interval(self.count_down, 1))
    
        self.reset(self)
        #Clock.schedule_interval(self.count_down, 1)
    
    def start_count_down(self):
        Clock.schedule_interval(self.count_down, 1)
    
    def count_down(self, obj):
        if (self.Count_down_timer == 3):
            self.timer_button.text = 'READY...'
        elif (self.Count_down_timer == 2):
            self.timer_button.text = 'SET...'
        elif (self.Count_down_timer == 1):
            self.timer_button.text = 'GO!'
        else:
            self.game_begin(self)
            Clock.unschedule(self.count_down)
        
        self.Count_down_timer -= 1
    
    # PURPOSE: reset all buttons
    def reset(self, instance):
        gray_color = [1, 1, 1, 1]
        self.Score = 0
        self.Time = 5
        self.Count_down_timer = 3
        
        # reset color buttons
        self.color_button1.background_color = gray_color
        self.color_button2.background_color = gray_color
        self.color_button3.background_color = gray_color
        self.color_button4.background_color = gray_color
        self.color_direction_button.background_color = [255,0,0,.9]
        
        # reset texts
        self.score_button.text = 'Score: 0'
        self.color_direction_button.text = 'COLOR DIRECTION'
        #self.start_button.text = 'START'
        self.timer_button.text = 'Timer'
        
        # reset bindings
        #self.start_button.bind(on_press=Clock.schedule_interval(self.count_down, 1))
        
        # stop the clock
        Clock.unschedule(self.count_down)
        Clock.unschedule(self.game_timer)
        Clock.unschedule(self.game_end)
        
    # starts the game
    def game_begin(self, instance):
        self.timer_button.text = 'Time : %r' %self.Time
        Clock.schedule_interval(self.game_timer, 1)
        Clock.schedule_once(self.game_end, self.Time)
        self.start()
    
    # PURPOSE: Timer
    def game_timer(self, instance):
        self.Time -= 1
        message = 'Time : %r' % self.Time
        self.timer_button.text = message
        
        if (self.Time == 0):
            self.timer_button.text = 'FINISH'
            Clock.unschedule(self.game_timer)
    
    # PURPOSE: end game
    #       -unbind all color buttons and start_button
    def game_end(self, instance):
        message = 'FINAL SCORE : %r' % self.Score
        self.score_button.text = message
        self.color_button1.unbind(on_press=self.correct)
        self.color_button2.unbind(on_press=self.correct)
        self.color_button3.unbind(on_press=self.correct)
        self.color_button4.unbind(on_press=self.correct)
        #self.start_button.unbind(on_press=self.game_begin)
    
    # Shuffle all colors
    #   -ask to click correct color
    #   -add score if correct
    def start(self):
        correct_color = self.shuffle()
        correct_button = self.RGBA_color[correct_color]
        
        if (self.color_button1.background_color == correct_button):
            self.color_button1.bind(on_press=self.correct)
        elif (self.color_button2.background_color == correct_button):
            self.color_button2.bind(on_press=self.correct)
        elif (self.color_button3.background_color == correct_button):
            self.color_button3.bind(on_press=self.correct)
        elif (self.color_button4.background_color == correct_button):
            self.color_button4.bind(on_press=self.correct)
        else:
            print 'None'
            
    # PURPOSE: add point for getting it correct
    def correct(self, instance):
        self.Score += 1
        message = 'Score : %s' % self.Score
        self.score_button.text = message
        
        self.color_button1.unbind(on_press=self.correct)
        self.color_button2.unbind(on_press=self.correct)
        self.color_button3.unbind(on_press=self.correct)
        self.color_button4.unbind(on_press=self.correct)
        
        self.start()
    
    # PURPOSE: shuffles all background_colors of button
    #           -returns the correct answer
    def shuffle(self):
        color_choice = []
    
        self.color_check = {'Red': False,
                            'Green': False,
                            'Blue': False,
                            'Yellow': False,
                            'Purple': False
                            }
        
        # color_button1
        b = self.a.randint(0, 4)
        while (self.color_check[self.color[b]] == True):
            b = self.a.randint(0, 4)    
        self.color_check[self.color[b]] = True
        color_choice.append(self.color[b])
        self.color_button1.background_color = (self.RGBA_color[self.color[b]])

        # color_button2
        b = self.a.randint(0, 4)
        while (self.color_check[self.color[b]] == True):
            b = self.a.randint(0, 4)    
        self.color_check[self.color[b]] = True
        color_choice.append(self.color[b])
        self.color_button2.background_color = (self.RGBA_color[self.color[b]])
        
        # color_button3
        b = self.a.randint(0, 4)
        while (self.color_check[self.color[b]] == True):
            b = self.a.randint(0, 4)    
        self.color_check[self.color[b]] = True
        color_choice.append(self.color[b])
        self.color_button3.background_color = (self.RGBA_color[self.color[b]])
        
        # color_button4
        b = self.a.randint(0, 4)
        while (self.color_check[self.color[b]] == True):
            b = self.a.randint(0, 4)    
        self.color_check[self.color[b]] = True
        color_choice.append(self.color[b])
        self.color_button4.background_color = (self.RGBA_color[self.color[b]])

        # color_direction_button
        b = self.a.randint(0, 3)
        self.color_direction_button.text = color_choice[b]
        self.color_direction_button.background_color = (self.RGBA_color[self.color[b]])
        
        return self.color_direction_button.text

class Menu(Screen):
    pass
    
class HowToPlay(Screen):
    pass

class Setting(Screen):
    pass
    
class GameOver(Popup):
    final_score = ObjectProperty(None)
    
class stroopApp(App):
    
    time = 5
    music_on = False
    
    def build(self):
        self.data_path = os.path.realpath(os.path.dirname(sys.argv[0])) + os.sep + "all_audio" + os.sep
    
        self.sm = ScreenManager(transition=WipeTransition())
    
        self.menu = Menu(name='menu')
        self.game = StroopGame(name='game')
        self.how_to_play = HowToPlay(name='how_to_play')
        self.setting = Setting(name='setting')
        
        self.sm.add_widget(self.menu)
        self.sm.add_widget(self.how_to_play)
        self.sm.add_widget(self.game)
        self.sm.add_widget(self.setting)
        
        return self.sm

    def play_music(self):
        if (self.music_on == False):
        
            sound = SoundLoader.load(self.data_path + 'audio2.mp3')
            sound.loop = True
            sound.volume = .5
            sound.play()
            self.music_on = True
        
    def start_game(self):
        self.time = 5
        self.sm.current = 'game'
        self.game.reset(self)
        self.game.start_count_down()
        Clock.schedule_interval(self.Timer, 1)
        
    def Timer(self, instance):
        if (self.time + 3 == 0):
            Clock.unschedule(self.Timer)
            self.popup()            
        self.time -= 1
    
    def go_to_menu(self):
        self.sm.current = 'menu'
    
    def popup(self):
        game_over_ad = GameOver()
        game_over_ad.final_score.text = 'Final score: %r' %self.game.Score
        game_over_ad.open()
        
if __name__ == '__main__':
    stroopApp().run()