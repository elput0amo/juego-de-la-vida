#primero  instalamos las bibiotecas necesarias para el propio codigo
import pygame as gm
import time
import numpy as np 
#se que la mayoria de los comentarios que voy a hacer no son necesarios pero  estoy intentando practicar porque no suelo comentar una mierda

#para usar esta bibioteca hay que hacer lo que te enseñaron en TIC, es basicamente el mismo proceso con otra sintaxis
gm.init()
width, height= 400, 400
bg= 25,25,25 #esto es para que el fondo sea gris,  luego puedes cambiarlo como te apetezca
screen= gm.display.set_mode((height, width))
screen.fill(bg)
#esto es segun como te lo dice en el tutorial, sinceramente yo lo veo inutil, seria mas facil y claro poner tu los valores de primeras en el setup y fill

#ahor establecemos celdas y el estado inical de estas 
nCx,nCy= 60,60       #numero de celdas
#aclaracion extra, al pasarlo por la biblioteca de np se crea un sistema de matriz
Cstate=np.zeros((nCx,nCy))         #clarificcion cuando sepa que coño hace esto (lo que hace es establecer a todos los valores de la matriz como 0, diendo estomuertos en el juego)
tamnCx=  width/nCx
tamnCy= height/nCy      #vale aqui si que tiene mas sentido haber usado varibles en vez de numeros puros

#aqui el tutorial empieza  a ser mucho texto y me da pereza explicarlo aqui

#basicamente te dice una serie de posiciones iniciales de la las flores en la matriz que hacen que se formen ciertos patrones y te explica como crearlos
#voy a poner un par, todo esto tiene que ponerse al principio porque es un prerequisito del juego


#este lo que hace es que rotar un cuarto de vuelta cada itreacion, es una puta diagonal
Cstate[38,20]=1
Cstate[39,20]=1
Cstate[40,20]=1

#este lo que hace es moverse en diagonal por la  matriz
Cstate[10,5] = 1
Cstate[12,5] = 1
Cstate[11,6] = 1
Cstate[12,6] = 1
Cstate[11,7] = 1

#y lo mismo otra vez
Cstate[5,10] = 1
Cstate[5,12] = 1
Cstate[6,11] = 1
Cstate[6,12] = 1
Cstate[7,11] = 1

#este es la definicion de me la pela, se queda invariable todo el tiempo a no ser que le toquen los cojones
Cstate[18,15] = 1
Cstate[17,16] = 1
Cstate[17,15] = 1
Cstate[18,16] = 1

#este se llama serpiente, ni zorra de lo que hace la  verdad
Cstate[30,20] = 1
Cstate[31,20] = 1
Cstate[32,20] = 1
Cstate[32,19] = 1
Cstate[33,19] = 1
Cstate[34,19] = 1

#necesitamos una vatiable para establecer la pausa en el sistema, en nuestro caso se tiene que empezar con pausa, a si que 
pausa=False 

#y ahora si toca hacer el bucle con las reglas del juego, pero antes hay que establecer la funcionalidad de que se refresque al principio de cada iteracion
#ademas va a meter cositas extra como `poder cambiar el estado de una casilla haciendo click o como poder pausar el juego
while True:
    #hay que copiar la matriz del final de la iteracion pasada, en el primer caso la establecida aqui arriba
    newCstate= np.copy(Cstate)

    #ralentizamos la ejecucion para que se entienda
    time.sleep(0.1)
    #ademas hay que limpiar la pantalla, con el gris feo de cojones
    screen.fill(bg)

    #aqui es cuando usamos la funcionalidad de la biblioteca de gamepy, es para hacer que el teclado pause y el raton reviva
    #al parecer hay que establecer un evento de primeras con el cual despues defines reacciones
    #el evento que hemos establecido esta iondefinido y es basicamente siempre que ocurre algo camvia ev
    ev = gm.event.get()

    for event in ev:
        #eso detecta si se ha pulsado una tecla y si es el caso pues pausa
        if event.type==gm.KEYDOWN:
            pausa= not pausa

        # esto mira si has clikeado,pocierto me acabo de dar cuanta que la bilbioteca funciona a case de funciones creadas para objetos
        #por ejemplo, aqui estas usando la funcion get_pressed de la clase mouse, tiene sentido todo
        click= gm.mouse.get_pressed()

        #luego esto de aqui hace algo con los clicks, ademas te saca la localizacion del raton en momento del click 
        #con la localizacion del raton, te saca la casilla que es con una division al suelo de la posicion entre el tamaño de una celda
        if sum(click)> 0:
            posX, posY=  gm.mouse.get_pos()
            celX,celY= int(np.floor(posX/tamnCx)) , int(np.floor(posY/tamnCy))
            newCstate[celX,celY]=1

        #ahora lo que toca es recorrer cada celda para ver los vecinos que tiene y ya sea matar, o hacer crecer una flor.
        #esto corre todas las celdas una a una
            
    for y in range (0, nCx):
        for x in range(0,nCy):

            if not pausa: 
                vecinos=  Cstate[(x - 1) % nCx, (y - 1)  % nCy] + \
                        Cstate[(x)     % nCx, (y - 1)  % nCy] + \
                        Cstate[(x + 1) % nCx, (y - 1)  % nCy] + \
                        Cstate[(x - 1) % nCx, (y)      % nCy] + \
                        Cstate[(x + 1) % nCx, (y)      % nCy] + \
                        Cstate[(x - 1) % nCx, (y + 1)  % nCy] + \
                        Cstate[(x)     % nCx, (y + 1)  % nCy] + \
                        Cstate[(x + 1) % nCx, (y + 1)  % nCy]
 #esto escanea todas las celdas que hay alrededor de la celda que le halla tocado en la iteracion
#ademas % sirve para que las celdas de los extremos tengan como vecinas las de los otros extemos
                    
                #regla 1
                if Cstate[x,y]==0 and vecinos== 3:
                    newCstate[x,y]=1
                #regla 2
                    
                elif Cstate[x,y]==1 and (vecinos<2 or vecinos>3):
                    newCstate[x,y]=0
                
                #esto es otra cosa de la bilbioteca, hay que calcular el tamaño d cada poligono q forma cada celda
            poligono= [((x)   * tamnCx, y * tamnCy),
                ((x+1) * tamnCx, y * tamnCy),
                ((x+1) * tamnCx, (y+1) * tamnCy),
                ((x)   * tamnCx, (y+1) * tamnCy)]
                
                #ahora pintamos dependiendo de cuales esten vivas o muertas
            if newCstate[x,y]==0:
                gm.draw.polygon(screen, (40,40,40), poligono,1)
            else:
                gm.draw.polygon(screen, (200,100,100), poligono,0)


        #ahora solo queda actualizar la matriz con todos los datos nuevos obtenidos en el bucle
    Cstate=np.copy(newCstate)
    
        #y por ultimo, mostrarlo todo
    gm.display.flip()


                



















