from random import randint as rndi, random as rnd


from kivy.uix.widget import Widget
from kivy.properties import ListProperty, StringProperty, NumericProperty
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.graphics import Color, RoundedRectangle
from kivymd.uix.label import MDLabel

class RectWidget(Widget):
    color = ListProperty([0.3, 0.6, 0.9, 1])

    def __init__(self, size_hint_y, color, **kwargs):
        super().__init__(**kwargs)
        self.size_hint_y = size_hint_y
        with self.canvas:
            Color(*color)
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[3])
        self.bind(pos=self.update_rect, size=self.update_rect)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size


class TagFeld(ButtonBehavior, MDBoxLayout):
    back_color = ListProperty([0, 0.2, 0.2, 1])
    text = StringProperty("-")
    text_color = ListProperty([0.8, 0.2, 0.2, 1])
    termin_rect_anz = NumericProperty(10)
    kalendertag:bool = False

    def __init__(self, text, termin_rect_list=None, **kwargs):
        super().__init__(**kwargs)
        self.text = str(text)
        self.orientation = 'horizontal'
        self.padding = 5
        #self.spacing = 10
        self.size_hint = (1, 1)

        # Erscheinungsbild- & Verhaltensanpassung
        if termin_rect_list is None: # kein Kalendertag
            text_color = [0.4, 0.4, 0.4, 1]
            self.kalendertag = False
        else:
            text_color = self.text_color
            self.kalendertag = True

        # Canvas für Rahmen
        with self.canvas:
            self.bg_color = Color(rgba=self.back_color)
            self.bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[10])

        # Haupt-BoxLayout
        self.main_box = MDBoxLayout(orientation='horizontal', size_hint=(1, 1), pos=self.pos)
        self.add_widget(self.main_box)

        # Zentraler Text
        self.central_text = MDLabel(
            halign='center',
            text=self.text,
            text_color=text_color,
            theme_text_color = 'Custom'
        )
        self.main_box.add_widget(self.central_text)

        # Rechte Box
        self.right_box = MDBoxLayout(
            orientation='vertical',
            size_hint_x=0.3,
            spacing=0
        )
        self.main_box.add_widget(self.right_box)

        # Termin-Rechteck-Widgets hinzufügen
        if self.kalendertag:
            self.setup_rectangles(self.gen_termin_rect_list())

        # Bindings für Canvas-Update
        self.bind(pos=self.update_canvas, size=self.update_canvas)


    def gen_termin_rect_list(self):
        #test data-dummy
        termin_rect_list = []
        left_h = 24
        for i in range(5):
            r = rndi(2,6)
            if r<left_h:
                left_h-=r
            else:
                r = left_h
                left_h = 0
            termin_rect_list.append([r / 24, [rnd(), rnd(), rnd(), 1 * (i % 5)*rndi(0,1)]])
            if left_h == 0: break
        return termin_rect_list

    def setup_rectangles(self,termin_rect_list):
        """termin_rect_list: [[h_r,color],...] für die Termine, h_r:Dauer in Stunden/24, color: falbliste[4*int]"""
        self.right_box.clear_widgets()
        for r in termin_rect_list:
            rect = RectWidget(r[0],r[1])
            self.right_box.add_widget(rect)

    def update_canvas(self, *args):
        self.bg_rect.pos = self.pos
        self.bg_rect.size = self.size

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if not touch.is_mouse_scrolling and self.kalendertag:
                self.on_click()
            return True
        return super().on_touch_down(touch)

    def on_click(self):
        print(f"TagFeld {self.text} wurde geklickt")