import pygame
import sys
pygame.init()

WIDTH, HEIGHT = 1000, 750
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
pygame.display.set_caption("Game Rpg")

WHITE = (255, 255, 255)
GREEN = (34, 139, 34)
font = pygame.font.Font(None, 36)

class Obstacle:
    def __init__(self, x, y, w, h):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = (50, 50, 50) # Abu-abu gelap

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class Entity:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, 50, 50)
        self.color = color
        self.speed = 2
        self.name = "Player"

    def move(self, keys, obstacles):
        # Simpan posisi lama
        old_x = self.rect.x
        old_y = self.rect.y

        # Gerak Horizontal
        if keys[pygame.K_LEFT]:  self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]: self.rect.x += self.speed
        
        # Cek tabrakan horizontal
        for obj in obstacles:
            if self.rect.colliderect(obj.rect):
                self.rect.x = old_x 

        # Gerak Vertikal
        if keys[pygame.K_UP]:    self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:  self.rect.y += self.speed
        
        # Cek tabrakan vertikal
        for obj in obstacles:
            if self.rect.colliderect(obj.rect):
                self.rect.y = old_y 

        # BATAS LAYAR 
        if self.rect.left < 0: self.rect.left = 0
        if self.rect.right > 1000: self.rect.right = 1000
        if self.rect.top < 0: self.rect.top = 0
        if self.rect.bottom > 750: self.rect.bottom = 750

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class NPC(Entity):
    def __init__(self, x, y, message):
        super().__init__(x, y, (200, 200, 0))
        self.message = message

    def talk(self):
        return self.message

class Treasure(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, (139, 69, 19))
        self.is_collected = False 

    def interact(self):
        self.is_collected = True
        return "Kamu mendapatkan peti"

# Inisialisasi Objek
player = Entity(10, 10, (0, 0, 255))
villager = NPC(940, 10, "Ambil peti itu dan bawa kembali ke sini!")
treasure = Treasure(870, 505)

# Daftar rintangan (Map)
tembok_list = [
    Obstacle(0, 0, 1000, 10),      # Batas atas map
    Obstacle(0, 740, 1000, 10),    # Batas bawah map
    Obstacle(0, 0, 10, 750),       # Batas kiri map
    Obstacle(990, 0, 10, 750),     # Batas kanan map

    Obstacle(0, 350, 200, 10),
    Obstacle(260, 350, 750, 10),
    Obstacle(160, 420, 770, 10),
    Obstacle(160, 490, 120, 10),
    Obstacle(340, 490, 800, 10),
    Obstacle(70, 490, 10, 200),
    Obstacle(160, 490, 10, 200),
    Obstacle(240, 560, 690, 10), 
    Obstacle(850, 490, 10, 70),
    Obstacle(500, 620, 700, 10), 
    Obstacle(160, 620, 280, 10),
    Obstacle(160, 680, 700, 10), 
    Obstacle(920, 680, 80, 10),
    Obstacle(70, 420, 30, 10),
    Obstacle(70, 420, 10, 80),
    Obstacle(10, 490, 60, 10),
]

active_message = ""

running = True
while running:
    screen.fill(GREEN) # Background Rumput
    
    # --- EVENT HANDLING ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            
            # Logika Tombol Spasi (Hanya ditulis 1 kali)
            if event.key == pygame.K_SPACE:
                
                # 1. Interaksi dengan NPC Villager
                if player.rect.inflate(30, 30).colliderect(villager.rect):
                    # Cek apakah peti sudah diambil
                    if treasure.is_collected:
                        active_message = "Misi telah selesai!"
                        
                        # Render kotak dialog seketika agar pesan muncul sebelum game freeze
                        text_surf = font.render(active_message, True, WHITE)
                        pygame.draw.rect(screen, (0, 0, 0), (50, 500, 700, 60))
                        screen.blit(text_surf, (70, 520))
                        pygame.display.flip()
                        
                        pygame.time.delay(3000) # Jeda 3 detik
                        running = False         # Keluar dari game loop
                    else:
                        active_message = villager.talk()
                
                # 2. Interaksi dengan PETI (Hanya jika belum diambil)
                elif not treasure.is_collected and player.rect.inflate(30, 30).colliderect(treasure.rect):
                    active_message = treasure.interact()
                
                # 3. Jika tidak dekat siapa-siapa
                else:
                    active_message = ""

    # UPDATE LOGIKA PERGERAKAN
    keys = pygame.key.get_pressed()
    
    # Gabungkan semua rintangan saat ini
    current_obstacles = tembok_list + [villager]
    if not treasure.is_collected:
        current_obstacles.append(treasure)
        
    player.move(keys, current_obstacles)

    # RENDERING (MENGGAMBAR KE LAYAR)
    for obstacle in tembok_list:
        obstacle.draw(screen)
    
    villager.draw(screen)
    
    if not treasure.is_collected:
        treasure.draw(screen)
        
    player.draw(screen)

    # UI Dialog
    if active_message:
        text_surf = font.render(active_message, True, WHITE)
        pygame.draw.rect(screen, (0, 0, 0), (50, 500, 700, 60)) # Box Dialog
        screen.blit(text_surf, (70, 520))
    
    pygame.display.flip()
    clock.tick(60) 

pygame.quit()
sys.exit()