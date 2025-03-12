from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty

from kivy.vector import Vector
from kivy.clock import Clock
from random import randint


# NumericProperty — это один из типов свойств в Kivy, фреймворке для разработки графических пользовательских интерфейсов на Python. Он используется для создания свойств, которые могут хранить числовые значения
# (целые числа или числа с плавающей запятой) и автоматически обновлять интерфейс, когда значение изменяется.
# ReferenceListProperty — это специальный тип свойства в Kivy, который используется для хранения списка объектов, которые являются ссылками на другие объекты
# (например, экземпляры классов). Это свойство позволяет создавать связи между объектами и управлять ими в рамках вашего приложения.
#класс для мяча
# В Kivy, Vector — это класс, который представляет вектор в двумерном или трехмерном пространстве. Он используется
# для выполнения различных операций с векторами, таких как сложение, вычитание, умножение на скаляр, нормализация и другие математические операции.

class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):
            vx,vy = ball.velocity
            offset = (ball.center_y - self.center_y) / (self.height / 2)
            bounced = Vector(-1 * vx, vy)
            vel = bounced * 1.1
            ball.velocity = vel.x, vel.y + offset

class PongBall(Widget):
    velocity_x = NumericProperty(0)
    velocity_y = NumericProperty(0)

    velocity = ReferenceListProperty(velocity_x, velocity_y)

    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


class PongGame(Widget):
    ball = ObjectProperty(None)
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)


    def serve_ball(self, vel=(4,0)):
        self.ball.center = self.center
        self.ball.velocity = vel

    #название движения ball
    def update(self, dt):
        self.ball.move()

        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

        if (self.ball.y < 0) or (self.ball.top > self.height):
            self.ball.velocity_y *= -1

        if (self.ball.x < 0) or (self.ball.right > self.width):
            self.ball.velocity_x *= -1

        if self.ball.x < self.x:
            self.player2.score += 1
            self.serve_ball(vel=(4,0))
        if self.ball.right > self.width:
            self.player1.score +=1
            self.serve_ball(vel=(-4,0))

    def on_touch_move(self, touch):
        if touch.x < self.width / 3:
            self.player1.center_y = touch.y
        if touch.x > self.width - self.width / 3:
            self.player2.center_y = touch.y
class PongApp(App):
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0/60.0)
        return game
        # return PongGame()
# class MyApp(App):
#    def build(self):
#        return Label(text='Hello, Kivy!')



if __name__ == '__main__':
   PongApp().run()
