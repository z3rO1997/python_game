import pygame
import os
#Basic init (must do)
pygame.init() # init

#Screen size setting
screen_width = 640 # width
screen_height = 480 # height
screen = pygame.display.set_mode((screen_width, screen_height))

#Screen title setting
pygame.display.set_caption("shot balloons")#game name

#FPS
clock = pygame.time.Clock()



# User game init (background, game image, location, speed, font, etc.)
current_path = os.path.dirname(__file__)#Current file location
image_path = os.path.join(current_path, "images")#images Return folder location

#background
background = pygame.image.load(os.path.join(image_path, "background2.png"))

#stage
stage = pygame.image.load(os.path.join(image_path, "stage2.png"))
stage_size = stage.get_rect().size
stage_hight = stage_size[1]

#Character
character = pygame.image.load(os.path.join(image_path, "character2.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - stage_hight - character_height

character_to_x_LEFT=0
character_to_x_RIGHT=0
character_speed = 5

#weapon
weapon = pygame.image.load(os.path.join(image_path, "weapon2.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

weapons = []
weapon_spead = 10

#ball (separately to size)
ball_images = [
    pygame.image.load(os.path.join(image_path, "balloon1_2.png")),
    pygame.image.load(os.path.join(image_path, "balloon2_2.png")),
    pygame.image.load(os.path.join(image_path, "balloon3_2.png")),
    pygame.image.load(os.path.join(image_path, "balloon4_2.png"))
]

#speed on size
ball_speed_y = [-18, -15, -12, -9]
balls = []

balls.append({#Add first ball
    "pos_x" : 50,#Ball x location
    "pos_y" : 50,#Ball y location
    "img_idx" : 0,#Ball image index
    "to_x" : 3,#x move -3 is left and 3 is right
    "to_y" : -6,#y move 
    "init_spd_y" : ball_speed_y[0]#init speed
})

#remove disappear, ball
weapon_to_remove = -1
ball_to_remove = -1

#font
game_font = pygame.font.Font(None, 40)
total_time = 99
start_ticks = pygame.time.get_ticks()#Start time 

#message
game_result = "Game Over"


running = True 
while running:
    dt = clock.tick(30) 

    #Event handling
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False 
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:#left
                character_to_x_LEFT -= character_speed
            elif event.key == pygame.K_RIGHT:#right
                character_to_x_RIGHT += character_speed
            elif event.key == pygame.K_SPACE:#spacebar
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT: 
                character_to_x_LEFT = 0
            elif event.key == pygame.K_RIGHT:
                character_to_x_RIGHT = 0




    #Character location
    character_x_pos += character_to_x_LEFT + character_to_x_RIGHT
    
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > (screen_width - character_width):
        character_x_pos = (screen_width - character_width)

    #weapons location
    weapons = [ [w[0], w[1] - weapon_spead] for w in weapons] # shot weapons 
    weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0]

    #ball location
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_size = ball_images[ball_img_idx].get_rect().size
        ball_width = ball_size[0]
        ball_height = ball_size[1]

        if ball_pos_x < 0 or ball_pos_x > screen_width - ball_width:
            ball_val["to_x"] = ball_val["to_x"] * -1
        
        if ball_pos_y >= screen_height - stage_hight - ball_height:
            ball_val["to_y"] = ball_val["init_spd_y"]
        else:
            ball_val["to_y"] += 0.5
        
        ball_val["pos_x"] += ball_val["to_x"]
        ball_val["pos_y"] += ball_val["to_y"]


    #Conflict handling
    #character_rect update
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    #ball_rect update
    for ball_idx, ball_val in enumerate(balls):
        ball_pos_x = ball_val["pos_x"]
        ball_pos_y = ball_val["pos_y"]
        ball_img_idx = ball_val["img_idx"]

        ball_rect = ball_images[ball_img_idx].get_rect()
        ball_rect.left = ball_pos_x
        ball_rect.top = ball_pos_y

        if character_rect.colliderect(ball_rect):
            running = False
        
        for w_idx, w_val in enumerate(weapons):
            weapon_pos_x = w_val[0]
            weapon_pos_y = w_val[1]

            weapon_rect = weapon.get_rect()
            weapon_rect.left = weapon_pos_x
            weapon_rect.top = weapon_pos_y

            if weapon_rect.colliderect(ball_rect):
                weapon_to_remove = w_idx
                ball_to_remove = ball_idx

                # division ball
                if ball_img_idx < 3:
                    #ball infor
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    #divid ball infor
                    small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    #left
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
                        "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
                        "img_idx" : ball_img_idx + 1,
                        "to_x" : -3, 
                        "to_y" : -6,
                        "init_spd_y" : ball_speed_y[ball_img_idx + 1]
                    })
                    #right
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2),
                        "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2),
                        "img_idx" : ball_img_idx + 1,
                        "to_x" : 3,
                        "to_y" : -6,
                        "init_spd_y" : ball_speed_y[ball_img_idx + 1]
                    })

                break
        else:
            continue
        break


    #Delete collided balls and weapons
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1
    
    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    #shot all balls
    if len(balls) == 0:
        game_result = "Mission Complete"
        running = False

    #bulid screen
    screen.blit(background, (0, 0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    for idx, val in enumerate(balls):
        ball_pos_x = val["pos_x"]
        ball_pos_y = val["pos_y"]
        ball_img_idx = val["img_idx"]
        screen.blit(ball_images[ball_img_idx], (ball_pos_x, ball_pos_y))
    screen.blit(stage, (0, screen_height - stage_hight))
    screen.blit(character, (character_x_pos, character_y_pos))


    #Time calculation
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = game_font.render("Time : {0}".format(int(total_time - elapsed_time)), True, (0,0,0,))
    screen.blit(timer, (10, 10))

    #Time out
    if total_time - elapsed_time <= 0:
        game_result = "Time Over"
        running = False


    pygame.display.update() 

#bulid Game over Messages
msg = game_font.render(game_result, True, (255, 0, 0))
msg_rect = msg.get_rect(center = (int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg, msg_rect)
pygame.display.update()

# delay
pygame.time.delay(2000) # 2scond (ms)

# pygame End
pygame.quit()