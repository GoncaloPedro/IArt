# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

from multiprocessing.sharedctypes import Value
import sys
from tkinter import N
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
    
    def __init__(self, size: int):
        if (size <= 0):
            raise ValueError
        
        self.side = size;
        self.matrix = [[] for i in range(size)]
    
    
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
            output.append(self.get_number(row + 1, col))
        except LookupError:
            output.append(None)
        try:
            output.append(self.get_number(row - 1, col))
        except LookupError:
            output.append(None)
        
        """if ((row + 1) == self.side):
            output.append(None)
        else:
            output.append(self.get_number(row + 1, col))
        if ((row - 1) < 0):
            output.append(None)
        else:
            output.append(self.get_number(row - 1, col))"""
        
        return output


    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        output = ()
        
        try:
            output.append(self.get_number(row, col - 1))
        except LookupError:
            output.append(None)
        try:
            output.append(self.get_number(row, col + 1))
        except LookupError:
            output.append(None)
        
        """if ((col - 1) < 0):
            output.append(None)
        else:
            output.append(self.get_number(row, col - 1))
        if ((col + 1) == self.side):
            output.append(None)
        else:
            output.append(self.get_number(row, col + 1))"""
        
        return output


    def change_cell(self, row: int, col:int, value: int):
        """Muda o valor numa dada célula do tabuleiro"""
        if (not Board.valid_value()):
            raise ValueError("Board.change_cell: O valor a inserir é inválido")
        
        try:
            self.matrix[row][col] = value
        except LookupError:
            raise LookupError("Board.change_cell: Posição inválida")
        
        
    def __append_to_row(self, row: int, value: int):
        """Acrescenta uma coluna com o valor value na linha row"""
        if (Board.valid_value(value)):
            try:
                self.get_row(row).append(value)
            except LookupError:
                raise LookupError
        else:
            raise ValueError


    @staticmethod
    def parse_instance_from_stdin():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 takuzu.py < input_T01

            > from sys import stdin
            > stdin.readline()
        """
        file_name = sys.argv[1]
        with open(file_name) as f:
            num_lines = int(f.read(2))
            
            board = Board(num_lines)
            for i in range(num_lines):
                # Leitura da linha i do tabuleiro de jogo
                row = board.get_row()
                
                c = f.read(1)
                while (c != '\n'):
                    if (c.isnumeric()):
                        #board[i].append(int(c))
                        try:
                            board.__append_to_row(i, int(c))
                        except ValueError:
                            raise ValueError("parse_instance_from_stdin: " +
                                             "tabuleiro inválido")
                    
                    c = f.read(1)
        
        return board


    def __str__(self):
        out = ""
        
        for row in range(self.side):
            for col in range(self.side):
                out += self.get_number(row, col)
                if col < (self.side - 1):
                    out += '\t'
            
            out += '\n'
        return out

    # TODO: outros metodos da classe


class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
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

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
