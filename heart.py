## Libraries
import random
from math import sin, cos, pi, log
from tkinter import *

## Canvas Elements
CANVAS_WIDTH = 640
CANVAS_HEIGHT = 480
CANVAS_CENTER_X = CANVAS_WIDTH / 2
CANVAS_CENTER_Y = CANVAS_HEIGHT / 2
IMAGE_ENLARGE = 11
HEART_COLOR = "#FF69B4"

def heart_function(t, shrink_ratio: float = IMAGE_ENLARGE):
    x = 16 * (sin(t) ** 3)
    y = -(13 * cos(t) - 5 * cos(2 * t) - 2 * cos(3 * t) - cos(4 * t))

    x *= shrink_ratio
    y *= shrink_ratio

    x += CANVAS_CENTER_X
    y += CANVAS_CENTER_Y

    return int(x), int(y)

def scatter_inside(x, y, beta = 0.15):
    ratio_x = - beta * log(random.random())
    ratio_y = - beta * log(random.random())

    dx = ratio_x * (x - CANVAS_CENTER_X)
    dy = ratio_y * (y - CANVAS_CENTER_Y)

    return x - dx, y - dy

def shrink(x, y, ratio):
    force = -1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.6)
    dx = ratio * force * (x - CANVAS_CENTER_X)
    dy = ratio * force * (y - CANVAS_CENTER_Y)

    return x - dx, y - dy

def curve(p):
    return 2 * (2 * sin(4 * p)) / (2 * pi)

class Heart:
    def __init__(self, generate_frame = 20):
        self._points = set() ## Heart Points
        self._edge_diffusion_points = set() ## Edge Diffusion Points
        self._center_diffusion_points = set() ## Center Diffusion Points
        self.all_points = {} ## All Points
        self.build(2000) ## Generate Heart Points
        self.random_halo = 1000 ## Random Halo
        self.generate_frame = generate_frame ## Generate Frame

        for frame in range(generate_frame): ## Generate Frame Points
            self.calc(frame)

    def build(self, number):
        for _ in range(number): ## Generate Heart Points
            t = random.uniform(0, 2 * pi)
            x, y = heart_function(t)
            self._points.add((x, y))

        for _x, _y in list(self._points): ## Generate Edge Diffusion Points
            for _ in range(3): ## Generate Edge Diffusion Points
                x, y = scatter_inside(_x, _y, 0.05)
                self._edge_diffusion_points.add((x, y))

        point_list = list(self._points) ## Generate Center Diffusion Points

        for _ in range(6000): ## Generate Center Diffusion Points
            x, y = random.choice(point_list)
            x, y = scatter_inside(x, y, 0.17)
            self._center_diffusion_points.add((x, y))

    @staticmethod
    def calc_position(x, y, ratio):
        force = 1 / (((x - CANVAS_CENTER_X) ** 2 + (y - CANVAS_CENTER_Y) ** 2) ** 0.520) ## Force of Heart

        ## Move of Heart
        dx = ratio * force * (x - CANVAS_CENTER_X) + random.randint(-1, 1)
        dy = ratio * force * (y - CANVAS_CENTER_Y) + random.randint(-1, 1)

        return x - dx, y - dy

    def calc(self, generate_frame):
        ratio = 10 * curve(generate_frame / 10 * pi) ## Curve of Heart

        ## Halo of Heart
        halo_radius = int(4 + 6 * (1 + curve(generate_frame / 10 * pi))) 
        halo_number = int(3000 + 4000 * abs(curve(generate_frame / 10 * pi) ** 2))

        all_points = [] ## All Points

        heart_halo_point = set() ## Heart Halo Points

        for _ in range(halo_number): ## Generate Heart Halo Diffusion Points
            t = random.uniform(0, 4 * pi)
            x, y = heart_function(t, shrink_ratio = 11.5)
            x, y = shrink(x, y, halo_radius)

            if (x, y) not in heart_halo_point: ## Generate Heart Halo Diffusion Point
                heart_halo_point.add((x, y))
                x += random.randint(-14, 14)
                y += random.randint(-14, 14)
                size = random.choice((1, 2, 2))
                all_points.append((x, y, size))

        for x, y in self._points: ## Generate Heart Points
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 3)
            all_points.append((x, y, size))

        for x, y in self._edge_diffusion_points: ## Generate Edge Diffusion Points
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))

        for x, y in self._center_diffusion_points: ## Generate Center Diffusion Points
            x, y = self.calc_position(x, y, ratio)
            size = random.randint(1, 2)
            all_points.append((x, y, size))

        self.all_points[generate_frame] = all_points ## All Points

    def render(self, render_canvas, render_frame):
        for x, y, size in self.all_points[render_frame % self.generate_frame]: ## Render Heart
            render_canvas.create_rectangle(x, y, x + size, y + size, width = 0, fill = HEART_COLOR) 

def draw(main: Tk, render_canvas: Canvas, render_heart: Heart, render_frame = 0):
    render_canvas.delete('all') ## Clear Canvas
    render_heart.render(render_canvas, render_frame) ## Render Heart
    main.after(160, draw, main, render_canvas, render_heart, render_frame + 1) ## Next Frame

if __name__ == '__main__':
    root = Tk() ## Main Window
    root.title('Beating_heart') ## Main Window Title
    canvas = Canvas(root, bg = 'black', height = CANVAS_HEIGHT, width = CANVAS_WIDTH) ## Main Window Canvas
    canvas.pack() ## Main Window Canvas Pack
    heart = Heart() ## Heart

    draw(root, canvas, heart) ## Draw
    root.mainloop() ## Main Loop