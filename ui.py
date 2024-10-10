import pygame

# Renkler
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (200, 200, 200)

def draw_environment(screen, environment, cleaned, grid_size):
    # Ekrana çevreyi çizer
    for r in range(len(environment)):
        for c in range(len(environment[0])):
            color = WHITE
            if environment[r][c] == 1:
                color = BLACK  # Engeller
            elif (r, c) in cleaned:
                color = GREEN  # Temizlenmiş alanlar
            pygame.draw.rect(screen, color, (c * grid_size, r * grid_size, grid_size, grid_size))

def draw_robot(screen, robot, grid_size):
    # Ekrana robotu çiz
    pygame.draw.rect(screen, BLUE, (robot.col * grid_size, robot.row * grid_size, grid_size, grid_size))

def draw_button(screen, button_rect, text, font):
    # Ekrana butonu çiz
    pygame.draw.rect(screen, GRAY, button_rect)
    pygame.draw.rect(screen, BLACK, button_rect, 2)  # Çerçeve
    text_surf = font.render(text, True, BLACK)
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)

def draw_legend(screen, font, grid_height, grid_size):
    # Lejant metinlerini tanımlar
    legends = [
        ("Robot", BLUE),
        ("Temizlenmiş Yol", GREEN),
        ("Engeller", BLACK)
    ]
    # Lejant için başlangıç pozisyonu verir
    x_start = 10
    y_start = grid_height * grid_size + 10

    for i, (text, color) in enumerate(legends):
        # Renk kutusunu çiz
        rect = pygame.Rect(x_start, y_start + i * 30, 20, 20)
        pygame.draw.rect(screen, color, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)  # Çerçeve

        # Metni render eder
        text_surf = font.render(text, True, BLACK)
        screen.blit(text_surf, (x_start + 30, y_start + i * 30))
