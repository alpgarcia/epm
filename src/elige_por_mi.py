#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (C) 2017 Alberto Pérez García-Plaza
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.
#
# Authors:
#     Alberto Pérez García-Plaza <alpgarcia@gmail.com>
#

import argparse
import colorama
import os
import sys
import time

from colorama import Fore, Back, Style

DESCRIPTION = \
    """Elijo nombre por ti si me das un par de listas."""

PROGRAM_VERSION = \
    ' \t' \
    + Style.BRIGHT + Back.BLUE + Fore.WHITE \
    + '     ' \
    + 'ELIGE POR MI v1.1 escrito por Alberto Pérez García-Plaza, (c)2017' \
    + '     '

ABIERTOS = '([0_0])'
CERRADOS = '([u_u])'
L_WINK = '([0_u])'
R_WINK = '([u_0])'
ESCRIBIENDO = '([U_U])'

def extraer_nombre(line):
    return line[0:len(line)-1].capitalize()

def borra_linea(lon):
    # Borra la linea anterior
    linea_en_blanco = ' '
    for j in range(lon):
        linea_en_blanco += ' '
    print(linea_en_blanco, end='\r')

def parpadeo(texto, lon=0):
    for i in range(6):
        ojos = ABIERTOS
        if i % 2 == 0:
            ojos = CERRADOS
            time.sleep(3)
        else:
            time.sleep(.25)

        borra_linea(lon)

        linea = '\t' + Back.MAGENTA + Fore.LIGHTWHITE_EX + ojos \
                + Style.RESET_ALL + ' '*4 + Style.BRIGHT + Back.BLUE + Fore.YELLOW + texto
        print(linea, end='\r', flush=True)

    return len(linea)

def pensando(texto, lon=0):
    ojos = L_WINK
    for i in range(24):

        if i % 8 == 0:
            ojos = L_WINK
        elif i % 4 == 0:
            ojos = R_WINK

        borra_linea(lon)

        idea = "º" * (i % 4)

        linea = '\t' + Back.MAGENTA + Fore.LIGHTWHITE_EX + ojos + idea \
                + Style.RESET_ALL + ' '*(4-len(idea)) + Style.BRIGHT + Back.BLUE \
                + Fore.YELLOW + texto
        print(linea, end='\r', flush=True)

        time.sleep(.5)

    return len(linea)

def escribiendo(texto, lon=0):
    for i in range(50):
        ojos = ESCRIBIENDO
        lapiz = '/'
        if i % 2 == 0:
            lapiz = '\\'

        time.sleep(.3)

        borra_linea(lon)

        linea = '\t' + Back.MAGENTA + Fore.LIGHTWHITE_EX + ojos + ' ' + lapiz \
                + Style.RESET_ALL + ' '*2 + Style.BRIGHT + Back.BLUE + Fore.YELLOW + texto
        print(linea, end='\r', flush=True)

    return len(linea)

def resultado(lista, log, lon=0):
    lon = parpadeo('Ya tengo una propuesta, déjame que la escriba', lon)

    lon = escribiendo('(...escribiendo...)', lon)

    borra_linea(lon)
    print('\t' + Back.MAGENTA + Fore.LIGHTWHITE_EX + ABIERTOS, end='')
    print(' '*4 + Style.BRIGHT + Back.BLUE + Fore.YELLOW
          + '¡Listo!')
    time.sleep(1)
    print('\t' + Back.MAGENTA + Fore.LIGHTWHITE_EX + ' m   m ')
    print('\t' + Fore.YELLOW + '\tNOMBRE\t\tPUNTUACIÓN\t')
    print('\t' + Fore.YELLOW + '\t------\t\t----------\t')
    top = 3
    for item in lista:
        sep = '\t'*3

        if top > 0:
            color = Fore.GREEN
            top = top -1
        else:
            color = Fore.WHITE

        if len(item[0]) > 7:
            sep = '\t'*2
        print('\t' + Style.BRIGHT + color + '\t' + item[0] + sep
              + str(item[1]) + '\t')
        log.write(item[0] + ': ' + str(item[1]) + '\n')
        time.sleep(1)

    print()

def parse_args():
    """Parse arguments from the command line"""

    parser = argparse.ArgumentParser(description=DESCRIPTION)

    parser.add_argument('-a', '--list1', dest='lista_1', \
        required=True, help='lista de 6 nombres')
    parser.add_argument('-b', '--list2', dest='lista_2', \
        required=True, help='lista de 6 nombres')

    parser.add_argument('-r', '--ranking', dest='ranking_file', \
        default='data/ranking.txt', help='ranking de nombres más usados')

    return parser.parse_args()

def main():

    args = parse_args()

    colorama.init(autoreset=True)

    # Limpiar pantalla
    os.system('cls' if os.name == 'nt' else 'clear')

    print()
    print(PROGRAM_VERSION)

    print()

    lon = parpadeo(' Voy a elegir nombre por ti ')
    lon = parpadeo(' No es una tarea fácil así que.. ')
    lon = pensando(' ...déjame que piense ', lon)

    log_file = 'log/log_' + time.asctime() + '.log'
    log = open(log_file, 'w')

    log.write('***LISTA 1***\n')
    lista = {}
    with open(args.lista_1, 'r') as f:
        puntos = 6
        for line in f:
            nombre = extraer_nombre(line)
            lista[nombre] = puntos
            log.write(nombre + ': ' + str(puntos) + '\n')
            puntos = puntos - 1

    log.write('***LISTA 2***\n')
    with open(args.lista_2, 'r') as f:
        puntos = 6
        for line in f:
            nombre = extraer_nombre(line)
            if nombre in lista:
                lista[nombre] = lista[nombre] + puntos
            else:
                lista[nombre] = puntos
            log.write(nombre + ': ' + str(puntos) + '\n')
            puntos =  puntos - 1

    log.write('***RANKING***\n')
    ranking = []
    with open(args.ranking_file, 'r') as f:
        for line in f:
            ranking.insert(0, extraer_nombre(line))

    # Asigna hasta 3 puntos a los nombres menos comunes
    puntos = 3
    for nombre in ranking:
        if nombre in lista:
            lista[nombre] = lista[nombre] + puntos
            log.write(nombre + ': ' + str(puntos) + '\n')
            if puntos > 0:
                puntos = puntos - 1

    lista_ordenada = sorted(lista.items(), key=lambda item: item[1], reverse=True)

    log.write('***RESULTADO***\n')

    resultado(lista_ordenada, log, lon)

    log.close()

    print(' \t' \
    + Style.BRIGHT + Back.BLUE + Fore.WHITE \
    + '     ' \
    + 'Una copia de esta lista ha sido guardada en ' + log_file \
    + ' '
    )

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        s = "\n\nReceived Ctrl-C or other break signal. Exiting.\n"
        sys.stdout.write(s)
        sys.exit(0)
    except RuntimeError as e:
        s = "Error: %s\n" % str(e)
        sys.stderr.write(s)
        sys.exit(1)
