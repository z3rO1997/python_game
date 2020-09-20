import pygame
#####################################################################
# 기본적인 초기화 (반드시 하는 것)
pygame.init() # 초기화 (반드시 필요)

# 화면 크기 설정
screen_width = 480 # 가로
screen_height = 640 # 세로
screen = pygame.display.set_mode((screen_width, screen_height))

# 화면 타이틀 설정
pygame.display.set_caption("my game") # 게임 이름

# FPS
clock = pygame.time.Clock()
#####################################################################


# 1. 사용자 게임 초기화 (배경 화면, 게임 이미지, 좌표, 속도, 폰트 등)

running = True 
while running:
    dt = clock.tick(144) 

    # 2. 이벤트 처리 (키보드, 마우스)
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False 
        
    # 3. 게임 캐릭터 위치 정의

    # 4. 충돌 처리

    # 5. 화면에 그리기

    pygame.display.update() 


# 잠시 대기
pygame.time.delay(2000) # 2초의 대기 (ms)

# pygame 종료
pygame.quit()