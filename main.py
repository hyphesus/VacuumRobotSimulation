import pygame
from map_generation import generate_environment, GRID_SIZE, GRID_WIDTH, GRID_HEIGHT, SCREEN_WIDTH, SCREEN_HEIGHT
from robot_movement import VacuumRobot
from ui import WHITE, draw_environment, draw_robot, draw_button, draw_legend

def main():
    pygame.init()
    # Ekran yüksekliğini buton ve lejant için artır
    extra_height = 150  # Buton ve lejant için ayarlandı
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT + extra_height))
    clock = pygame.time.Clock()

    # Buton metni ve lejant için yazı tipi tanımlar
    font = pygame.font.SysFont(None, 24)

    # Butonun boyutlarını ve pozisyonunu tanımlar
    button_width = 150
    button_height = 40
    button_x = (SCREEN_WIDTH - button_width) // 2
    button_y = SCREEN_HEIGHT + extra_height - button_height - 10  # Butonun altına yerleştir

    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    environment = generate_environment()
    robot = VacuumRobot(environment, GRID_HEIGHT // 2, GRID_WIDTH // 2, GRID_WIDTH, GRID_HEIGHT)

    running = True
    cleaning_complete = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if button_rect.collidepoint(mouse_pos):
                    # Haritayı yeniden oluştur ve robotu sıfırlar
                    environment = generate_environment()
                    robot = VacuumRobot(environment, GRID_HEIGHT // 2, GRID_WIDTH // 2, GRID_WIDTH, GRID_HEIGHT)
                    cleaning_complete = False
                    print("Harita yeniden oluşturuldu!")

        if not cleaning_complete:
            if not robot.explore():
                cleaning_complete = True
                print("Temizlik tamamlandı!")

        screen.fill(WHITE)

        # Ekranda çevreyi çizer
        draw_environment(screen, environment, robot.cleaned, GRID_SIZE)
        # Robotu ekrana çizer
        draw_robot(screen, robot, GRID_SIZE)
        # Lejantı ekrana çizer
        draw_legend(screen, font, GRID_HEIGHT, GRID_SIZE)
        # Butonu ekrana çizer
        draw_button(screen, button_rect, "Haritayı Yeniden Oluştur", font)

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()
