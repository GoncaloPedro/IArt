from mailbox import linesep


# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

from multiprocessing.sharedctypes import Value
from pickle import FALSE
import numpy as np
import sys
"""from tkinter import N"""
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class TakuzuState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = TakuzuState.state_id
        TakuzuState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Takuzu."""
    
    def __init__(self, board:list, lines:int):
        if (lines <= 0):
            raise ValueError

        self.side = lines
        self.matrix = np.array(board)
    
    
    @staticmethod
    def valid_value(value: int):
        return value >= 0 and value <= 2


    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        try:
            return self.matrix[row][col]
        except LookupError:
            raise LookupError
    
    
    def get_row(self, row: int):
        """Devolve uma linha do tabuleiro"""
        try:
            return self.matrix[row]
        except LookupError:
            raise LookupError
    

    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        output = ()
        
        try:
            output += (self.get_number(row + 1, col),)
        except LookupError:
            output += (None,)
        try:
            output += (self.get_number(row - 1, col),)
        except LookupError:
            ouput += (None,)
        
        return output


    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        output = ()
        
        try:
            output += (self.get_number(row, col - 1),)
        except LookupError:
            output += (None,)
        try:
            output += (self.get_number(row, col + 1),)
        except LookupError:
            output += (None,)
        
        return output


    def change_cell(self, row: int, col:int, value: int):
        """Muda o valor numa dada célula do tabuleiro"""
        if (not Board.valid_value()):
            raise ValueError("Board.change_cell: O valor a inserir é inválido")
        
        try:
            self.matrix[row][col] = value
        except LookupError:
            raise LookupError("Board.change_cell: Posição inválida")
        

    @staticmethod
    def parse_instance_from_stdin():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 takuzu.py < input_T01

            > from sys import stdin
            > stdin.readline()
        """
        input_file = sys.stdin.readlines()

        board = []
        for it, line in enumerate(input_file):
            if (it > 0):
                line = line.split('\t')
                board.append([int(num) for num in line])
            else:
                num_lines = int(line[0])


        return Board(board, num_lines)        


    def __str__(self):
        # TODO ver se há forma mais eficaz de iterar numpy arrays
        out = ""
        
        for row in range(self.side):
            for col in range(self.side):
                out += str(self.get_number(row, col))
                if col < (self.side - 1):
                    out += '\t'
            
            out += '\n'
        return out

    # TODO: outros metodos da classe


class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial_state = board
        
        # TODO
        pass

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        # TODO
        pass

    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        # TODO
        pass

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        # TODO
        pass

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass
    
    def equal_zeros_ones(board: Board, sum):
        """Funcao auxiliar permite verificar a condicao, da existencia de um
        número igual de 1s e 0s em cada linha e coluna (ou mais um para grelhas
        de dimensão ímpar, do estado objetivo"""
        even = board.side % 2
        if (even):
            return sum == board.side
        else:
            return sum == (board.side + 1) or sum == (board.side - 1)

    def valid_rows(board: Board):
        """Funcao que verifica a condicao de igualdade de 1 ou 0 nas linhas da grelha"""
        for i in range(Board.side):
            if (not equal_zeros_ones(board, numpy.sum(board.get_row(i)) != (board.side / 2))):
                return False


    def valid_columns(board: Board):
        """Funcao que verifica a condicao de igualdade de 1 ou 0 nas colunas da grelha"""
        for col in range(board.side):
            sum = 0
            for row in range(board.side):
                sum += board.get_value(row, col)
            if (not equal_zeros_ones(board, sum)):
                return False


    

if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    board = Board.parse_instance_from_stdin()

    print("Initial:\n", board, sep="")

    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
