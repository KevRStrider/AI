#!/usr/bin/env python

"""
busquedas_adversarios.py
------------------------

Modulo con las funciones genericas para la búsqueda con adversarios

Para hacerlo orientado a objetos y pasar toda la información por
referencia (y hacer un poco más rápido el juego) vamos a mantener
el estado del juego y el jugador actual dentro del juego.

"""

from random import shuffle


class JuegoSumaCeros2T:
    """
    Clase abstracta para juegos de suma cero, por turnos para 2 jugadores.

    """
    def __init__(self, x0, jugador=1):
        """
        Inicializa el estado inicial del juego y el jugador
        que comienza (típicamente el primero)
        
        El estado se representa como una lista, y el estado inicial (x0) 
        de preferencia se representa con una tupla
        
        El jugador puede ser 1 y -1 en este caso

        """
        self.estado_inicial = x0
        self.estado = list(x0)
        self.jugador = jugador

    def jugadas_legales(self):
        """ 
        Devuelve un iterable con las jugadas legales del jugador actual
        
        """
        raise NotImplementedError("Hay que desarrollar este método, pues")

    def es_terminal(self):
        """ 
        Devuelve True si el juago está en una posición terminal
        
        """
        raise NotImplementedError("Hay que desarrollar este método, pues")
    
    def utilidad(self):
        """ 
        Devuelve la utilidad (final) del juador 1

        """
        raise NotImplementedError("Hay que desarrollar este método, pues")

    def hacer_jugada(self, jugada):
        """ 
        Realiza la juagada, cambia self.estado y self.jugador, devuelve None
        
        Recuerda que el estado es una lista, para poder hacer cambios
        por referencia y ahorrar un poco de tiempo en cada nodo
        
        """
        raise NotImplementedError("Hay que desarrollar este método, pues")

    def deshacer_jugada(self, estado_anterior):
        """ 
        Restaura el estado anterior y cambia el jugador en turno.
        Devuelve None
        
        """
        self.estado = estado_anterior[:]
        self.jugador *= -1
    
    def copia_estado(self):
        return self.estado[:]


def minimax(juego, dmax=100, heuristica=None):
    inicial = juego.jugador
    return max(
        juego.jugadas_legales(),
        key=lambda a:inicial * negval(a, juego, inicial, dmax - 1, heuristica)
    )

def negval(jugada, juego, paso, dmax, heuristica):

    anterior = juego.copia_estado()
    juego.hacer_jugada(jugada)

    if juego.es_terminal():
        valor = juego.utilidad()
    elif heuristica != None and dmax == 0:
        valor = heuristica(juego)
    else:
        valor = paso * min(
            paso * negval(a, juego, -paso, dmax - 1, heuristica) 
            for a in juego.jugadas_legales()
        )
    juego.deshacer_jugada(anterior)
    return valor

def orden_aleatorio(jugadas):
    jugadas = list(jugadas)
    shuffle(jugadas)
    return jugadas

#PUNTO 1, TABLA DE TRANSPOSICIONES
def alpha_beta(juego, dmax=12, heuristica=None, orden_jugadas=None):
    if heuristica == None:
        heuristica = lambda j:j.utilidad()
    if orden_jugadas == None:
        orden_jugadas = orden_aleatorio

    tabla_transposicion = {}
    
    jugada, _ = negamax(
        juego, dmax, -1e10, 1e10, juego.jugador, heuristica, orden_jugadas, tabla_transposicion
    )
    return jugada

def negamax(juego, d, alpha, beta, lado, heuristica, orden_jugadas, tabla_transposicion):
    clave = (tuple(juego.estado), d, lado)
    if clave in tabla_transposicion:
        valor, profundidad, mejor_jugada = tabla_transposicion[clave]
        if profundidad >= d:
            return mejor_jugada, valor

    if juego.es_terminal():
        return None, lado * juego.utilidad()
    if d == 0:
        return None, lado * heuristica(juego)

    jugadas = orden_jugadas(juego.jugadas_legales(), juego)
    valor = -1e10

    for jugada in jugadas:
        estado_anterior = juego.copia_estado()
        juego.hacer_jugada(jugada)
        _, v = negamax(juego, d - 1, -beta, -alpha, -lado, heuristica, orden_jugadas, tabla_transposicion)
        juego.deshacer_jugada(estado_anterior)
        if -v > valor:
            mejor_jugada, valor = jugada, -v
            alpha = max(alpha, valor)
            if alpha >= beta:
                break

    tabla_transposicion[clave] = (valor, d, mejor_jugada)
    return mejor_jugada, valor
