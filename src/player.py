"""Classe du joueur"""
import pygame
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Player(pygame.sprite.Sprite):
    """Classe joueur qui correspond au vaisseau"""

    def __init__(self, plane_img, player_rect, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = [
            plane_img.subsurface(img).convert_alpha() for img in player_rect
        ]  # List of pictures of player object wizard
        self.rect = player_rect[
            0]  # Initialize the rectangle where the picture is located
        self.rect.topleft = init_pos  # Initialize the upper left corner coordinates of the rectangl
        self.speed = 8  # Initialize the player speed, here is a definite value.
        self.img_index = 0  # Player Wizard Image Index
        self.bullets = pygame.sprite.Group(
        )  # Collection of bullets fired by the player's aircraft
        self.is_hit = False  # Is the player hit?
        self.v2 = False

    def move_up(self):
        """Déplace le joueur vers le haut"""
        if self.rect.top <= 0:
            self.rect.top = 0
        else:
            self.rect.top -= self.speed

    def move_down(self):
        """Déplace le joueur vers le bas"""
        if self.rect.top >= SCREEN_HEIGHT - self.rect.height:
            self.rect.top = SCREEN_HEIGHT - self.rect.height
        else:
            self.rect.top += self.speed

    def move_left(self):
        """Déplace le joueur vers la gauche"""
        if self.rect.left <= 0:
            self.rect.left = 0
        else:
            self.rect.left -= self.speed

    def move_right(self):
        """Déplace le joueur vers la droite"""
        if self.rect.left >= SCREEN_WIDTH - self.rect.width:
            self.rect.left = SCREEN_WIDTH - self.rect.width
        else:
            self.rect.left += self.speed

    def shoot(self, bullet_img):
        """Tire une balle"""
        if self.v2:
            pos:pygame.Rect = self.rect.copy()
            pos.left += 23
            bullet = Bullet(bullet_img,pos.topleft)
            self.bullets.add(bullet)
            pos.left -= 46
            bullet = Bullet(bullet_img,pos.topright)
            self.bullets.add(bullet)
        else :
            bullet = Bullet(bullet_img, self.rect.midtop)
            self.bullets.add(bullet)

    def changement_vaiseau(self,plane_img,player_rect):
        """change le vaisseau"""
        self.image = [
            plane_img.subsurface(img).convert_alpha() for img in player_rect
        ]
        player_rect[0].left = self.rect.left
        player_rect[0].top = self.rect.top
        self.rect = player_rect[0]
        self.v2 = True

class Bullet(pygame.sprite.Sprite):
    """Classe Bullet qui correspond à une balle"""

    def __init__(self, bullet_img, init_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.rect = self.image.get_rect()
        self.rect.midbottom = init_pos
        self.speed = 10

    def move(self):
        """Fait avancé la balle vers le haut"""
        self.rect.top -= self.speed
