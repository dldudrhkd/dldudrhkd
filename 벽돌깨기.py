import pygame
import random
import time

pygame.init()

# 색깔
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BROWN = (139, 69, 19)
YELLOW = (255, 255, 0)

# 폰트
large_font = pygame.font.SysFont(None, 72)
small_font = pygame.font.SysFont(None, 36)

# 화면 크기
screen_width = 600
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

clock = pygame.time.Clock()

# 배경음악 파일 로드 및 재생
pygame.mixer.music.load('background_music.mp3')
pygame.mixer.music.play(-1)  # 무한 반복 재생

# 성공 및 실패 음악 파일 로드
success_music = 'success_music.mp3'
failure_music = 'failure_music.mp3'

def runGame():
    score = 100  # 시작 점수
    missed = 0
    SUCCESS = 1
    FAILURE = 2
    game_over = 0

    start_time = time.time()  # 타이머 시작 시간
    score_decay_timer = 1.0  # 점수 감소 시간

    bricks = []
    COLUMN_COUNT = 8
    ROW_COUNT = 7
    for column_index in range(COLUMN_COUNT):
        for row_index in range(ROW_COUNT):
            brick = pygame.Rect(column_index * (60 + 10) + 35, row_index * (16 + 5) + 35, 60, 16)
            bricks.append(brick)

    balls = [pygame.Rect(screen_width // 2 - 16 // 2, screen_height // 2 - 16 // 2, 16, 16)]
    ball_speeds = [(10, -10)]  # 공 속도
    paddle = pygame.Rect(screen_width // 2 - 80 // 2, screen_height - 30, 80, 16)
    paddle_dx = 0
    paddle_speed = 15  # 패들 속도

    items = []  # 아이템 리스트

    running = True
    while running:
        clock.tick(30)
        screen.fill(BLACK)

        # 시간 계산
        elapsed_time = time.time() - start_time

        # 점수 감소
        score_decay_timer -= 1 / 30  # 매 프레임마다 타이머 감소(30FPS로 가정)
        if score_decay_timer <= 0:
            score_decay_timer = 1.0  # 타이머 재설정
            if score > 0:
                score -= 1  # 1점씩 감소

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    paddle_dx = -paddle_speed
                elif event.key == pygame.K_RIGHT:
                    paddle_dx = paddle_speed
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    paddle_dx = 0

        paddle.left += paddle_dx

        for i, ball in enumerate(balls):
            ball.left += ball_speeds[i][0]
            ball.top += ball_speeds[i][1]

            if ball.left <= 0:
                ball.left = 0
                ball_speeds[i] = (-ball_speeds[i][0], ball_speeds[i][1])
            elif ball.left >= screen_width - ball.width:
                ball.left = screen_width - ball.width
                ball_speeds[i] = (-ball_speeds[i][0], ball_speeds[i][1])
            if ball.top < 0:
                ball.top = 0
                ball_speeds[i] = (ball_speeds[i][0], -ball_speeds[i][1])
            elif ball.top >= screen_height:
                missed += 1
                ball.left = screen_width // 2 - ball.width // 2
                ball.top = screen_height // 2 - ball.width // 2
                ball_speeds[i] = (ball_speeds[i][0], -ball_speeds[i][1])

            if missed >= 7:
                game_over = FAILURE
                score = 0  # 실패 시 점수를 0으로 설정

            if paddle.left < 0:
                paddle.left = 0
            elif paddle.left > screen_width - paddle.width:
                paddle.left = screen_width - paddle.width

            for brick in bricks[:]:
                if ball.colliderect(brick):
                    bricks.remove(brick)
                    ball_speeds[i] = (ball_speeds[i][0], -ball_speeds[i][1])
                    score += 1
                    # 일정확률로 아이템 드랍
                    if random.random() < 0.5:  # 아이템 50% 확률로 떨굼
                        # 아이템 확률
                        item_type = random.choices(
                             ['slow', 'big', 'fast', 'small', 'extra_ball', 'paddle_lengthen'],
                            weights=[1, 1, 0.5, 0.3, 1, 0.2],
                            k=1
                        )[0]
                        item = {'rect': pygame.Rect(brick.left, brick.top, 20, 20), 'type': item_type}
                        items.append(item)
                    break

            if ball.colliderect(paddle):
                ball_speeds[i] = (ball_speeds[i][0], -ball_speeds[i][1])
                ball_speeds[i] = (10 if ball.centerx > paddle.centerx else -10, ball_speeds[i][1])

        if len(bricks) == 0:
            game_over = SUCCESS

        for item in items[:]:
            item['rect'].top += 5  # 아이템 떨어지는 속도
            if item['rect'].colliderect(paddle):
                if item['type'] == 'slow':
                    for j in range(len(ball_speeds)):
                        ball_speeds[j] = (abs(ball_speeds[j][0]) + 5 if ball_speeds[j][0] > 0 else -(abs(ball_speeds[j][0]) + 5),
                                          abs(ball_speeds[j][1]) + 5 if ball_speeds[j][1] > 0 else -(abs(ball_speeds[j][1]) + 5))
                elif item['type'] == 'small':
                    for ball in balls:
                        ball.inflate_ip(-8, -8)  # 공 크기 줄이기
                elif item['type'] == 'extra_ball':
                    new_ball = pygame.Rect(paddle.centerx - 8, paddle.top - 16, 16, 16)
                    balls.append(new_ball)
                    ball_speeds.append((random.choice([10, -10]), -10))
                elif item['type'] == 'paddle_lengthen':
                    paddle.width += 40  # 패들 길이 늘리기
                    paddle.left -= 20
                items.remove(item)
            elif item['rect'].top > screen_height:
                items.remove(item)

        # 블럭 그리기
        for brick in bricks:
            pygame.draw.rect(screen, GREEN, brick)

        # 공 그리기
        if game_over == 0:
            for ball in balls:
                pygame.draw.circle(screen, WHITE, ball.center, ball.width // 2)  # Draw ball with proper radius

        # 패들 그리기
        pygame.draw.rect(screen, BLUE, paddle)

        # 아이템 그리기
        for item in items:
            color = (BROWN if item['type'] == 'slow' else
                     RED if item['type'] == 'big' else
                     YELLOW if item['type'] == 'fast' else
                     GREEN if item['type'] == 'small' else
                     BLUE if item['type'] == 'paddle_lengthen' else
                     WHITE)
            pygame.draw.rect(screen, color, item['rect'])

        # 놓친 공을 기준으로 최종 점수 계산
        final_score = score - missed * 5 if missed > 0 else score

        # 추첨 점수 및 놓친 횟수
        score_image = small_font.render('Point {}'.format(final_score), True, YELLOW)
        screen.blit(score_image, (10, 10))

        missed_image = small_font.render('Missed {}'.format(missed), True, YELLOW)
        screen.blit(missed_image, missed_image.get_rect(right=screen_width - 10, top=10))

        # 경과 시간
        time_image = small_font.render('Time {:.1f}s'.format(elapsed_time), True, YELLOW)
        screen.blit(time_image, time_image.get_rect(centerx=screen_width // 2, top=10))

        # 점수가 0점일 때 게임 종료
        if score <= 0:
            game_over = FAILURE

        # 메시지
        if game_over > 0:
            pygame.mixer.music.stop()  # 배경음악 정지
            if game_over == SUCCESS:
                pygame.mixer.music.load(success_music)
                pygame.mixer.music.play()
                success_image = large_font.render('Success', True, GREEN)
                screen.blit(success_image, success_image.get_rect(centerx=screen_width // 2, centery=screen_height // 2))
            elif game_over == FAILURE:
                pygame.mixer.music.load(failure_music)
                pygame.mixer.music.play()
                failure_image = large_font.render('Failure', True, RED)
                screen.blit(failure_image, failure_image.get_rect(centerx=screen_width // 2, centery=screen_height // 2))

            # 최종 점수 표시
            final_score_image = large_font.render('Final Score: {}'.format(final_score), True, WHITE)
            screen.blit(final_score_image, final_score_image.get_rect(centerx=screen_width // 2, centery=screen_height // 2 + 100))

            pygame.display.update()
            time.sleep(3)
            running = False

        pygame.display.update()

runGame()
pygame.quit()
