import pygame as pg
import sys

WINDOWSIZE = (800, 800)

pg.init()
window = pg.display.set_mode(WINDOWSIZE)
clock = pg.time.Clock()

def events():
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()

class Circle:
    def __init__(self, pos, r):
        self.pos = pos
        self.r = r
    

    def collidepoint(self, point: tuple[int, int]):
        a, b = delta_pos(self.pos, point)
        return a * a + b * b <= self.r * self.r


    def collidecircle(self, circle):
        a, b = delta_pos(self.pos, circle.pos)
        r = self.r + circle.r
        return a * a + b * b <= r * r


    def collideline(self, line: list[tuple[int, int], tuple[int, int]]):
        x1, y1 = line[0]
        x2, y2 = line[1]
        cx, cy = self.pos
        
        dx = x2 - x1
        dy = y2 - y1
        
        if dx == 0 and dy == 0:
            x, y = cx - x1, cy - y1
            return x * x + y * y <= self.r * self.r, (x1, y1)
        
        t = max(0, min(1, ((cx - x1) * dx + (cy - y1) * dy) / (dx * dx + dy * dy)))
        
        closest_x = x1 + t * dx
        closest_y = y1 + t * dy
        
        x, y = cx - closest_x, cy - closest_y
        collision = x * x + y * y <= self.r * self.r
        
        return collision, (closest_x, closest_y)


    def colliderect(self, rect: pg.Rect):
        cx, cy = self.pos

        closest_x = max(rect.left, min(cx, rect.right))
        closest_y = max(rect.top, min(cy, rect.bottom))

        dx, dy = cx - closest_x, cy - closest_y
        collision = dx * dx + dy * dy <= self.r * self.r

        return collision, (closest_x, closest_y)


def delta_pos(p1, p2):
    x = abs(p1[0] - p2[0])
    y = abs(p1[1] - p2[1])
    return (x, y)


circle = Circle((500, 500), 50)
line = [(200, 200), (600, 600)]
rect = pg.Rect(350, 450, 220, 140)

collision_color = (255, 0, 0)
no_collision_color = (0, 255, 0)

if __name__ == "__main__":
    running = True
    while running:
        clock.tick(60)
        events()
        
        mouse_pos = pg.mouse.get_pos()
        line[1] = mouse_pos
        rect.topleft = mouse_pos
        
        is_colliding, closest_point = circle.collideline(line)
        rect_colliding, rect_closest = circle.colliderect(rect)
        
        window.fill((30, 30, 30))
        
        pg.draw.line(window, (200, 200, 200), *line, 2)

        rect_color = (0, 128, 255) if not rect_colliding else (255, 0, 128)
        pg.draw.rect(window, rect_color, rect, 2)
        
        color = collision_color if is_colliding else no_collision_color
        pg.draw.circle(window, color, circle.pos, circle.r, 2)
        
        pg.draw.circle(window, (255, 255, 0), closest_point, 3)
        pg.draw.circle(window, (0, 255, 255), (int(rect_closest[0]), int(rect_closest[1])), 4)
        
        pg.draw.line(window, (255, 255, 0), circle.pos, closest_point, 1)

        font = pg.font.Font(None, 36)
        status = "COLLISION!" if is_colliding else "No collision"
        text = font.render(status, True, color)
        window.blit(text, (20, 20))
        
        distance_text = font.render(f"Distance: {((circle.pos[0]-closest_point[0])**2 + (circle.pos[1]-closest_point[1])**2) ** 0.5:.2f}", True, (255, 255, 255))
        window.blit(distance_text, (20, 60))
        
        rect_status = "Rect COLLISION" if rect_colliding else "Rect: No collision"
        rect_text = font.render(rect_status, True, rect_color)
        window.blit(rect_text, (20, 100))
        
        pg.display.update()
