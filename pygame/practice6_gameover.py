import pygame
import os
# 기본적인 초기화 (반드시 하는 것)
pygame.init() # 초기화 (반드시 필요)

# 화면 크기 설정
screen_width = 640 # 가로
screen_height = 480 # 세로
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("shot balloons") # 게임 이름

# FPS
clock = pygame.time.Clock()



# 1. 사용자 게임 초기화 (배경 화면, 게임 이미지, 좌표, 속도, 폰트 등)
current_path = os.path.dirname(__file__) # 현재 파일 위치
image_path = os.path.join(current_path, "images") # images 폴더 위치 반환

#배경
background = pygame.image.load(os.path.join(image_path, "background2.png"))

#스테이지
stage = pygame.image.load(os.path.join(image_path, "stage2.png"))
stage_size = stage.get_rect().size
stage_hight = stage_size[1] # 스테이지  높이 위에 캐릭터 배치

# 캐릭터
character = pygame.image.load(os.path.join(image_path, "character2.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - stage_hight - character_height

character_to_x_LEFT=0
character_to_x_RIGHT=0
character_speed = 5

# 무기
weapon = pygame.image.load(os.path.join(image_path, "weapon2.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# 무기는 여러번 발사 가능
weapons = []

# 무기 속도
weapon_spead = 10

# 공 만들기 (크기에 따라 따로 처리)
ball_images = [
    pygame.image.load(os.path.join(image_path, "balloon1_2.png")),
    pygame.image.load(os.path.join(image_path, "balloon2_2.png")),
    pygame.image.load(os.path.join(image_path, "balloon3_2.png")),
    pygame.image.load(os.path.join(image_path, "balloon4_2.png"))
]

# 공 크기에 따른 최초 스피드
ball_speed_y = [-18, -15, -12, -9]

# 공들
balls = []

balls.append({ #최초의 공 추가
    "pos_x" : 50, # 공 x좌표
    "pos_y" : 50, # 공 y좌표
    "img_idx" : 0, # 공의 이미지 인덱스
    "to_x" : 3, # x축 이동방향 -3은 왼쪽 3은 오른쪽
    "to_y" : -6, # y축 이동방향
    "init_spd_y" : ball_speed_y[0] # 최초 스피드
})

# 사라질 무기, 공 정보 저장
weapon_to_remove = -1
ball_to_remove = -1

#font
game_font = pygame.font.Font(None, 40)
total_time = 99
start_ticks = pygame.time.get_ticks() # 시작 시간

# 게임 종료 메시지
game_result = "Game Over"


running = True 
while running:
    dt = clock.tick(30) 

    # 2. 이벤트 처리 (키보드, 마우스)
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False 
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: #왼쪽
                character_to_x_LEFT -= character_speed
            elif event.key == pygame.K_RIGHT:  #오른쪽
                character_to_x_RIGHT += character_speed
            elif event.key == pygame.K_SPACE: #스페이스바
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT: 
                character_to_x_LEFT = 0
            elif event.key == pygame.K_RIGHT:
                character_to_x_RIGHT = 0




    # 3. 게임 캐릭터 위치 정의
    character_x_pos += character_to_x_LEFT + character_to_x_RIGHT
    
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > (screen_width - character_width):
        character_x_pos = (screen_width - character_width)

    # 무기 위치 조정
    weapons = [ [w[0], w[1] - weapon_spead] for w in weapons] # 무기를 위로 발사
    weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0]

    # 공 위치 정의
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


    # 4. 충돌 처리
    #캐릭터 rect 정보 업데이트
    character_rect = character.get_rect()
    character_rect.left = character_x_pos
    character_rect.top = character_y_pos

    # 공 rect 정보 업데이트
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

                # 가장 작은 공이 아니면 나뉜다
                if ball_img_idx < 3:
                    #현재 공의 정보
                    ball_width = ball_rect.size[0]
                    ball_height = ball_rect.size[1]

                    #나눈 공 정보
                    small_ball_rect = ball_images[ball_img_idx + 1].get_rect()
                    small_ball_width = small_ball_rect.size[0]
                    small_ball_height = small_ball_rect.size[1]

                    # 왼쪽 방향
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2), # 공 x좌표
                        "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2), # 공 y좌표
                        "img_idx" : ball_img_idx + 1, # 공의 이미지 인덱스
                        "to_x" : -3, # x축 이동방향 
                        "to_y" : -6, # y축 이동방향
                        "init_spd_y" : ball_speed_y[ball_img_idx + 1] # 최초 스피드
                    })
                    # 오른쪽 방향
                    balls.append({
                        "pos_x" : ball_pos_x + (ball_width / 2) - (small_ball_width / 2), # 공 x좌표
                        "pos_y" : ball_pos_y + (ball_height / 2) - (small_ball_height / 2), # 공 y좌표
                        "img_idx" : ball_img_idx + 1, # 공의 이미지 인덱스
                        "to_x" : 3, # x축 이동방향 
                        "to_y" : -6, # y축 이동방향
                        "init_spd_y" : ball_speed_y[ball_img_idx + 1] # 최초 스피드
                    })

                break
        else:
            continue
        break


    # 충돌한 공 및 무기 삭제
    if ball_to_remove > -1:
        del balls[ball_to_remove]
        ball_to_remove = -1
    
    if weapon_to_remove > -1:
        del weapons[weapon_to_remove]
        weapon_to_remove = -1

    # 모든 공 삭제 성공
    if len(balls) == 0:
        game_result = "Mission Complete"
        running = False

    # 5. 화면에 그리기
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


    # 시간 계산
    elapsed_time = (pygame.time.get_ticks() - start_ticks) / 1000
    timer = game_font.render("Time : {0}".format(int(total_time - elapsed_time)), True, (0,0,0,))
    screen.blit(timer, (10, 10))

    # 시간 초과
    if total_time - elapsed_time <= 0:
        game_result = "Time Over"
        running = False


    pygame.display.update() 

#게임 오브 메시지 저장
msg = game_font.render(game_result, True, (255, 0, 0))
msg_rect = msg.get_rect(center = (int(screen_width / 2), int(screen_height / 2)))
screen.blit(msg, msg_rect)
pygame.display.update()

# 잠시 대기
pygame.time.delay(2000) # 2초의 대기 (ms)

# pygame 종료
pygame.quit()