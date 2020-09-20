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
background = pygame.image.load(os.path.join(image_path, "background.png"))

#스테이지
stage = pygame.image.load(os.path.join(image_path, "stage.png"))
stage_size = stage.get_rect().size
stage_hight = stage_size[1] # 스테이지  높이 위에 캐릭터 배치

# 캐릭터
character = pygame.image.load(os.path.join(image_path, "character.png"))
character_size = character.get_rect().size
character_width = character_size[0]
character_height = character_size[1]
character_x_pos = (screen_width / 2) - (character_width / 2)
character_y_pos = screen_height - stage_hight - character_height

character_to_x = 0
character_speed = 5

# 무기
weapon = pygame.image.load(os.path.join(image_path, "weapon.png"))
weapon_size = weapon.get_rect().size
weapon_width = weapon_size[0]

# 무기는 여러번 발사 가능
weapons = []

# 무기 속도
weapon_spead = 10


running = True 
while running:
    dt = clock.tick(30) 

    # 2. 이벤트 처리 (키보드, 마우스)
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False 
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: #왼쪽
                character_to_x -= character_speed
            elif event.key == pygame.K_RIGHT:  #오른쪽
                character_to_x += character_speed
            elif event.key == pygame.K_SPACE: #스페이스바
                weapon_x_pos = character_x_pos + (character_width / 2) - (weapon_width / 2)
                weapon_y_pos = character_y_pos
                weapons.append([weapon_x_pos, weapon_y_pos])
        
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                character_to_x = 0


    # 3. 게임 캐릭터 위치 정의
    character_x_pos += character_to_x
    
    if character_x_pos < 0:
        character_x_pos = 0
    elif character_x_pos > (screen_width - character_width):
        character_x_pos = (screen_width - character_width)

    # 무기 위치 조정
    weapons = [ [w[0], w[1] - weapon_spead] for w in weapons] # 무기를 위로 발사
    weapons = [ [w[0], w[1]] for w in weapons if w[1] > 0]

    # 4. 충돌 처리

    # 5. 화면에 그리기
    screen.blit(background, (0, 0))

    for weapon_x_pos, weapon_y_pos in weapons:
        screen.blit(weapon, (weapon_x_pos, weapon_y_pos))

    screen.blit(stage, (0, screen_height - stage_hight))
    screen.blit(character, (character_x_pos, character_y_pos))

    


    pygame.display.update() 


# 잠시 대기
#pygame.time.delay(2000) # 2초의 대기 (ms)

# pygame 종료
pygame.quit()