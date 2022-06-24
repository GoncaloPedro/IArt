# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 67:
# 99229 Gonçalo Nunes
# 99297 Pedro Cruz

import numpy as np
import sys
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



class Board:
    """Representação interna de um tabuleiro de Takuzu."""

    def __init__(self, board, lines:int, free: int):
        if (lines <= 0):
            raise ValueError

        if (isinstance(board, np.ndarray)):
            self.matrix = board
        else:
            self.matrix = np.array(board)

        self.side = lines
        self.free_cells = free


    @staticmethod
    def valid_value(value: int):
        return value >= 0 and value <= 2


    def get_number(self, row: int, col: int) -> int:
        """Devolve o valor na respetiva posição do tabuleiro."""
        return self.matrix[row][col]
        
        
    def is_empty_cell(self, row: int, col: int) -> bool:
        """Devolve True se a célula está vazia, False caso contrário"""
        return self.get_number(row, col) == 2
    
    
    def is_edge_cell(self, row: int, col:int) -> bool:
        """Devolve True se a célula está num dos lados do tabuleiro"""
        return row in (0, board.side - 1) or col in (0, board.side - 1)
    
    
    def get_row(self, row: int):
        """Devolve uma linha do tabuleiro"""
        return self.matrix[row]
        

    def adjacent_vertical_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        output = ()

        if (row != 0):
            output += (self.get_number(row - 1, col),)
        else:
            output += (None,)
        if (row == (self.side - 1)):
            output += (None,)
        else:
            output += (self.get_number(row + 1, col),)

        return output


    def adjacent_horizontal_numbers(self, row: int, col: int) -> (int, int):
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        output = ()
        
        if (col == 0):
            output += (None,)
        else:
            output += (self.get_number(row, col - 1),)
        if (col == (self.side - 1)):
            output += (None,)
        else:
            output += (self.get_number(row, col + 1),)
        
        return output


    def change_cell(self, row: int, col:int, value: int):
        """Muda o valor numa dada célula do tabuleiro"""
        self.matrix[row][col] = value
        self.free_cells = self.free_cells - 1


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
        free_cells = 0
        for it, line in enumerate(input_file):
            if (it > 0):
                line = line.split('\t')
                row = [int(num) for num in line]
                free_cells += row.count(2)
                board.append(row)
            else:
                num_lines = int(line)


        return Board(board, num_lines, free_cells)
    
    
    def deep_copy(self):
        side = board.side
        
        new_board = Board(np.ndarray(shape=(side, side), dtype=int), side, self.free_cells)
        
        
        for row in range(board.side):
            for col in range(board.side):
                new_board.change_cell(row, col, int(self.get_number(row, col)))
        
        new_board.free_cells = self.free_cells
        
        
        return new_board


    def __str__(self):
        out = ""
        
        for row in range(self.side):
            for col in range(self.side):
                out += str(self.get_number(row, col))
                if col < (self.side - 1):
                    out += '\t'
            
            if (row != (self.side - 1)):
                out += '\n'
        return out


class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial_state = TakuzuState(board)
        super().__init__(self.initial_state)
        

    def actions(self, state: TakuzuState):
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""
        
        
        side = state.board.side
        actions = []
        action_picked = False
        row = 0
        while (row < side and not action_picked):
            for col in range(side):
                if (state.board.is_empty_cell(row, col)):
                    option = self.pick_conditioned_by_adjacencies(row, col, state.board)
                    
                    if (option == -2):
                        # Kill this branch
                        actions = []
                        action_picked = True
                        break
                    if (option == -1):
                        option = self.pick_conditioned_by_number_of_occurences(row, col, state.board)
                        if (option == -2):
                            # Kill this branch
                            actions = []
                            action_picked = True
                            break

                    if (option != -1):
                        actions = [(row, col, option)]
                        action_picked = True
                        break
                    elif (option == -1):
                        actions = [(row, col, 0), (row, col, 1)]


            row = row + 1
        

        return actions


    def result(self, state: TakuzuState, action):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""
        board = state.board
        new_board = board.deep_copy()
        
        new_board.change_cell(action[0], action[1], action[2])

        return TakuzuState(new_board)

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        board = state.board
        size = board.side
        if (board.free_cells == 0):
            num_occ_col = True
            num_occ_row = True
            for i in range(size):
            
                num_0_col = 0
                num_1_col = 0
                num_0_row = 0
                num_1_row = 0
                col_limit = 0
                col_last_value = -1
                row_limit = 0
                row_last_value = -1
                for j in range(size):
                    if (board.get_number(j, i) == 2):
                        return False
                    if (board.get_number(j, i) == 1):
                        num_1_col += 1
                    if (board.get_number(j, i) == 0):
                        num_0_col += 1
                    if (board.get_number(i, j) == 0):
                        num_0_row += 1
                    if (board.get_number(i, j) == 1):
                        num_1_row += 1
                    if (board.get_number(j, i) == col_last_value):
                        col_limit += 1
                    else:
                        col_limit = 1
                    if (board.get_number(i, j) == row_last_value):
                        row_limit += 1
                    else:
                        row_limit = 1
                    
                    if (col_limit == 3 or row_limit == 3):
                        return False
                    col_last_value = board.get_number(j, i)
                    row_last_value = board.get_number(i, j)
                        
                if (num_0_col >= num_1_col and num_0_col >= int((size) / 2)):
                    num_occ_col = self.check_num_occurences(size, num_0_col)
                elif (num_1_col > num_0_col and num_1_col >= int(size / 2)):
                    num_occ_col = self.check_num_occurences(size, num_1_col)
                if (num_0_row >= num_1_row and num_0_row >= int((size) / 2)):
                    num_occ_row = self.check_num_occurences(size, num_0_row)
                elif (num_1_row > num_0_row and num_1_row >= int(size / 2)):
                    num_occ_row = self.check_num_occurences(size, num_1_row)
                if (not num_occ_col or not num_occ_row):
                    return False            
                    
            return self.check_equal_lines(board)

        return False


    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        return node.state.board.free_cells


    @staticmethod
    def get_complementary_value(value: int) -> int:
        if (value == 1):
            return 0
        elif (value == 0):
            return 1
        else:
            return -1


    def pick_conditioned_by_adjacencies(self, row: int, col: int, board: Board) -> int:
        vertical = board.adjacent_vertical_numbers(row, col)
        horiz = board.adjacent_horizontal_numbers(row, col)
        
        horizontal_move = self.horizontal_adjacencies(row, col, horiz, board)
        vertical_move = self.vertical_adjacencies(row, col, vertical, board)
        
        
        if (horizontal_move != -1):
            if (vertical_move == Takuzu.get_complementary_value(horizontal_move)):
                # Kill this branch
                return -2
            return horizontal_move
        elif (vertical_move != -1):
            return vertical_move
        
        return -1


    def horizontal_adjacencies(self, row: int, col: int, horiz, board: Board):
        if (horiz[0] == horiz[1]):
            return Takuzu.get_complementary_value(horiz[0])
        
        elif (not (col in (board.side - 2, board.side - 1)) and 
              (horiz[1] == board.get_number(row, col + 2))):
            
            return Takuzu.get_complementary_value(horiz[1])
        
        elif (not (col in (0, 1)) and
              (horiz[0] == board.get_number(row, col - 2))):
            
            return Takuzu.get_complementary_value(horiz[0])
        
        return -1


    def vertical_adjacencies(self, row: int, col: int, vert, board: Board):
        if (vert[0] == vert[1]):
            return Takuzu.get_complementary_value(vert[0])
        
        elif (not (row in (0,1)) and (vert[0] == board.get_number(row - 2, col))):
            return Takuzu.get_complementary_value(vert[0])
        
        elif (not (row in (board.side - 2, board.side - 1)) and 
              (vert[1] == board.get_number(row + 2, col))):
            return Takuzu.get_complementary_value(vert[1])
        
        return -1

    
    def check_num_occurences(self, board_size: int, num_occurences: int):
        """Funcao que permite ver se o número de ocorrências de 0s ou 1s,
        numa linha ou tabuleiro, já atingiu o limite válido. Se num_occurences
        for a soma dos valores, permite ver se a linha/coluna está totalmente,
        preenchida com o número certo de 0s e 1s"""
        uneven = board_size % 2
        
        if (uneven):
            return num_occurences == int(board_size / 2 + 1)
        else:
            return num_occurences == int(board_size / 2)
    
    
    def pick_conditioned_by_number_of_occurences(self, row: int, col: int, board: Board):

        num_0_row = 0
        num_1_row = 0
        num_0_col = 0
        num_1_col = 0
        for i in range(board.side):
            row_val = board.get_number(row, i)
            col_val = board.get_number(i, col)
            if (row_val == 0):
                num_0_row += 1
            elif (row_val == 1):
                num_1_row += 1
            if (col_val == 0):
                num_0_col += 1
            elif (col_val == 1):
                num_1_col += 1

        valid_row_0 = self.check_num_occurences(board.side, num_0_row)
        valid_row_1 = self.check_num_occurences(board.side, num_1_row)
        valid_col_0 = self.check_num_occurences(board.side, num_0_col)
        valid_col_1 = self.check_num_occurences(board.side, num_1_col)

        if (num_0_row > num_1_row and valid_row_0):
            if (num_1_col > num_0_col and valid_col_1):
                return -2
            return 1
        elif (num_1_row > num_0_row and valid_row_1):
            if (num_0_col > num_1_col and valid_col_0):
                return -2
            return 0
        if (num_0_col > num_1_col and valid_col_0):
            return 1
        elif (num_1_col > num_0_col and valid_col_1):
            return 0


        return -1


    def check_equal_lines(self, board: Board):
        size = board.side
        
        for row_1 in range(size):
            for row_2 in range(row_1 + 1, size):
                col_equalities = 0
                row_equalities = 0
                
                
                for i in range(size):
                    if (board.get_number(row_1, i) == board.get_number(row_2, i)):
                        row_equalities += 1
                    if (board.get_number(i, row_1) == board.get_number(i, row_2)):
                        col_equalities += 1

                    if (row_equalities == size or col_equalities == size):
                        return False
        
        return True


if __name__ == "__main__":
    
    board = Board.parse_instance_from_stdin()
    problem = Takuzu(board)

    solution_node = depth_first_tree_search(problem)
    #solution_node = greedy_search(problem)
    if (solution_node != None):
        solution_state = solution_node.state
        final_board = solution_state.board
        print(final_board)
