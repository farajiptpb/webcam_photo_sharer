from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
import time
from filestack import Client
import webbrowser
from kivy.core.clipboard import Clipboard

Builder.load_file('frontend.kv')


class FirstScreen(Screen):

    def start_stop_cam(self):

        if self.ids.cam.play == False :
            self.ids.cam.opacity = 1
            self.ids.cam.play = True
            self.ids.ss.text = 'Stop'
            #self.ids.cam.texture \
                #= self.ids.cam._camera.texture
            self.ids.cap.text = 'Capture'
        else:
            self.ids.cam.opacity = 0
            self.ids.cam.play = False
            self.ids.ss.text = 'Start'
            #self.ids.cam.texture = None

    def capture(self):
        current_time = time.strftime('%Y%m%d-%H%M%S')
        global file_name
        file_name = current_time + '.png'

        if self.ids.ss.text == 'Stop':
            self.ids.cam.export_to_png(file_name)
            self.manager.current = 'second_screen'
            self.manager.current_screen.ids.img.source = file_name
        else:
            self.ids.cap.text = 'First start the camera and try again'


class SecondScreen(Screen):
    def back_to_cam(self):
        self.manager.current = 'first_screen'

    def create_link(self):

        client = Client(apikey='AKL0sKGIRLiD4HQWQIbcQz')
        cloud_file = client.upload(filepath=file_name)
        self.url = cloud_file.url
        self.ids.link.text = self.url

    def open_link(self):
        try:
            webbrowser.open(self.url)
        except:
            self.ids.link.text = 'First create the link'

    def copy(self):
        try:
            Clipboard.copy(self.url)
        except:
            self.ids.link.text = 'First create the link'


class RootWidget(ScreenManager):
    pass


class MainApp(App):

    def build(self):
        return RootWidget()


MainApp().run()