# -*- coding: utf-8 -*-
"""Fichier de lancement du jeu"""

import sys
import random
import math
import pygame

from pygame.locals import *

from constants import SCREEN_HEIGHT, SCREEN_WIDTH
from enemy import Enemy
from player import Player


class AirplanWar():
    """Jeu AirplanWar"""

    def initialisation_joueur(self):
        """Initialise les variables en rapport avec le joueur"""
        player_rect = []
        player_rect.append(pygame.Rect(0, 99, 102,126))
        player_rect.append(pygame.Rect(165, 360, 102, 126))
        player_rect.append(pygame.Rect(165, 234, 102, 126))
        player_rect.append(pygame.Rect(330, 624, 102, 126))
        player_rect.append(pygame.Rect(330, 498, 102, 126))
        player_rect.append(pygame.Rect(432, 624, 102, 126))
        player_pos = [200, 600]
        self.player = Player(self.plane_img, player_rect, player_pos)
        self.player_down_index = 16

    def initialisation_game_over(self):
        """Initialise les images du game over"""
        self.game_over = pygame.image.load('resources/image/gameover.png')
        self.game_over_sound = pygame.mixer.Sound('resources/sound/game_over.wav')
        self.game_over_sound.set_volume(0.3)

    def initialisation_enemy(self):
        """Initialise les variable en rapport avec les enemiess"""
        self.enemy1_down_sound = pygame.mixer.Sound('resources/sound/enemy1_down.wav')
        self.enemy1_down_sound.set_volume(0.3)
        self.enemy1_down_imgs = []
        self.enemy1_down_imgs.append(self.plane_img.subsurface(pygame.Rect(267, 347, 57, 43)))
        self.enemy1_down_imgs.append(self.plane_img.subsurface(pygame.Rect(873, 697, 57, 43)))
        self.enemy1_down_imgs.append(self.plane_img.subsurface(pygame.Rect(267, 296, 57, 43)))
        self.enemy1_down_imgs.append(self.plane_img.subsurface(pygame.Rect(930, 697, 57, 43)))
        # Stockez des avions détruits pour le rendu d'animations de sprites d'épaves
        self.enemies_down = pygame.sprite.Group()

        self.enemy1_rect = pygame.Rect(534, 612, 57, 43)
        self.enemy1_img = self.plane_img.subsurface(self.enemy1_rect)
        self.enemies1 = pygame.sprite.Group()
        self.enemy_frequency = 0

    def initialisation_bullet(self):
        """Initialise les variable en rapport avec les balles"""
        self.bullet_sound = pygame.mixer.Sound('resources/sound/bullet.wav')
        self.bullet_sound.set_volume(0.3)
        bullet_rect = pygame.Rect(1004, 987, 9, 21)
        self.bullet_img = self.plane_img.subsurface(bullet_rect)
        self.shoot_frequency = 0

    def __init__(self):
        # pylint: disable=E1101
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Airplane Wars')

        self.background = pygame.image.load('resources/image/background.png')
        self.plane_img = pygame.image.load('resources/image/shoot.png')
        self.initialisation_joueur()
        self.initialisation_game_over()
        self.initialisation_enemy()
        self.initialisation_bullet()
        self.font = pygame.font.SysFont("comicsans", 36)
        self.clock = pygame.time.Clock()
        self.score = 0
        self.running = True
        self.co_background = 0

    def fond_rendu(self):
        """Affiche le fond"""
        self.screen.fill(0)
        self.co_background = (self.co_background+3)%SCREEN_HEIGHT
        self.screen.blit(self.background, (0, self.co_background-SCREEN_HEIGHT))
        self.screen.blit(self.background, (0, self.co_background))
        self.screen.blit(self.font.render(str(self.score), True, "black"), (0,0))

    def apparition_balle(self):
        """fait apparaitre les balles du joueur"""
        if self.shoot_frequency % 15 == 0:
            self.bullet_sound.play()
            self.player.shoot(self.bullet_img)
        self.shoot_frequency += 1
        if self.shoot_frequency >= 15:
            self.shoot_frequency = 0

    def suppression_balle(self):
        """fait disparraitre les balles du joueur lorqu'elles sortent de l'écran"""
        for bullet in self.player.bullets:
            bullet.move()
            if bullet.rect.bottom < 0:
                self.player.bullets.remove(bullet)

    def apparition_enemy(self):
        """fait apparaitre les enemies"""
        if self.enemy_frequency % 50 == 0:
            enemy1_pos = [random.randint(0, SCREEN_WIDTH - self.enemy1_rect.width), 0]
            enemy1 = Enemy(
                self.enemy1_img,
                self.enemy1_down_imgs,  #Ajouter ceci car on a modifie la classe Enemy
                enemy1_pos)
            self.enemies1.add(enemy1)
        self.enemy_frequency += 1
        if self.enemy_frequency >= 100:
            self.enemy_frequency = 0

    def actualisation_enemy(self):
        """actualise les images des enemies / les fait bouger"""
        enemy: Enemy
        for enemy in self.enemies1:
            if self.score <= 20000 :
                enemy.move()
            else:
                enemy.move(
                    (3 / (1 - math.exp(-0.00005 * (self.score + 60000))))
                    * math.log(self.score, 10) - 12
                    )   # La ptn de formule de variation de vitesse
            # Déterminez si le joueur a été touché
            if pygame.sprite.collide_circle_ratio(0.6)(enemy, self.player):
                self.enemies_down.add(enemy)
                self.enemies1.remove(enemy)
                self.player.is_hit = True
                self.game_over_sound.play()
                break
            if enemy.rect.top > SCREEN_HEIGHT:
                self.enemies1.remove(enemy)

    def dessin_joueur(self):
        """dessine le joueur"""
        if not self.player.is_hit:
            self.screen.blit(self.player.image[self.player.img_index], self.player.rect)
            # Changer l'index de l'image pour animer l'avion
            self.player.img_index = self.shoot_frequency // 8
        else:
            self.player.img_index = self.player_down_index // 8
            self.screen.blit(self.player.image[self.player.img_index], self.player.rect)
            self.player_down_index += 1
            if self.player_down_index > 47:
                self.running = False

    def destruction_enemy(self):
        """fait disparaitre l'enemy"""
        enemies1_down = pygame.sprite.groupcollide(self.enemies1, self.player.bullets, 1, 1)
        for enemy_down in enemies1_down:
            self.enemies_down.add(enemy_down)

    def animation_mort_enemy(self):
        """joue l'animation de la destruction d'un enmy"""
        for enemy_down in self.enemies_down:
            if enemy_down.down_index == 0:
                self.enemy1_down_sound.play()
            if enemy_down.down_index > 7:
                self.enemies_down.remove(enemy_down)
                self.score += 1000
                continue
            self.screen.blit(enemy_down.down_imgs[enemy_down.down_index // 2],
                        enemy_down.rect)
            enemy_down.down_index += 1

    def fin(self):
        """permet de quitter l'appli"""
        for event in pygame.event.get():
            # pylint: disable=E1101
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    def gestion_controls(self):
        """bouge le joueur en fonction de la touche pressé"""
        key_pressed = pygame.key.get_pressed()
        # pylint: disable=E0602
        if key_pressed[K_w] or key_pressed[K_UP]:
            self.player.move_up()
        if key_pressed[K_s] or key_pressed[K_DOWN]:
            self.player.move_down()
        if key_pressed[K_a] or key_pressed[K_LEFT]:
            self.player.move_left()
        if key_pressed[K_d] or key_pressed[K_RIGHT]:
            self.player.move_right()

    def changement_vaiseau(self):
        """change le vaisseau"""
        if self.score>=50000 and not self.player.v2:
            player_rect = []
            player_rect.append(pygame.Rect(337,752, 503-337,998-752))
            player_rect.append(pygame.Rect(506, 752, 503-337, 998-752))
            player_rect.append(pygame.Rect(167, 752, 503-337, 998-752))
            player_rect.append(pygame.Rect(841, 752, 503-337, 998-752))
            player_rect.append(pygame.Rect(676, 752, 503-337, 998-752))
            player_rect.append(pygame.Rect(0, 752, 503-337, 998-752))
            self.player.changement_vaiseau(self.plane_img,player_rect)

    def main(self):
        """permet de jouer"""
        while self.running:
            self.fond_rendu()
            self.apparition_balle()
            self.suppression_balle()
            self.apparition_enemy()
            self.actualisation_enemy()
            self.dessin_joueur()
            self.player.bullets.draw(self.screen)
            self.destruction_enemy()
            self.animation_mort_enemy()
            self.changement_vaiseau()
            self.enemies1.draw(self.screen)
            pygame.display.update()
            self.clock.tick(45)
            self.gestion_controls()
            self.fin()
        self.screen.blit(self.game_over, (0, 0))

        while 1:
            self.fin()
            pygame.display.update()

jeu = AirplanWar()
jeu.main()
