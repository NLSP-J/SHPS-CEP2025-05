##Tag##
#importing
import pygame as pg
import random as ran
import time
import asyncio

pg.init()

#colours
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (25, 180, 25)

#screen.init()
win_width = 500
win_height = 575
screen = pg.display.set_mode([win_width, win_height])
pg.display.set_caption("Tag")

font = pg.font.Font(None, 30)

#main game variables
running = True
caught = False
num_rows = 10
col_size = win_width / num_rows
font_width = 3
sqr_width = col_size - font_width
guide_number = 0
a_pos = []
b_pos  = []
tele_pos = []
obs_pos = []

start_time = 0
game_duration = 45000
remaining_time = game_duration
game_start = False

while True:
    for pos in range (2):
        a_pos.append(ran.randint(0, num_rows - 1) * col_size + font_width)
        b_pos.append(ran.randint(0, num_rows - 1) * col_size + font_width)
        tele_pos.append(ran.randint(0, num_rows - 1) * col_size + font_width)

        obs_pos.append(ran.randint(1, num_rows - 2) * col_size + font_width)

    if a_pos != b_pos and a_pos != tele_pos and a_pos != obs_pos:
        if b_pos != tele_pos and b_pos != obs_pos:
            if tele_pos != obs_pos:
                break

a_new_pos = a_pos
b_new_pos = b_pos
##IMPORTANT- col_size is the size of the row/column
##IMPORTANT- a is catcher, b is runner


def update_text(string):
    global font
    TRH = win_height - win_width #text_rect_height

    screen.fill(black, (0, win_height - TRH, win_width, TRH))
    string = font.render(string, True, white)
    text_rect = string.get_rect(center = (win_width / 2, win_height - TRH / 2))
    screen.blit(string, text_rect)
    pg.display.flip()

def game_timer():
    global caught, remaining_time, running
    if caught != True:
        if remaining_time != 0 and remaining_time > 0:
            remaining_time = game_duration - (pg.time.get_ticks() - start_time)
            text = f"Time Left: {remaining_time // 1000}"
            update_text(text)
        else:
            text = "Times up! Blue won! Congrats!"
            update_text(text)
            time.sleep(2)
            running = False
        
def game_window():
    screen.fill(white)
    global sqr_width

    for row in range(num_rows + 1):
        pg.draw.line(screen, black, (0, (col_size) * (row - 1)),
				    (win_width, (col_size) * (row - 1)), font_width + 1)

    for col in range(num_rows + 1):
        pg.draw.line(screen, black, ((col_size) * (col - 1), 0),
	                 ((col_size) * (col - 1), win_height), font_width + 1)
        
    pg.draw.rect(screen, green, ((tele_pos[0], tele_pos[1]), (sqr_width, sqr_width)), width = 10)
    pg.draw.rect(screen, black, ((obs_pos), (sqr_width, sqr_width)))


def update_squares():
    global a_pos, b_pos, tele_pos, running

    if (b_pos == tele_pos) or (a_pos == tele_pos):

        if (b_pos == tele_pos):
            for pos in range (2):
                b_pos[pos - 1] = ran.randint(0, 1) * (num_rows - 1) * col_size + font_width

        elif (a_pos == tele_pos):
            for pos in range (2):
                a_pos[pos - 1] = ran.randint(0, 1) * (num_rows - 1) * col_size + font_width

        pg.draw.rect(screen, white, (tele_pos, (sqr_width, sqr_width)))
        while True:
            for pos in range(2):
                tele_pos[pos] = ran.randint(0, num_rows - 1) * col_size + font_width
            if tele_pos != obs_pos:
                break
        pg.draw.rect(screen, green, (tele_pos, (sqr_width, sqr_width)), width = 10)

    elif a_pos == b_pos:
        text = "Red won! Catcher wins! Congrats!!"
        update_text(text)
        time.sleep(2)
        running = False

    pg.draw.rect(screen, red, ((a_pos), (sqr_width, sqr_width)))
    pg.draw.rect(screen, blue, (b_pos, (sqr_width, sqr_width)))


game_window()
update_squares()
update_text("Click to read the guide")

def check_click():
    global guide_number
    if guide_number != 5 and guide_number < 5:
        guide_number += 1

    if guide_number == 1:
        update_text("Red is catcher, uses WASD")
    elif guide_number == 2:
        update_text("Blue is runner uses arrow keys")

    elif guide_number == 3:
        update_text("Green holo sqrs teleport you to a random corner")
    elif guide_number == 4:
        update_text("Black is obstacle: No going there")
    elif guide_number == 5:
        update_text("READY? Move to start!")

def check():
    global a_pos, b_pos, a_new_pos, b_new_pos
    if (a_new_pos != obs_pos) and (b_new_pos != obs_pos):
        a_pos = a_new_pos
        b_pos = b_new_pos

def shortcut1(x_shift, y_shift):
    global b_new_pos
    b_new_pos = [min(max(font_width, b_pos[0] + x_shift), (col_size * (num_rows - 1) + font_width)), min(max(font_width, b_pos[1] + y_shift), (col_size * (num_rows - 1) + font_width))]

def shortcut2(x_shift, y_shift):
    global a_new_pos
    a_new_pos = [min(max(font_width, a_pos[0] + x_shift), (col_size * (num_rows - 1) + font_width)), min(max(font_width, a_pos[1] + y_shift), (col_size * (num_rows - 1) + font_width))]

def delete_squares():
    global a_pos, b_pos
    pg.draw.rect(screen, white, (a_pos, (sqr_width, sqr_width)))
    pg.draw.rect(screen, white, (b_pos, (sqr_width, sqr_width)))

async def main():
    global running, game_start, start_time
    while running:
        if game_start == True:
            game_timer()
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.MOUSEBUTTONDOWN:
                check_click()
            elif event.type == pg.KEYDOWN and guide_number == 5:
                if game_start == False:
                    game_start = True
                    start_time = pg.time.get_ticks()
                elif game_start == True:
                    delete_squares()

                    if event.key == pg.K_LEFT:
                        shortcut1(-col_size, 0)
                    elif event.key == pg.K_RIGHT:
                        shortcut1(col_size, 0)
                    elif event.key == pg.K_DOWN:
                        shortcut1(0, col_size)
                    elif event.key == pg.K_UP:
                        shortcut1(0, -col_size)

                    if event.key == pg.K_a:
                        shortcut2(-col_size, 0)
                    elif event.key == pg.K_d:
                        shortcut2(col_size, 0)
                    elif event.key == pg.K_w:
                        shortcut2(0, -col_size)
                    elif event.key == pg.K_s:
                        shortcut2(0, col_size)
                    check()
                    update_squares()
            #End If
        #End For

        pg.display.flip()

        await asyncio.sleep(0)

asyncio.run(main())