#Proyecto Goku Smart IA
#Nombre: Sebastian Peñaranda Hurtado
#Codigo: 202041138-3743
#Descripcion: es un juego entre dos adversarios en el que cada uno controla un caballo sobre un tablero de ajedrez,
#el objetivo del juego es obtener más puntos que el adversario.

import random
import tkinter as tk
import time

# Crear la ventana
ventana = tk.Tk()

# Resolucion de pantalla y nombre 
ventana.geometry("528x700")
ventana.title("Proyecto IA")
ventana.resizable(width=False,height=False)
turno = False
nivelBot = 0
puntosMaquina = 0
puntosJugador = 0
#----------------------------------------------------CLASE NODO------------------------------------------------


class Nodo:
    def __init__(self, puzzle, padre, operador, profundidad, expandido, hijos, puntosCPU, puntosJugador):
        self.puzzle = puzzle
        self.padre = padre
        self.operador = operador
        self.profundidad = profundidad
        self.expandido = expandido
        self.hijos = hijos
        self.puntosCPU = puntosCPU
        self.puntosJugador = puntosJugador

    #Muestra cantidad de puntos del jugador
    def mostrarPuntosJugador(self):
        return self.puntosJugador
    
    #Muestra cantidad de puntos de la CPU
    def mostrarPuntosCPU(self):
        return self.puntosCPU
    
    #Muestra la profundidad 
    def mostrarProfundidad(self):
        return self.profundidad
    
    #Muestra el puzzle del nodo actual
    def mostrarPuzzle(self):
        return self.puzzle

    #Cambia la cantidad del atributo hijos por la que esta en el parametro
    def cambiarHijos(self,hijos):
        self.hijos = hijos
    
    #Muestra el atributo hijos
    def mostrarHijos(self):
        if self.hijos == None:
            hijos = []
        else:
            hijos = self.hijos
        return hijos
    
    #Expande el nodo actual
    def expandirNodo(self, lista, turno):
        nodosHijos = []
        #expandir hijos y asigna que caballo sera
        if(turno):
            print('soy caballo blanco')
            operadores = self.encontrarCaminos(self.mostrarPuzzle(), 1)
        else:
            print('soy caballo negro')
            operadores = self.encontrarCaminos(self.mostrarPuzzle(), 2)
        
        print("Profundidad:",self.mostrarProfundidad() ,"los caminos posibles son:",operadores)

        #Expansion minimax
        for i in range(0,len(operadores)):
            if(turno):
                puntos = self.puntosTotal(operadores[i], 1)
                matrizNodo=self.mover(operadores[i], self.mostrarPuzzle(), 1)
                nodo = Nodo(matrizNodo, self, operadores[i], self.profundidad+1, False, None, puntos + self.mostrarPuntosCPU(), self.mostrarPuntosJugador())
                #print('nodoCreadoBlancas: ', nodo.mostrarOperador(),' con puntosMaquina: ',puntos + self.mostrarPuntosCPU(),'y puntos jugador: ', self.mostrarPuntosJugador())
            else:
                puntos = self.puntosTotal(operadores[i], 2)
                matrizNodo=self.mover(operadores[i], self.mostrarPuzzle(), 2)
                nodo = Nodo(matrizNodo, self, operadores[i], self.profundidad+1, False, None, self.mostrarPuntosCPU(), puntos + self.mostrarPuntosJugador())
                #print('nodoCreadoNegras: ', nodo.mostrarOperador(),' con puntosMaquina: ', self.mostrarPuntosCPU(), 'y puntos jugador: ', puntos + self.mostrarPuntosJugador())
                
            #Añade los nodos a una nueva lista para el atributos hijos
            nodosHijos.append(nodo)
            lista.append(nodo)
        self.cambiarHijos(nodosHijos)
        self.cambiarExpandido()

        return lista

    #Busca los caminos posibles del caballo blanco
    def encontrarCaminos(self,matrizArg, caballo):
        operadoresPosibles = []
        if caballo == 1:
            caballoEnemigo = 2
        else:
            caballoEnemigo = 1
        #Busca al caballo blanco en la matriz en la matriz
        for i in range(len(matrizArg)):
            for j in range(len(matrizArg[0])):
                if(self.mostrarPuzzle()[i][j] == caballo):
                    #Busca los movimientos posibles hacia cada direccion y segun que algoritmo se use
                    #Por profundidad
                    if j-1 >= 0 and i-2 >= 0:
                        if(self.padre == None and matrizArg[i-2][j-1] != caballoEnemigo):
                            operadoresPosibles.append("arribaIzquierda")
                        else:
                            if(matrizArg[i-2][j-1] != caballoEnemigo and (self.evitaCiclos(self.mover("arribaIzquierda",matrizArg, caballo)) ) ):
                                operadoresPosibles.append("arribaIzquierda")
                    if j+1 < 8 and i-2 >= 0: 
                        if(self.padre == None and matrizArg[i-2][j+1] != caballoEnemigo):
                            operadoresPosibles.append("arribaDerecha")
                        else:
                            if(matrizArg[i-2][j+1] != caballoEnemigo and (self.evitaCiclos(self.mover("arribaDerecha",matrizArg, caballo)) )):
                                operadoresPosibles.append("arribaDerecha")
                    if j+2 < 8 and i-1 >= 0:  
                        if(self.padre == None and matrizArg[i-1][j+2] != caballoEnemigo):
                            operadoresPosibles.append("derechaArriba")
                        else:      
                            if(matrizArg[i-1][j+2] != caballoEnemigo and (self.evitaCiclos(self.mover("DerechaArriba",matrizArg, caballo)) ) ):
                                operadoresPosibles.append("derechaArriba")
                    if j+2 < 8 and i+1 < 8: 
                        if(self.padre == None and matrizArg[i+1][j+2] != caballoEnemigo):
                            operadoresPosibles.append("derechaAbajo")
                        else:
                            if(matrizArg[i+1][j+2] != caballoEnemigo and (self.evitaCiclos(self.mover("derechaAbajo",matrizArg, caballo)) )):
                                operadoresPosibles.append("derechaAbajo")
                    if j-1 >= 0 and i+2 < 8:  
                        if(self.padre == None and matrizArg[i+2][j-1] != caballoEnemigo):
                            operadoresPosibles.append("abajoIzquierda")
                        else:      
                            if(matrizArg[i+2][j-1] != caballoEnemigo and (self.evitaCiclos(self.mover("abajoIzquierda",matrizArg, caballo)) ) ):
                                operadoresPosibles.append("abajoIzquierda")
                    if j+1 < 8 and i+2 < 8: 
                        if(self.padre == None and matrizArg[i+2][j+1] != caballoEnemigo):
                            operadoresPosibles.append("abajoDerecha")
                        else:
                            if(matrizArg[i+2][j+1] != caballoEnemigo and (self.evitaCiclos(self.mover("abajoDerecha",matrizArg, caballo)) )):
                                operadoresPosibles.append("abajoDerecha")
                    if j-2 >= 0 and i-1 >= 0:  
                        if(self.padre == None and matrizArg[i-1][j-2] != caballoEnemigo):
                            operadoresPosibles.append("izquierdaArriba")
                        else:      
                            if(matrizArg[i-1][j-2] != caballoEnemigo and (self.evitaCiclos(self.mover("izquierdaArriba",matrizArg, caballo)) ) ):
                                operadoresPosibles.append("izquierdaArriba")
                    if j-2 >= 0 and i+1 < 8:  
                        if(self.padre == None and matrizArg[i+1][j-2] != caballoEnemigo):
                            operadoresPosibles.append("izquierdaAbajo")
                        else:      
                            if(matrizArg[i+1][j-2] != caballoEnemigo and (self.evitaCiclos(self.mover("izquierdaAbajo",matrizArg, caballo)) ) ):
                                operadoresPosibles.append("izquierdaAbajo")    
                    return operadoresPosibles
    
    #Funcion que evita devolverse a cualquier padre de los nodos ya transitados
    def evitaCiclos(self, matrizFutura):
        #Si llega aqui significa que no hay ciclo
        if(self.mostrarPadre() == None):
            return True
        #Si entra aqui significa que el camino se repetira
        elif(self.mostrarPuzzle() == matrizFutura):
            return False
        #Hace que sea iterativo hasta acabar con los padres
        else:
            padre = self.mostrarPadre()
            return padre.evitaCiclos(matrizFutura)

    #Da la matriz con el siguiente movimiento que uno le escribe
    def mover(self, operador, matrizNodo, caballo):
        #Uso una matriz auxiliar para no editar directamente a la matriz de self.mostrarPuzzle()
        matrizAuxiliar = [[0 for j in range(maxRC)] for i in range(maxRC)]
        for i in range(len(matriz)):
            for j in range(len(matriz[0])):
                matrizAuxiliar[i][j] = matrizNodo[i][j]

        #Asigna el caballo enemigo
        if caballo == 1:
            caballoEnemigo = 2
        else:
            caballoEnemigo = 1

        #con la matriz de solo paredes
        for i in range(len(matriz)):
            for j in range(len(matriz[0])):
                #posicion del caballo blanco
                if(self.mostrarPuzzle()[i][j] == caballo):
                    if(operador.lower() == "arribaizquierda"):
                        if self.mostrarPuzzle()[i-2][j-1] != caballoEnemigo:
                            matrizAuxiliar[i][j] = 0
                            resultado= self.moverMatriz(matrizAuxiliar, i-2,j-1,caballo)                            
                    if(operador.lower() == "arribaderecha"):
                        if self.mostrarPuzzle()[i-2][j+1] != caballoEnemigo:
                            matrizAuxiliar[i][j] = 0
                            resultado= self.moverMatriz(matrizAuxiliar, i-2,j+1,caballo)                            
                    if(operador.lower() == "derechaarriba"):
                        if self.mostrarPuzzle()[i-1][j+2] != caballoEnemigo:
                            matrizAuxiliar[i][j] = 0
                            resultado= self.moverMatriz(matrizAuxiliar, i-1,j+2,caballo)                            
                    if(operador.lower() == "derechaabajo"):
                        if self.mostrarPuzzle()[i+1][j+2] != caballoEnemigo:
                            matrizAuxiliar[i][j] = 0
                            resultado= self.moverMatriz(matrizAuxiliar, i+1,j+2,caballo)                            
                    if(operador.lower() == "abajoizquierda"):
                        if self.mostrarPuzzle()[i+2][j-1] != caballoEnemigo:
                            matrizAuxiliar[i][j] = 0
                            resultado= self.moverMatriz(matrizAuxiliar, i+2,j-1,caballo)                            
                    if(operador.lower() == "abajoderecha"):
                        if self.mostrarPuzzle()[i+2][j+1] != caballoEnemigo:
                            matrizAuxiliar[i][j] = 0
                            resultado= self.moverMatriz(matrizAuxiliar, i+2,j+1,caballo)                            
                    if(operador.lower() == "izquierdaarriba"):
                        if self.mostrarPuzzle()[i-1][j-2] != caballoEnemigo:
                            matrizAuxiliar[i][j] = 0
                            resultado= self.moverMatriz(matrizAuxiliar, i-1,j-2,caballo)
                    if(operador.lower() == "izquierdaabajo"):
                        if self.mostrarPuzzle()[i+1][j-2] != caballoEnemigo:
                            matrizAuxiliar[i][j] = 0
                            resultado= self.moverMatriz(matrizAuxiliar, i+1,j-2,caballo)
                    return resultado

    #Funcion auxiliar de moverse, sirve para ahorrar lineas de codigo
    def moverMatriz(self, matrizAuxiliar,i, j,caballo):
        if caballo == 1:
            matrizAuxiliar[i][j] = 1 
        else:
            matrizAuxiliar[i][j] = 2
        return matrizAuxiliar

    #Muestra si el nodo ha sido expandido
    def mostrarExpandido(self):
        return self.expandido
                           
    #Cambia el estado expandido del nodo
    def cambiarExpandido(self):
        if self.expandido == True:
            self.expandido = False
        else:
            self.expandido = True
    
    #Muestra el nodo padre del nodo actual
    def mostrarPadre(self):
        return self.padre
    
    #Muestra el operador utilizado
    def mostrarOperador(self):
        return self.operador   

    #Calcula los puntos segun la posicion del operador
    def puntosTotal(self,operador,caballo):
        auxiliar=0
        for i in range(len(matriz)):
            for j in range(len(matriz[0])):
                #Encuentra el caballo blanco
                if(self.mostrarPuzzle()[i][j] == caballo):
                    if(operador.lower() == "arribaizquierda"):
                        auxiliar = self.calcularPuntos(i-2,j-1)
                    if(operador.lower() == "arribaderecha"):
                        auxiliar = self.calcularPuntos(i-2,j+1)
                    if(operador.lower() == "derechaarriba"):
                        auxiliar = self.calcularPuntos(i-1,j+2)
                    if(operador.lower() == "derechaabajo"):
                        auxiliar = self.calcularPuntos(i+1,j+2)
                    if(operador.lower() == "abajoizquierda"):
                        auxiliar = self.calcularPuntos(i+2,j-1)
                    if(operador.lower() == "abajoderecha"):
                        auxiliar = self.calcularPuntos(i+2,j+1)
                    if(operador.lower() == "izquierdaarriba"):
                        auxiliar = self.calcularPuntos(i-1,j-2)
                    if(operador.lower() == "izquierdaabajo"):
                        auxiliar = self.calcularPuntos(i+1,j-2)
        return auxiliar 
    
    #Funcion auxiliar del la funcion de arriba: Calcula los puntos
    def calcularPuntos(self, i, j):
        auxiliar = 0
        if self.mostrarPuzzle()[i][j] == 0:
            auxiliar = 0
        if self.mostrarPuzzle()[i][j] == 3:
            if self.mostrarProfundidad() + 1 == 2:
                auxiliar = 1 * 10
            elif self.mostrarProfundidad() + 1 == 4:
                auxiliar = 1 * 5
            else:
                auxiliar = 1
        if self.mostrarPuzzle()[i][j] == 4:
            if self.mostrarProfundidad() + 1 == 2:
                auxiliar = 2 * 10
            elif self.mostrarProfundidad() + 1 == 4:
                auxiliar = 2 * 5
            else:
                auxiliar = 2
        if self.mostrarPuzzle()[i][j] == 5:
            if self.mostrarProfundidad() + 1 == 2:
                auxiliar = 3 * 10
            elif self.mostrarProfundidad() + 1 == 4:
                auxiliar = 3 * 5
            else:
                auxiliar = 3
        if self.mostrarPuzzle()[i][j] == 6:
            if self.mostrarProfundidad() + 1 == 2:
                auxiliar = 4 * 10
            elif self.mostrarProfundidad() + 1 == 4:
                auxiliar = 4 * 5
            else:
                auxiliar = 4
        if self.mostrarPuzzle()[i][j] == 7:
            if self.mostrarProfundidad() + 1 == 2:
                auxiliar = 5 * 10
            elif self.mostrarProfundidad() + 1 == 4:
                auxiliar = 5 * 5
            else:
                auxiliar = 5
        if self.mostrarPuzzle()[i][j] == 8:
            if self.mostrarProfundidad() + 1 == 2:
                auxiliar = 6 * 10
            elif self.mostrarProfundidad() + 1 == 4:
                auxiliar = 6 * 5
            else:
                auxiliar = 6
        if self.mostrarPuzzle()[i][j] == 9:
            if self.mostrarProfundidad() + 1 == 2:
                auxiliar = 7 * 10
            elif self.mostrarProfundidad() + 1 == 4:
                auxiliar = 7 * 5
            else:
                auxiliar = 7
        return auxiliar


#-------------------------------------FUNCIONES DE ALGORITMOS-------------------------------------------


#Comienza el juego segun el nivel elegido
def comenzarJuego(nivel):
    global nivelBot, turno, puntosMaquina, puntosJugador
    botonPrincipiante.config(state=tk.DISABLED)
    botonAmateur.config(state=tk.DISABLED)
    botonExperto.config(state=tk.DISABLED)

    turno = False
    nivelBot = nivel
    puntosMaquina = 0
    puntosJugador = 0
    turnoMaquina(nivelBot)
    #cambiarColores()

#Se encuentra las acciones que tomara la maquina durante su turno
def turnoMaquina(nivel):
    texto = 'Estoy Pensando...'
    varGanar.set(texto)
    ventana.update()  # Actualizar la interfaz gráfica antes de la pausa
    time.sleep(1)

    global turno
    if turno == False:
        #Iniciar Variable
        listaNodos = []
        #Crea el nodo padre
        nodo = Nodo(matriz, None, None, 0, False, None, verPuntosMaquina(),verPuntosJugador())
        listaNodos.append(nodo)
        calcularProfundidad(listaNodos, nivel)
        
        resultado = minimaxAlphaBeta(nodo, nivel, True, float('-inf'), float('inf'))
        print("heuristica es: ", resultado)
        
        if resultado == nodo.puntosCPU - nodo.puntosJugador:
            nodo = elegirAleatorio(nodo, resultado)
            print('Voy a elegir camino aleatorio sin perjudicar mi puntuacion')
            puntosCPU = tomarDecision(resultado, nodo, False)
        else:
            puntosCPU = tomarDecision(resultado, nodo, True)
        
        colocarPuntosMaquina(puntosCPU)
        #Reporte
        texto= verPuntosJugador()
        varJugador.set(texto)
        texto= verPuntosMaquina()
        varMaquina.set(texto)
        texto = 'Termine, te toca'
        varGanar.set(texto)
        
        turno = True
        if terminarJuego(matriz) == True:
            turno = False
            if verPuntosJugador() > verPuntosMaquina():
                texto= "Has Ganado, Felicitaciones! :)"
                varGanar.set(texto)
            elif verPuntosJugador() < verPuntosMaquina():
                texto= "Has perdido, suerte la proxima vez :("
                varGanar.set(texto)
            else:
                texto= "Has empatado, buen intento"
                varGanar.set(texto)
            return 0
        listaNodos.clear()

#Se encuentra las acciones que puede tomar el jugador durante su turno
def turnoJugador(variablei,variablej):
    matrizJuego = matriz
    activar=False
    global turno
    global nivelBot
    #Condicional si es el turno del jugador
    if turno == True:
        posicioni= 0
        posicionj= 0
        #Verifica que se presione los botones adecuados
        for i in range(len(matriz)):
            for j in range(len(matriz[0])):
                #posicion del caballo blanco
                if(matriz[i][j] == 2):
                    posicioni=i
                    posicionj=j
                    if(variablei == (i-1) and variablej == (j-2)):
                        activar=True
                    if(variablei == (i+1) and variablej == (j-2)):
                        activar=True
                    if(variablei == (i-1) and variablej == (j+2)):
                        activar=True
                    if(variablei == (i+1) and variablej == (j+2)):
                        activar=True
                    if(variablei == (i-2) and variablej == (j-1)):
                        activar=True
                    if(variablei == (i-2) and variablej == (j+1)):
                        activar=True
                    if(variablei == (i+2) and variablej == (j-1)):
                        activar=True
                    if(variablei == (i+2) and variablej == (j+1)):
                        activar=True
        #En caso que presione los botones que corresponde
        if activar == True:
            #Si es diferente al caballo blanco no se mueva ni sume puntos
            if matriz[variablei][variablej] != 1:
                #Suma puntos al jugador si coge un numero
                if matriz[variablei][variablej] == 3:
                    sumarPuntosJugador(1)
                if matriz[variablei][variablej] == 4:
                    sumarPuntosJugador(2)
                if matriz[variablei][variablej] == 5:
                    sumarPuntosJugador(3)
                if matriz[variablei][variablej] == 6:
                    sumarPuntosJugador(4)
                if matriz[variablei][variablej] == 7:
                    sumarPuntosJugador(5)
                if matriz[variablei][variablej] == 8:
                    sumarPuntosJugador(6)
                if matriz[variablei][variablej] == 9:
                    sumarPuntosJugador(7)
                matriz[posicioni][posicionj] = 0
                matriz[variablei][variablej] = 2
                actualizarImagen(matriz)
                turno = False
                activar = False
                texto= verPuntosJugador()
                varJugador.set(texto)
                texto= verPuntosMaquina()
                varMaquina.set(texto)
                if terminarJuego(matrizJuego) == True:
                    #Reporte
                    if verPuntosJugador() > verPuntosMaquina():
                        texto= "Has Ganado, Felicitaciones! :)"
                        varGanar.set(texto)
                    elif verPuntosJugador() < verPuntosMaquina():
                        texto= "Has perdido, suerte la proxima vez :("
                        varGanar.set(texto)
                    else:
                        texto= "Has empatado, buen intento"
                        varGanar.set(texto)
                    return 0
                turnoMaquina(nivelBot)

#Termina el juego cuando todos los numeros desaparezcan, si es true termino el juego
def terminarJuego(matrizAuxiliar):
    for i in range(len(matrizAuxiliar)):
            for j in range(len(matrizAuxiliar[0])):
                if(matrizAuxiliar[i][j] == 3 or matrizAuxiliar[i][j] == 4 or matrizAuxiliar[i][j] == 5 or matrizAuxiliar[i][j] == 6 or 
                   matrizAuxiliar[i][j] == 7 or matrizAuxiliar[i][j] == 8 or matrizAuxiliar[i][j] == 9):
                    return False
    return True

#Algoritmo minimax
def minimaxAlphaBeta(nodo, profundidad, maximizar, alpha, beta):
    if profundidad == 0 or terminarJuego(nodo.mostrarPuzzle()):
        # Caso base: alcanzo la profundidad maxima o el juego ha terminado
        heuristica = nodo.mostrarPuntosCPU() - nodo.mostrarPuntosJugador()
        print('El nodo finalizado es: ', nodo.mostrarOperador())
        print('La heuristica es: ',heuristica)
        return heuristica
    
    if maximizar:
        valorMaximo = float('-inf')
        for hijo in nodo.mostrarHijos():
            evaluar = minimaxAlphaBeta(hijo, profundidad - 1, False, alpha, beta)
            valorMaximo = max(valorMaximo, evaluar)
            alpha = max(alpha, evaluar)
            if beta <= alpha:
                break #poda 
        return valorMaximo
    else:
        valorMinimo = float('inf')
        for hijo in nodo.mostrarHijos():
            evaluar = minimaxAlphaBeta(hijo, profundidad - 1, True, alpha, beta)
            valorMinimo = min(valorMinimo, evaluar)
            beta = min(beta, evaluar)
            if beta <= alpha:
                break #poda
        return valorMinimo
    
#Toma el camino que mejor le va a la CPU y devuelve la cantidad de puntos
def tomarDecision(mejorValor, nodo, buenaHeuristica):
    global turnoJugador
    
    #Si la heuristica es buena
    if buenaHeuristica:
        #Busca de manera recursiva el nodo con la mejor heuristica
        nodoActual = buscarValor(mejorValor, nodo)

        #Busca el nodo que le sigue al nodo raiz
        nodoPadre= nodoActual.mostrarPadre()
        while nodoPadre.mostrarPadre() != None:
            nodoActual = nodoPadre
            nodoPadre = nodoPadre.mostrarPadre()
    
    #Si la heuristica no es buena
    else:
        nodoActual = nodo

    nodoGanador = nodoActual
    
    #Movimiento
    #borra el caballo blanco de la matriz
    for i in range(len(matriz)):
            for j in range(len(matriz[0])):
                if matriz[i][j] == 1:
                    matriz[i][j] = 0
                    actualizarImagen(matriz)
    #Coloca el caballo blanco en donde ahora debe ir 
    for i in range(len(matriz)):
            for j in range(len(matriz[0])):
                if nodoGanador.mostrarPuzzle()[i][j] == 1:
                    matriz[i][j] = 1
                    actualizarImagen(matriz)
    print('Me movi a: ', nodoGanador.mostrarOperador())
    return nodoGanador.mostrarPuntosCPU()

#Crea un arbol por medio de profundidad para asignar a cada nodo sus hijos
def calcularProfundidad(listaNodos,nivel):
    nodoGanador=buscarNodoProfundidad(listaNodos, nivel)
    while(nodoGanador != None):
        #Impar (turno del caballo blanco)
        if nodoGanador.mostrarProfundidad() % 2 == 0 or nodoGanador.mostrarProfundidad() == 0:
            turno = True
        #Par (turno del caballo negro)
        else:
            turno = False
        nodoGanador.expandirNodo(listaNodos, turno)
        nodoGanador=buscarNodoProfundidad(listaNodos, nivel)


#--------------------------------FUNCIONES AUXILIARES---------------------------------------------------


#Busca el nodo con la mejor heuristica
def buscarValor(mejorValor, nodo):
    if nodo.mostrarOperador() == None:
        heuristicaNodoActual = -888888888888
    else:
        heuristicaNodoActual = nodo.mostrarPuntosCPU() - nodo.mostrarPuntosJugador()
    
    if heuristicaNodoActual == mejorValor:
        return nodo  # Valor encontrado, retorna el nodo
    
    for hijo in nodo.mostrarHijos():
        resultado = buscarValor(mejorValor, hijo)  # Llamada recursiva para cada hijo
        
        if resultado is not None:
            return resultado  # Si se encuentra el valor en un subárbol, retorna el resultado
    
    return None  # Valor no encontrado en el árbol

#Elige un nodo hijo aleatorio igual a la heuristica, es llamada cuando la heuristica es la misma del nodo raiz
def elegirAleatorio(nodo, heuristica):
    lista = []
    for hijo in nodo.mostrarHijos():
        if(heuristica == hijo.mostrarPuntosCPU() - hijo.mostrarPuntosJugador()):
            lista.append(hijo)
    numeroAleatorio = random.randint(0,len(lista) - 1)
    return lista[numeroAleatorio]

#Suma puntos al jugador
def sumarPuntosJugador(cantidad):
    global puntosJugador
    puntosJugador += cantidad

#Suma puntos a la maquina
def colocarPuntosMaquina(cantidad):
    global puntosMaquina
    puntosMaquina = cantidad

#Permite ver la cantidad de los puntos de la maquina
def verPuntosMaquina():
    global puntosMaquina
    return puntosMaquina

#Permite ver la cantidad de los puntos del jugador
def verPuntosJugador():
    global puntosJugador
    return puntosJugador

#Busca el nodo de la lista con mayor profundidad, elimina los nodos expandidos con mayor profundidad a esta 
#y retorna el nodo con mayor profundidad de izq a derecha 
def buscarNodoProfundidad(lista, nivel):
    #variables auxiliares necesarias
    auxiliar = 0
    auxiliar2 = []
    
    #Busca el nodo de mayor profundidad hasta el limite del nivel sin haberse expandido
    for i in range(0,len(lista)):
        if(lista[i].mostrarProfundidad() > auxiliar and lista[i].mostrarExpandido() == False):
            #Se guarda la profundidad maxima 
            if lista[i].mostrarProfundidad() < nivel: 
                auxiliar = lista[i].mostrarProfundidad()

    #Busca los nodos de mayor profundidad que se expandieron y los anota en un auxiliar
    for i in range(0,len(lista)):
        if(lista[i].mostrarProfundidad() > auxiliar and lista[i].mostrarExpandido() == True):
            auxiliar2.append(i)

    #los elimina de la lista de nodos
    for i in range(0,len(auxiliar2)):
        lista.pop(auxiliar2[i])
        auxiliar2 = [x-1 for x in auxiliar2]
            
    #Busca el nodo de mayor profundidad sin haberse expandido, pero retornando el primero que se encuentre, de izq a derecha
    for i in range(0,len(lista)):
        if(auxiliar == lista[i].mostrarProfundidad() and lista[i].mostrarExpandido() == False):
            return lista[i]
    return None 
        
#Define que numero es de la matriz y coloca la imagen correspondiente
def colocarImagen(matrizPadre,numero1,numero2):
    if(matrizPadre[numero1][numero2] == 0):
        boton[numero1][numero2].config(image=imagen0)
    elif(matrizPadre[numero1][numero2] == 1):
        boton[numero1][numero2].config(image=imagencaballob)
    elif(matrizPadre[numero1][numero2] == 2):
        boton[numero1][numero2].config(image=imagencaballon)
    elif(matrizPadre[numero1][numero2] == 3):
        boton[numero1][numero2].config(image=imagen3)
    elif(matrizPadre[numero1][numero2] == 4):
        boton[numero1][numero2].config(image=imagen4)
    elif(matrizPadre[numero1][numero2] == 5):
        boton[numero1][numero2].config(image=imagen5)
    elif(matrizPadre[numero1][numero2] == 6):
        boton[numero1][numero2].config(image=imagen6)
    elif(matrizPadre[numero1][numero2] == 7):
        boton[numero1][numero2].config(image=imagen7)
    elif(matrizPadre[numero1][numero2] == 8):
        boton[numero1][numero2].config(image=imagen8)
    elif(matrizPadre[numero1][numero2] == 9):
        boton[numero1][numero2].config(image=imagen9)

#Coloca los elementos de la matriz de manera aleatoria 
def aleatorizarTablero():
    for i in range(1,10):
        colocado = False
        while(colocado==False):
            posicionI=random.randint(0,7)
            posicionJ=random.randint(0,7)
            if(matriz[posicionI][posicionJ] == 0):
                matriz[posicionI][posicionJ] = i
                colocado = True
    
#Actualiza la pestaña grafica
def actualizarImagen(matriz):
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            colocarImagen(matriz,i,j)
    ventana.update()


#-------------------------------------Matriz y GUI--------------------------------------------------------

#Inicializacion de la matriz
maxRC=8 
matriz = [[0 for j in range(maxRC)] for i in range(maxRC)]
boton = [[0 for j in range(maxRC)] for i in range(maxRC)]
#para comprobar que se inicializa print(matriz)

#Coloca los caballos y los numeros de manera aleatoria
aleatorizarTablero()

# Carga las imagenes
imagencaballob = tk.PhotoImage(file = "./images/caballob.png")
imagencaballon = tk.PhotoImage(file = "./images/caballon.png")
imagen0 = tk.PhotoImage(file = "./images/0.png")
imagen3 = tk.PhotoImage(file = "./images/1.png")
imagen4 = tk.PhotoImage(file = "./images/2.png")
imagen5 = tk.PhotoImage(file = "./images/3.png")
imagen6 = tk.PhotoImage(file = "./images/4.png")
imagen7 = tk.PhotoImage(file = "./images/5.png")
imagen8 = tk.PhotoImage(file = "./images/6.png")
imagen9 = tk.PhotoImage(file = "./images/7.png")


# Recorrer la matriz y crear etiquetas para cada elemento
for i in range(len(matriz)):
    for j in range(len(matriz[0])):
        etiqueta = tk.Button(ventana, text=matriz[i][j], command=lambda i=i, j=j: turnoJugador(i,j))
        boton[i][j]=etiqueta
        colocarImagen(matriz,i,j)
        etiqueta.grid(row=i, column=j)

botonPrincipiante = tk.Button(ventana, text="Principiante", command=lambda: comenzarJuego(2))
botonPrincipiante.place(x=300, y = 580)
botonAmateur = tk.Button(ventana, text="Amateur", command=lambda: comenzarJuego(4))
botonAmateur.place(x=300, y = 620)
botonExperto = tk.Button(ventana, text="Experto", command=lambda: comenzarJuego(6))
botonExperto.place(x=300, y = 660)

#Añadir reporte
varJugador = tk.StringVar()
varJugador.set("")
varMaquina = tk.StringVar()
varMaquina.set("")
varGanar = tk.StringVar()
varGanar.set("")
titulo1 = tk.Label(ventana, text="PUNTUACION")
titulo1.place(x=50, y=550)
titulo2 = tk.Label(ventana, text="ELIGE DIFICULTAD PARA COMENZAR")
titulo2.place(x=300, y=550)
reporte11 = tk.Label(ventana, text="Los puntos del jugador son: ")
reporte11.place(x=50, y=580)
reporte1 = tk.Label(ventana, textvariable= varJugador)
reporte1.place(x=205, y=580)
reporte22 = tk.Label(ventana, text="Los puntos del contrincante son: ")
reporte22.place(x=50, y=620)
reporte2 = tk.Label(ventana, textvariable=varMaquina)
reporte2.place(x=230, y=620)
reporteGanar = tk.Label(ventana, textvariable=varGanar)
reporteGanar.place(x=50, y=660)
# Iniciar el bucle principal de la ventana
ventana.mainloop()