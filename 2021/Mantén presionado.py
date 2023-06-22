import pygame as pg

WIDTH, HEIGHT = 700, 300
WHITE, BLACK = (255, 255, 255), (0, 0, 0)
FPS = 60

def draw_text(window, msg, center, size, color, bold=False, italic=False, bgcolor=None):
    font = pg.font.SysFont('Serif', size)
    text = font.render(msg, True, color, bgcolor)
    rect = text.get_rect(center = center)
    window.blit(text, rect.topleft)
    return text

pg.init()
pg.font.init()
window = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption('Mantén presionada la barra espaciadora')
clock = pg.time.Clock()
counter = 0
counting = False


done = False
while not done:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            done = True

        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                counter = 0
                counting = True

        if event.type == pg.KEYUP:
            if event.key == pg.K_SPACE:
                counting = False

    if counting:
        counter += 1
    draw_time = str(round(counter / FPS, 4))
    draw_time += '0' * (4 - len(draw_time.split('.')[1]))

    window.fill(WHITE)
    draw_text(window,
              draw_time,
              (WIDTH / 2, HEIGHT / 2),
              100,
              BLACK,
              bold=True)
    pg.display.flip()
    clock.tick(FPS)
pg.quit()








