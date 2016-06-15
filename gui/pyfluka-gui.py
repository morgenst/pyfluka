__author__ = 'marcusmorgenstern'
__mail__ = ''

from kivy.app import App
from kivy.lang import Builder
from kivy.uix.anchorlayout import AnchorLayout

Builder.load_file('menubar.kv')
Builder.load_file('drawingspace.kv')
Builder.load_file('toolbar.kv')
Builder.load_file('controlpanel.kv')
Builder.load_file('pyflukawidgets.kv')


class PyFlukaGui(AnchorLayout):
    pass


class PyFlukaGuiApp(App):
    def build(self):
        return PyFlukaGui()


if __name__ == '__main__':
    PyFlukaGuiApp().run()