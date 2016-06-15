__author__ = 'marcusmorgenstern'
__mail__ = ''

from kivy.uix.relativelayout import RelativeLayout
from kivy.graphics import Line


class DraggableWidget(RelativeLayout):
    def __init__(self, **kwargs):
        self.selected = None
        super(DraggableWidget, self).__init__(**kwargs)

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.select()
            return True
        return super(DraggableWidget, self).on_touch_down(touch)

    def on_touch_up(self, touch):
        if self.selected:
            self.unselect()
            return True
        return super(DraggableWidget, self).on_touch_up(touch)

    def on_touch_move(self, touch):
        (x, y) = self.parent.to_parent(touch.x, touch.y)
        if self.selected and self.parent.collide_point(x - self.width/2, y - self.height/2):
            self.translate(touch.x - self.ix, touch.y - self.iy)
            return True
        return super(DraggableWidget, self).on_touch_move(touch)

    def select(self):
        if not self.selected:
            self.ix = self.center_x
            self.iy = self.center_y
            with self.canvas:
                print self.width, self.height
                self.selected = Line(rectangle=(0, 0, self.width, self.height), dash_offset = 2)

    def unselect(self):
        if self.selected:
            self.canvas.remove(self.selected)
            print "removed"
            self.selected = None

    def translate(self, x, y):
        print "translate"
        self.center_x = self.ix = self.ix + x
        self.center_y = self.iy = self.iy + y


class Node(DraggableWidget):
    pass