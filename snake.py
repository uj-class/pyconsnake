import random
import curses

def rnd(a, b, skip_val=None):
    z = a - 1
    while z < a or (skip_val and z == skip_val):
        z = random.randint(a, b)
    return z

def gain(snake):
    global points, stage, p, q, life
    points += 100 * stage // 2
    snake.append(snake[-1])
    
    p, q = rnd(1, sw-2, p), rnd(1, sh-4, q)
    if life < 9 and points > 2500:
        life += 1
        points -= 2500
    if life * points > stage * 2000 and stage < 9:
        stage += 1
        if life < 9:
            life += 1
        else:
            points += 1000

def loss():
    global life
    life -= 1
    if life <= 0:
        return True
    return False

def display_status():
    w.addstr(sh-3, 0, f"Stage: {stage}")
    w.addstr(sh-2, 0, f"Life: {life}")
    w.addstr(sh-1, 0, f"Points: {points}")

def main(stdscr):
    global p, q, w, sh, sw, points, stage, life
    curses.curs_set(0)
    sh, sw = stdscr.getmaxyx()
    w = curses.newwin(sh, sw, 0, 0)
    w.timeout(100)  # Refresh every 100 milliseconds
    w.keypad(1)
    w.border(0)

    x, y = sw // 4, sh // 4
    snake = [(y, x), (y, x-1), (y, x-2)]
    p, q = rnd(1, sw-2), rnd(1, sh-4)

    direction = curses.KEY_RIGHT
    while True:
        next_key = w.getch()
        direction = direction if next_key == -1 else next_key

        # Get the new head of the snake
        if direction == curses.KEY_DOWN:
            y += 1
        if direction == curses.KEY_UP:
            y -= 1
        if direction == curses.KEY_LEFT:
            x -= 1
        if direction == curses.KEY_RIGHT:
            x += 1

        snake.insert(0, (y, x))
        
        w.addch(q, p, curses.ACS_PI)  # Display food
        
        # Collision with border or self
        if y in [0, sh-1] or \
           x in [0, sw-1] or \
           snake[0] in snake[1:]:
            if loss():
                w.addstr(sh // 2, sw // 2 - 10, "GAME OVER!")
                w.refresh()
                curses.napms(2000)
                break

        # Check if snake has eaten food
        if p == x and q == y:
            gain(snake)
        else:
            tail = snake.pop()
            w.addch(int(tail[0]), int(tail[1]), ' ')

        w.addch(int(snake[0][0]), int(snake[0][1]), curses.ACS_CKBOARD)
        display_status()

    curses.endwin()

# Global Variables
life = 4
points = 0
stage = 1

curses.wrapper(main)
