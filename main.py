import pygame
import random
import math
from pygame import mixer

#Inicializar Pygame
pygame.init()

#Crear la pantalla
screen = pygame.display.set_mode((800, 600))

#Titulo e icono
pygame.display.set_caption("Space Invasion")
icono = pygame.image.load("icono_nave.png")
pygame.display.set_icon(icono)
fondo = pygame.image.load('fondo(800x600).png') 

#Musica
mixer.music.load('background.mp3')
mixer.music.set_volume(0.5)
mixer.music.play(-1)

#Variables Jugador
img_jugador = pygame.image.load("nave(64).png")
jugador_x = 368
jugador_y = 480
jugador_x_cambio = 0

def jugador(x,y):
    screen.blit(img_jugador, (x,y))

#Variables Enemigo
img_enemy = []
enemy_x = []
enemy_y = []
enemy_x_cambio = []
enemy_y_cambio = []
cantidad_enemigos = 10

#Creación de enemigos 
for e in range(cantidad_enemigos):
    img_enemy.append(pygame.image.load("enemy(64).png"))
    enemy_x.append(random.randint(0,736))
    enemy_y.append(random.randint(50,100))
    enemy_x_cambio.append(0.4)
    enemy_y_cambio.append(25)

#Variables laser
laser = []
img_laser = pygame.image.load("laser(12x24px).png")
laser_x = 0
laser_y = 500
laser_x_cambio = 0
laser_y_cambio = 0.8
laser_visible = False

#Puntaje
puntaje = 0
fuente = pygame.font.Font('Starborn.ttf',24)
texto_x = 10
texto_y = 560


#Texto final 
fuente_final = pygame.font.Font('Daydream.ttf', 50)

#Funcion texto final
def texto_final():
    mi_funete_final = fuente_final.render("GAME OVER", True, (255,255,255))
    screen.blit(mi_funete_final, (150,250))

#Funncion mostrar puntaje 
def mostrar_puntaje(x,y):
    texto = fuente.render(f"PUNTAJE: {puntaje}",True,(255,255,255))
    screen.blit(texto,(x,y))

#Funcion Jugador 
def jugador(x,y):
    screen.blit(img_jugador, (x,y))

#Funcion Enemigo 
def enemy(x,y,ene):
    screen.blit(img_enemy[ene], (x,y))

#Funcion Laser
def disparar_laser(x,y):
    global laser_visible
    laser_visible = True
    screen.blit(img_laser, (x+16, y+10))

#Funcion Colisiones
def detect_collision(x1,y1,x2,y2):
    distancia = math.sqrt((math.pow(x1 - x2,2)) + (math.pow(y1 - y2,2)))
    if distancia < 27 :
        return True
    else:
        return False
    
#Loop del Juego
se_ejecuta = True 

while se_ejecuta:
    #Fondo
    screen.blit(fondo, (0,0))
    #Iterar eventos
    for evento in pygame.event.get():
        #Evento para cerrar juego
        if evento.type == pygame.QUIT:
            se_ejecuta = False
        #Evento para presionar flechas    
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_LEFT:
                jugador_x_cambio = -0.7

            if evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0.7
                
            if evento.key == pygame.K_SPACE:
                sonido_laser = mixer.Sound('lasergun.mp3')
                sonido_laser.play()
                if not laser_visible:
                    laser_x = jugador_x
                    disparar_laser(laser_x,laser_y)
                    
        #Evento soltar flechas
        if evento.type == pygame.KEYUP:
            if evento.key == pygame.K_LEFT or evento.key == pygame.K_RIGHT:
                jugador_x_cambio = 0
    
    #Modificar ubicación del jugador
    jugador_x += jugador_x_cambio  
      
    #Bordes del jugador
    if jugador_x <= 0:
        jugador_x = 0
    elif jugador_x >= 736:
        jugador_x = 736
    
     #Modificar ubicación del enemigo
    for e in range(cantidad_enemigos):
        #Fin del juego 
        if enemy_y[e] > 438:
            for k in range(cantidad_enemigos):
                enemy_y[k] = 1000
            texto_final()
            break

        enemy_x[e] += enemy_x_cambio[e]
        #Bordes del Enemigo
        if enemy_x[e] <= 10:
            enemy_x_cambio[e] = 0.35
            enemy_y[e] += enemy_y_cambio[e]
        elif enemy_x[e] >= 726:
            enemy_x_cambio[e] = -0.35
            enemy_y[e] += enemy_y_cambio[e]
        #Colisiones
        colision = detect_collision(enemy_x[e],enemy_y[e],laser_x,laser_y)
        
        if colision:
            sonido_colision = mixer.Sound('explosion.mp3')
            sonido_colision.play()
            laser_y = 500
            laser_visible = False
            puntaje += 1
            enemy_x[e] = random.randint(0,736)
            enemy_y[e] = random.randint(50,100)
                
        enemy(enemy_x[e],enemy_y[e],e)    
            
    #Movimiento laser
    if laser_y <= -64:
        laser_y = 500
        laser_visible = False
    if laser_visible:
        disparar_laser(laser_x,laser_y)
        laser_y -= laser_y_cambio
    
    jugador(jugador_x,jugador_y)
    mostrar_puntaje(texto_x,texto_y)
    
    
    #Actualizar
    pygame.display.update()       