import pygame, math, random

pygame.init()
size = [500, 900]
screen = pygame.display.set_mode(size)
title = "HANGMAN"
pygame.display.set_caption(title)
clock = pygame.time.Clock()
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

hint_font = pygame.font.Font("C:/Windows/Fonts/arial.ttf", 80)
entry_font = pygame.font.Font("C:/Windows/Fonts/arial.ttf", 60)
no_font = pygame.font.Font("C:/Windows/Fonts/arial.ttf", 40)
game_over_font = pygame.font.Font(None, 100)

def tup_r(tup):
    temp_list = []
    for a in tup:
        temp_list.append(round(a))
    return tuple(temp_list)

entry_text = ""
drop = False
enter_go = False
exit = False
game_over = False
game_clear = False  # 게임 클리어 여부를 나타내는 변수 추가

f = open("voca.txt", "r", encoding='UTF-8')
raw_data = f.read()
f.close()
data_list = raw_data.split("\n")
data_list = data_list[:-1]

while True:
    r_index = random.randrange(0, len(data_list))
    word = data_list[r_index].replace(u"\xa0", u" ").split(" ")[1]
    if len(word) <= 6:
        break

word = word.upper()
word_show = "_" * len(word)
try_num = 0
ok_list = []
no_list = []
k = 0

while not exit:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit = True
        if not game_over and not game_clear:  # 게임 종료되지 않은 경우와 게임 클리어되지 않은 경우에만 키 입력 처리
            if event.type == pygame.KEYDOWN:
                key_name = pygame.key.name(event.key)
                if (key_name == "return" or key_name == "enter"):
                    if entry_text != "" and (ok_list + no_list).count(entry_text) == 0:
                        enter_go = True
                elif len(key_name) == 1:
                    if (ord(key_name) >= 65 and ord(key_name) <= 90) or (
                            ord(key_name) >= 97 and ord(key_name) <= 122):
                        entry_text = key_name.upper()
                    else:
                        entry_text = ""
                else:
                    entry_text = ""

    if try_num == 8:
        k += 1
    if enter_go == True:
        ans = entry_text
        result = word.find(ans)
        if result == -1:
            try_num += 1
            no_list.append(ans)
        else:
            ok_list.append(ans)
            for i in range(len(word)):
                if word[i] == ans:
                    word_show = word_show[:i] + ans + word_show[i+1:]
        enter_go = False
        entry_text = ""

    screen.fill(black)
    A = tup_r((0, size[1] * 2 / 3))
    B = (size[0], A[1])
    C = tup_r((size[0] / 6, A[1]))
    D = (C[0], C[0])
    E = tup_r((size[0] / 2, D[1]))
    pygame.draw.line(screen, white, A, B, 3)
    pygame.draw.line(screen, white, C, D, 3)
    pygame.draw.line(screen, white, D, E, 3)
    F = tup_r((E[0], E[1] + size[0] / 6))
    if drop == False:
        pygame.draw.line(screen, white, E, F, 3)
    r_head = round(size[0] / 12)
    if drop == True:
        G = (F[0], E[1] + r_head + k * 10)
    else:
        G = (F[0], F[1] + r_head)
    if try_num >= 1:
        pygame.draw.circle(screen, white, tup_r(G), r_head, 3)
    H = (G[0], G[1] + r_head)
    I = (H[0], H[1] + r_head)
    if try_num >= 2:
        pygame.draw.line(screen, white, H, I, 3)
    l_arm = r_head * 2
    J = (I[0] - l_arm * math.cos(30 * math.pi / 180), I[1] - l_arm * math.sin(30 * math.pi / 180))
    K = (I[0] + l_arm * math.cos(30 * math.pi / 180), I[1] + l_arm * math.sin(30 * math.pi / 180))
    J = tup_r(J)
    K = tup_r(K)
    if try_num >= 3:
        pygame.draw.line(screen, white, I, J, 3)
    if try_num >= 4:
        pygame.draw.line(screen, white, I, K, 3)
    L = (I[0], I[1] + l_arm)
    if try_num >= 5:
        pygame.draw.line(screen, white, I, L, 3)
    l_leg = round(l_arm * 1.5)
    M = (L[0] - l_arm * math.cos(60 * math.pi / 180), L[1] - l_arm * math.sin(60 * math.pi / 180))
    N = (L[0] + l_arm * math.cos(30 * math.pi / 180), L[1] + l_arm * math.sin(30 * math.pi / 180))
    M = tup_r(M)
    N = tup_r(N)
    if try_num >= 6:
        pygame.draw.line(screen, white, L, M, 3)
    if try_num >= 7:
        pygame.draw.line(screen, white, L, N, 3)
    if drop == False and try_num == 8:
        O = tup_r((size[0] / 2 - size[0] / 6, E[1] / 2 + F[1] / 2))
        P = (O[0] + k * 2, O[1])
        if P[0] > size[0] / 2 + size[0] / 6:
            P = tup_r((size[0] / 2 + size[0] / 6, O[1]))
            drop = True
            k = 0
        pygame.draw.line(screen, white, O, P, 3)

    hint = hint_font.render(word_show, True, white)
    hint_size = hint.get_size()
    hint_pos = tup_r((size[0] / 2 - hint_size[0] / 2, size[1] * 5 / 6 - hint_size[1] / 2))
    screen.blit(hint, hint_pos)

    entry_bg_size = 80
    entry_bg_rect = pygame.Rect(size[0] / 2 - entry_bg_size / 2, size[1] * 17 / 18 - entry_bg_size / 2, entry_bg_size,
                                entry_bg_size)
    pygame.draw.rect(screen, white if not game_over else black, entry_bg_rect)

    entry = entry_font.render(entry_text, True, black)
    entry_size = entry.get_size()
    entry_pos = tup_r((size[0] / 2 - entry_size[0] / 2, size[1] * 17 / 18 - entry_size[1] / 2))
    screen.blit(entry, entry_pos)

    no_text = " ".join(no_list)
    no = no_font.render(no_text, True, red)
    no_pos = tup_r((20, size[1] * 2 / 3 + 20))
    screen.blit(no, no_pos)

    if try_num == 8:
        game_over = True
        game_over_text = game_over_font.render("GAME OVER", True, red)
        game_over_size = game_over_text.get_size()
        game_over_pos = tup_r((size[0] / 2 - game_over_size[0] / 2, size[1] / 2 - game_over_size[1] / 2))
        screen.blit(game_over_text, game_over_pos)

    if "_" not in word_show:  # 성공 조건: 단어를 모두 맞춘 경우
        game_clear = True
        game_clear_text = game_over_font.render("GAME CLEAR", True, (0, 128, 0))  # 초록색으로 표시
        game_clear_size = game_clear_text.get_size()
        game_clear_pos = tup_r((size[0] / 2 - game_clear_size[0] / 2, size[1] / 2 - game_clear_size[1] / 2))
        screen.blit(game_clear_text, game_clear_pos)

    pygame.display.flip()

pygame.quit()

