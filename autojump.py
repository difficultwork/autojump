import os
import win32api,win32gui,win32con
import threading
import time
os.environ['KIVY_IMAGE'] = 'pil,sdl2'

from kivy.app import App
from kivy.uix.switch import Switch
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.button import Button

#winName = '魔兽世界'
winName = '魔兽世界'
signal = False

class AutoJumpTimer:
    signal = False
    def __init__(self):
        return
 
    #开启线程
    def start(self, hwnd):
        self.signal = True
        _thread = threading.Thread(target=self.__run, args=(hwnd,))
        _thread.setDaemon(True)
        _thread.start()#启动线程
        return
 
    def stop(self):
        self.signal = False
        return

    def __run(self, hwnd):
        count = 1
        while self.signal:
            if (count%16 == 0):
                count = 0
                win32api.PostMessage(hwnd, win32con.WM_KEYDOWN, win32con.VK_SPACE, 0)
                win32api.PostMessage(hwnd, win32con.WM_KEYUP, win32con.VK_SPACE, 0)
            else:
                count += 1
            time.sleep(1)
        print("thread closed")
        return

timer = AutoJumpTimer()

class SwitchContainer(GridLayout):
    def __init__(self, **kwargs):
        super(SwitchContainer, self).__init__(**kwargs)
        self.cols = 2
        self.add_widget(Label(text="Auto jump status:"))
        self.settings_sample = Switch(active=False)
        self.add_widget(self.settings_sample)
        self.settings_sample.bind(active=switch_callback)       

# Callback for the switch state transition
def switch_callback(switchObject, switchValue):
    if switchValue:
        global hwnd
        hwnd = win32gui.FindWindow(None, winName)
        if hwnd >= 1:
            timer.start(hwnd)
        else:
            layout = GridLayout(cols=1, padding=10)
            closeButton = Button(text = "OK")
            layout.add_widget(closeButton)
            popup = Popup(title='Not found wow window', content=layout)
            popup.open()
            closeButton.bind(on_press=popup.dismiss)
    else:
        timer.stop()

class AutoJump(App):
    def build(self):
        Window.size = (400, 200)
        return SwitchContainer()

if __name__ == '__main__':
    AutoJump().run()