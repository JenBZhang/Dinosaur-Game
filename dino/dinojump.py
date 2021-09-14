import pygame
import gamebox
camera = gamebox.Camera(800,600)
# movement
dinosaur=gamebox.from_circle(100, 525, 'blue', 10)
#obstacle
cacti_image="cacti1.png"
cacti1=gamebox.from_image(300, 525, cacti_image)
cacti1.scale_by(.05)
cacti2=gamebox.from_image(550, 525, cacti_image)
cacti2.scale_by(.05)
cacti3=gamebox.from_image(950, 525, cacti_image)
cacti3.scale_by(.05)
platform = gamebox.from_color(450, 550, 'gray', 1000, 10)
cacti1.bottom=platform.top
cacti2.bottom=platform.top
cacti3.bottom=platform.top
obstacles = [cacti1,cacti2,cacti3,platform]
dinosaur.bottom=platform.top
#global
gravity=1
jump_speed=15
score=0
scored_since_touch = False
game_on=False
game_end=False

def draw_stats():
  """draws the gameplay information score"""
  scorebox = gamebox.from_text(700,100, "score: " + str(score), 36, 'red')
  camera.draw(scorebox)
def game_start(keys): #hit the up key to start the game
    global game_on
    if pygame.K_UP in keys:
       game_on=True

def move_dinosaur(keys): # this is what does the drawing
    camera.clear('white')
    global scored_since_touch
    for obstacle in obstacles:
        if dinosaur.bottom_touches(obstacle):
            scored_since_touch = False
            if pygame.K_SPACE in keys:
                dinosaur.speedy = -jump_speed
    dinosaur.speedy += gravity
    dinosaur.move_speed()
    for obstacle in obstacles:
        dinosaur.move_to_stop_overlapping(obstacle)
def move_obstacles():# the obstacles keep moving until game over
    if cacti1.right < camera.left:
       cacti1.left = cacti3.right
    if cacti3.right <camera.left:
       cacti3.left =camera .right
    if cacti2.right<camera.left:
       cacti2.left= camera.right
    platform.right=camera.right
    for obstacle in obstacles:
        obstacle.speedx=-8
        obstacle.move_speed()

def scored():# as long as the player playing the game he will earn 5 point with his moving
    global scored_since_touch,score
    if not dinosaur.touches(cacti1) and not dinosaur.touches(cacti2)and not dinosaur.touches(cacti3):
        scored_since_touch = True
        return 5
    return 0

def game_over():
    global game_end,game_on
    if dinosaur.touches(cacti1)or dinosaur.touches(cacti2)or dinosaur.touches(cacti3):
        camera.draw(gamebox.from_text(400, 300, 'Game Over! ', 42, 'red'))
        camera.display()
        game_on=False
        game_end=True
        return True
    return False


def night():# night view when score > 750
    global score
    if score>750:
        camera.clear('black')
def re_draw(keys): # reset the score and cacti position
    global score,game_end
    score=0
    game_end=False
    camera.clear('white')
    game_start(keys)
    draw_stats()
    if game_on==True:
       move_dinosaur(keys)
       move_obstacles()
       score+=scored()
    night()
    cacti1.x=600
    cacti2.x=750
    cacti3.x=1000
    camera.draw(platform)
    #camera.draw(cacti1)
    #camera.draw(cacti2)
    #camera.draw(cacti3)

def restart(keys):
    global game_end
    if game_end == True:
        if pygame.K_SPACE in keys:
            re_draw(keys)
def tick(keys):
    global score
    camera.clear('white')
    restart(keys)
    if game_over():
        return
    if game_on==True:
       move_dinosaur(keys)
       move_obstacles()
       score+=scored()
    night()
    camera.draw(platform)
    camera.draw(dinosaur)
    camera.draw(cacti1)
    camera.draw(cacti2)
    camera.draw(cacti3)
    draw_stats()
    game_start(keys)

    camera.display()


gamebox.timer_loop(30, tick)