# this file was created by: Tyler Marshall
# this code inspired by Zelda and informed by Chris Bradfield


import pygame as pg
from settings import *
from utils import *
from random import choice
from os import path

vec = pg.math.Vector2

# making it impossible for the player to go through walls
def collide_with_walls(sprite, group, dir):
    if dir == 'x':
        hits = pg.sprite.spritecollide(sprite, group, False)
        if hits:
            if hits[0].rect.centerx > sprite.rect.centerx:
                sprite.pos.x = hits[0].rect.left - sprite.rect.width / 2
            if hits[0].rect.centerx < sprite.rect.centerx:
                sprite.pos.x = hits[0].rect.right + sprite.rect.width / 2
            sprite.vel.x = 0
            sprite.rect.centerx = sprite.pos.x
    if dir == 'y':
        hits = pg.sprite.spritecollide(sprite, group, False)
        if hits:
            if hits[0].rect.centery > sprite.rect.centery:
                sprite.pos.y = hits[0].rect.top - sprite.rect.height / 2
            if hits[0].rect.centery < sprite.rect.centery:
                sprite.pos.y = hits[0].rect.bottom + sprite.rect.height / 2
            sprite.vel.y = 0
            sprite.rect.centery = sprite.pos.y

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        # init super class
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        # self.image = pg.Surface((TILESIZE, TILESIZE))
        # added player image to sprite from the game class...
        self.image = game.player_img
        # self.image.fill(GREEN)
        self.rect = self.image.get_rect()
        self.vx, self.vy = 0, 0
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.moneybag = 0
        self.speed = 300
        self.status = ""
        self.hitpoints = 100
        self.cooling = False
        self.pos = vec(self.x, self.y)
        self.vaulthit = 0   

    def get_keys(self):
        self.vx, self.vy = 0, 0 
        keys = pg.key.get_pressed()
        if keys[pg.K_t]:
            self.game.test_method()
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vx = -self.speed
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vx = self.speed
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vy = -self.speed  
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vy = self.speed
        if keys[pg.K_e]:
            print("trying to shoot...")
            self.pew()
        if self.vx != 0 and self.vy != 0:
            self.vx *= 0.7071
            self.vy *= 0.7071
    
    def pew(self):
        p = PewPew(self.game, self.rect.x, self.rect.y)
        print(p.rect.x)
        print(p.rect.y)

    def move(self, dx=0, dy=0):
        if not self.collide_with_walls(dx, dy):
            self.x += dx
            self.y += dy

    def collide_with_walls(self, dx=0, dy=0):
        for wall in self.game.walls:
            if wall.x == self.x + dx and wall.y == self.y + dy:
                return True
        return False
            
    def collide_with_walls_dir(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vx > 0:
                    self.x = hits[0].rect.left - self.rect.width
                if self.vx < 0:
                    self.x = hits[0].rect.right
                self.vx = 0
                self.rect.x = self.x
        if dir == 'y':
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vy > 0:
                    self.y = hits[0].rect.top - self.rect.height
                if self.vy < 0:
                    self.y = hits[0].rect.bottom
                self.vy = 0
                self.rect.y = self.y
    
    # made possible by Aayush's question!
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin":
                self.moneybag += 1
            if str(hits[0].__class__.__name__) == "PowerUp":
                print(hits[0].__class__.__name__)
                effect = choice(POWER_UP_EFFECTS)
                self.game.cooldown.cd = 5
                self.cooling = True
                print(effect)
                print(self.cooling)
                if effect == "Invincible":
                    self.status = "Invincible"
            if str(hits[0].__class__.__name__) == "Mob":
                # print(hits[0].__class__.__name__)
                # print("Collided with mob")
                # self.hitpoints -= 1
                if self.status == "Invincible":
                    print("you can't hurt me")
            
    def die(self):
        # Handle player death here
        # For example, reset player position, reduce hitpoints, etc.
        self.hitpoints -= 10  # Example: reduce hitpoints by 10
        if self.hitpoints <= 0:
            # Player has no hitpoints left, handle game over or any other game over actions
            print("Game Over!")
            # You might want to reset the game, display a game over screen, etc.

    def update(self):
        self.get_keys()
        # Other update logic...

        # Check for collision with mobs
        self.collide_with_group(self.game.mobs, False)
    
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            for hit in hits:
                # Check if the collided object is a Mob
                if isinstance(hit, Mob) or isinstance(hit, Mob2):
                    # Player touched a mob, trigger player death
                    self.die()
    
    def update(self):
        self.get_keys()
        # self.power_up_cd.ticking()
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        # this order of operations for rect settings and collision is imperative
        self.rect.x = self.x
        self.collide_with_walls_dir('x')
        self.rect.y = self.y
        self.collide_with_walls_dir('y')
        # added coin collection with a cooldown setting
        self.collide_with_group(self.game.coins, True)
        if self.game.cooldown.cd < 1:
            self.cooling = False
        if not self.cooling:
            self.collide_with_group(self.game.power_ups, True)
        self.collide_with_group(self.game.mobs, False)
        
class PewPew(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.pew_pews
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE / 4, TILESIZE / 4))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y
        self.speed = 10
        print("I created a pew pew...")
    
    def collide_with_group(self, group, kill):
        hits = pg.sprite.spritecollide(self, group, kill)
        if hits:
            if str(hits[0].__class__.__name__) == "Coin":
                self.moneybag += 1
    
    def update(self):
        self.collide_with_group(self.game.coins, True)
        self.rect.y -= self.speed
        # pass

#create class for walls
class Wall(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

# #create class for unlockable door that opens after key is collected
class Door(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE

class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y

class Mob2(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y

class Coin(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.coins
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y

   # Define the BossSprite class
class BossSprite(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        # Initialize the sprite
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(RED)  # Assume RED color for boss sprite
        self.rect = self.image.get_rect()
        self.rect.x = x * TILESIZE
        self.rect.y = y * TILESIZE
        self.speed = 3  # Speed of boss movement
        self.attack_cooldown = 1000  # Time between attacks (in milliseconds)
        self.last_attack_time = 0

    def update(self):
        # Move the boss horizontally
        self.rect.x += self.speed
        # Check for collision with walls
        hits = pg.sprite.spritecollide(self, self.game.walls, False)
        for hit in hits:
            if self.speed > 0:  # Moving right
                self.rect.right = hit.rect.left
            else:  # Moving left
                self.rect.left = hit.rect.right
            self.speed *= -1  # Reverse direction

        # Perform attacks
        now = pg.time.get_ticks()
        if now - self.last_attack_time > self.attack_cooldown:
            self.attack()
            self.last_attack_time = now

    
def attack(self):
    # Calculate the direction towards the player
    player_x, player_y = self.game.player.rect.center
    boss_x, boss_y = self.rect.center
    direction = pg.math.Vector2(player_x - boss_x, player_y - boss_y)
    direction.normalize()  # Normalize the vector to get a unit vector

    # Create a projectile and add it to the sprite groups
    projectile = Projectile(self.rect.centerx, self.rect.centery, direction)
    self.game.all_sprites.add(projectile)
    self.game.projectiles.add(projectile)

# Create a Projectile class
class Projectile(pg.sprite.Sprite):
    def __init__(self, x, y, direction):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface((10, 10))  # Placeholder image for projectile
        self.image.fill(YELLOW)  # Assume YELLOW color for projectile
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = 5  # Speed of projectile
        self.direction = direction  # Direction vector of projectile

    def update(self):
        # Move the projectile in its direction
        self.rect.x += self.speed * self.direction.x
        self.rect.y += self.speed * self.direction.y

        # Check for collision with walls or player
        hits = pg.sprite.spritecollide(self, self.game.walls, True)  # Assuming walls can be destroyed by projectiles
        if hits:
            self.kill()  # Destroy projectile if it hits a wall
        if pg.sprite.collide_rect(self, self.game.player):
            self.game.player.health -= 10  # Example: Reduce player health on collision
            self.kill()  # Destroy projectile on collision with player


class PowerUp(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.power_ups
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = pg.transform.scale(pg.image.load(path.join(self.game.img_folder, 'chest.png')).convert_alpha(), (TILESIZE, TILESIZE))
        self.rect = self.image.get_rect()
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.rect.x = self.x
        self.rect.y = self.y


#creating class for mob 2 (wont be used in my version)
class Mob(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image = pg.transform.scale(pg.image.load(path.join(self.game.img_folder, 'Bowser.png')).convert_alpha(), (BOSSSIZE, BOSSSIZE))
        self.rect = self.image.get_rect()
        self.x = x
        self.y = y
        self.vx, self.vy = 100, 100
        self.x = x * TILESIZE
        self.y = y * TILESIZE
        self.speed = 1
        #what happens when player collides with mob
    def collide_with_walls(self, dir):
        if dir == 'x':
            # print('colliding on the x')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vx *= -1
                self.rect.x = self.x
        if dir == 'y':
            # print('colliding on the y')
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                self.vy *= -1
                self.rect.y = self.y
    def update(self):
        # self.rect.x += 1
        self.x += self.vx * self.game.dt
        self.y += self.vy * self.game.dt
        
        if self.rect.x < self.game.player.rect.x:
            self.vx = 100
        if self.rect.x > self.game.player.rect.x:
            self.vx = -100    
        if self.rect.y < self.game.player.rect.y:
            self.vy = 100
        if self.rect.y > self.game.player.rect.y:
            self.vy = -100
        self.rect.x = self.x
        self.collide_with_walls('x')
        self.rect.y = self.y
        self.collide_with_walls('y')

    


#creating class for mob (goomba)
class Mob2(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites, game.mobs
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.goomba.png
        self.image = pg.Surface((TILESIZE, TILESIZE))
        self.image.fill(ORANGE)
        self.image = self.game.goomba.png
        self.rect = self.image.get_rect()
        # self.hit_rect = MOB_HIT_RECT.copy()
        # self.hit_rect.center = self.rect.center
        self.pos = vec(x, y) * TILESIZE
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)
        self.rect.center = self.pos
        self.rot = 0
        # added
        self.speed = 150
        # self.health = MOB_HEALTH
    

    def update(self):
        self.rot = (self.game.player.rect.center - self.pos).angle_to(vec(1, 0))
        # self.image = pg.transform.rotate(self.image, 45)
        # self.rect = self.image.get_rect()
        self.rect.center = self.pos
        self.acc = vec(self.speed, 0).rotate(-self.rot)
        self.acc += self.vel * -1
        self.vel += self.acc * self.game.dt
        self.pos += self.vel * self.game.dt + 0.5 * self.acc * self.game.dt ** 2
        # self.hit_rect.centerx = self.pos.x
        collide_with_walls(self, self.game.walls, 'x')
        # self.hit_rect.centery = self.pos.y
        collide_with_walls(self, self.game.walls, 'y')
        # self.rect.center = self.hit_rect.center
        # if self.health <= 0:
        #     self.kill()