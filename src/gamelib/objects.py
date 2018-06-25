###############################################################################
## PygameCross
##
## Copyright (C) 2010 Jorge Zilbermann ealdorj@gmail.com
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
###############################################################################

import os
import sys
from pygame.locals import *
import pygame
from gamelib.constants import *


class Board:
    def __init__(self, num_fil, num_col, linea, archivo):
        self.sol = []
        lista = []
        chain = ''
        abre = aux = False
        self.titulo = ''
        count = 50
        
        self.archivo = open(os.path.join('size', archivo))
        for line in self.archivo:
            if count == linea:
                for e in line:
                    if e == "[":
                        abre = True
                    if e == "]":
                        for i in chain.split(","):
                            lista.append(int(i))
                        self.sol.append(lista)
                        lista = []
                        abre = False
                        chain = ''
                    if abre and e != "[":
                        chain = chain + e
                    if e != ":" and not aux:
                        self.titulo = self.titulo + e
                    if e == ":":
                        aux = True
            count += 30
        self.archivo.close()
                
        self.celdas = self.crear_celdas(num_fil, num_col, EMPTY)
        self.tipos = self.agregar_tipos()
        self.columnas = num_col
        self.filas = num_fil
        
        self.fuente = pygame.font.Font(None, 25)
        
        uno = False
        sum = 0
        list = []
        self.listoflists = []
        for i in range(self.filas):
            for j in range(self.columnas):
                if self.sol[i][j] == 1:
                    uno = True
                    if uno:
                        sum += 1
                if self.sol[i][j] == 0:
                    if uno:
                        list.append(sum)
                    uno = False
                    sum = 0
                    list.append(sum)
                if uno and j == self.columnas-1:
                    list.append(sum) 
            self.listoflists.append(list)
            uno = False
            sum = 0
            list = []
            
        uno = False
        sum = 0
        list = []
        self.listoflists2 = []
        for i in range(self.columnas):
            for j in range(self.filas):
                if self.sol[j][i] == 1:
                    uno = True
                    if uno:
                        sum += 1
                if self.sol[j][i] == 0:
                    if uno:
                        list.append(sum)
                    uno = False
                    sum = 0
                    list.append(sum)
                if uno and j == self.filas-1:
                    list.append(sum) 
            self.listoflists2.append(list)
            uno = False
            sum = 0
            list = []
        
    def reset(self):
        self.celdas = self.crear_celdas(self.filas, self.columnas, EMPTY)
        
    def to_complete(self):
        for i in range(self.filas):
            for j in range(self.columnas):
                if self.celdas[i][j] == EMPTY:
                    self.celdas[i][j] = MARK_X
                
    def crear_celdas(self, num_fil, num_col, tipo):
        celdas = []
        for i in range(num_fil):
            celdas.append([tipo for i in range(num_col)])
        return celdas
    
    def agregar_tipos(self):
        tipos = []
        tipos.append(Tipo(os.path.join("images", "relleno.png")))
        tipos.append(Tipo(os.path.join("images", "equis.png")))
        return tipos
    
    def draw_table(self, surface, color):
        tamano = self.tipos[0].get_width()
        
        for i in range(len(self.celdas) + 1):
            pygame.draw.line(surface, (0, 0, 0), (WIDTH / 2 - 20, i * tamano + HEIGHT / 2 - 120), (self.columnas * tamano + WIDTH / 2 - 20, i * tamano + HEIGHT / 2 - 120), 2)
        for i in range(len(self.celdas[0]) + 1):
            pygame.draw.line(surface, (0, 0, 0), (i * tamano + WIDTH / 2 - 20, HEIGHT / 2 - 120), (i * tamano + WIDTH / 2 - 20, self.filas * tamano + HEIGHT / 2 - 120), 2)
        
        x = y = 0
        for fila in self.celdas:
            for ele in fila:
                if ele != EMPTY:
                    self.tipos[ele - 1].drawn(surface, x + 2, y + 2)
                x += tamano
            x = 0
            y += tamano  
        
        aux, aux2 = 0, 140
        for i in range(self.columnas):
            for j in self.listoflists2[i].__reversed__():
                if j > 9:
                    surface.blit(self.fuente.render(str(j), True, color), (WIDTH / 2 - 20 + aux, HEIGHT / 2 - aux2))
                else:
                    surface.blit(self.fuente.render(str(j).replace("0", "  "), True, color), (WIDTH / 2 - 15 + aux, HEIGHT / 2 - aux2))
                aux2 += 20
                if j == 0:
                    aux2 -=20
            aux2 = 140
            aux += 20 
        
        aux, aux2 = 0, 40
        for i in range(self.filas):
            for j in self.listoflists[i].__reversed__():
                if j > 9:
                    surface.blit(self.fuente.render(str(j), True, color), (WIDTH / 2 - aux2 - 5, HEIGHT / 2 + 1 + aux - 120))
                else:
                    surface.blit(self.fuente.render(str(j).replace("0", "  "), True, color), (WIDTH / 2 - aux2, HEIGHT / 2 + 1 + aux - 120))
                aux2 += 20
                if j == 0:
                    aux2 -=20
            aux2 = 40
            aux += 20
        
        posx, posy = pygame.mouse.get_pos()
        if posx > WIDTH / 2 - 20 and posx < self.columnas * tamano + WIDTH / 2 -20 and posy > HEIGHT / 2 - 120 and posy < i * tamano + HEIGHT / 2 - 100:
            pygame.draw.line(surface, (238, 0, 255), (WIDTH / 2 - 20, posy), (posx, posy), 2)
            pygame.draw.line(surface, (238, 0, 255), (posx, HEIGHT / 2 - 120), (posx, posy), 2)
        
        surface.blit(self.fuente.render("Size: " + str(self.filas) + " x " + str(self.columnas), True, (0, 0, 0)), (10, 10))
        surface.blit(self.fuente.render("Title: " + self.titulo, True, (0, 0, 0)), (10, 40))
        
    def actualizar(self):
        boton = pygame.mouse.get_pressed()
        posicionx = posiciony = -1
        actualizar = False
        
        if boton[0] or boton[2]:
            x, y = pygame.mouse.get_pos() 
            posicionx = (x // self.tipos[0].get_width()) - 19
            posiciony = (y // self.tipos[0].get_width()) - 9
            if (posicionx < self.columnas and posicionx >= 0) and (posiciony < self.filas and posiciony >= 0):
                if self.celdas[posiciony][posicionx] == MARK_O or self.celdas[posiciony][posicionx] == MARK_X:
                    self.celdas[posiciony][posicionx] = EMPTY
                else:
                    if boton[0]:
                        self.celdas[posiciony][posicionx] = MARK_O
                    if boton[2]:
                        self.celdas[posiciony][posicionx] = MARK_X
                actualizar = True
            else:
                posicionx = posiciony = -1
         
        return actualizar
    
    def analysis(self):
        res = True
        
        for i in range(self.filas):
            for j in range(self.columnas):
                if (self.sol[i][j] == self.celdas[i][j] or self.sol[i][j] + 2 == self.celdas[i][j]) and res:
                    res = True
                else:
                    res = False
        
        return res


class Tipo:
    def __init__(self, image):
        self.image = pygame.image.load(image).convert_alpha()
        
    def get_width(self):
        return self.image.get_width()
    
    def drawn(self, surface, x, y):
        surface.blit(pygame.transform.scale(self.image, (18, 18)), (x + WIDTH // 2 - 20, y + HEIGHT // 2 - 120))
