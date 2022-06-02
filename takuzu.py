# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
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

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Takuzu."""
    
    def __init__(self, board, lines:int):
        if (lines <= 0):
            raise ValueError
        
        if (isinstance(board, np.ndarray)):
            self.matrix = board
        else:
            self.matrix = np.array(board)

        self.side = lines
        
        self.x = 0
    
    
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
        return (None in self.adjacent_horizontal_numbers(row, col) or
                None in self.adjacent_vertical_numbers(row, col))
    
    
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
        #if (not Board.valid_value(value)):
        #    raise ValueError("Board.change_cell: O valor a inserir é inválido")
        
        self.matrix[row][col] = value
        

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
                num_lines = int(line)


        return Board(board, num_lines)
    
    
    def deep_copy(self):
        side = board.side
        
        new_board = Board(np.ndarray(shape=(side, side), dtype=int), side)
        
        
        for row in range(board.side):
            for col in range(board.side):
                new_board.change_cell(row, col, int(self.get_number(row, col)))
        
        new_board.x = self.x
        
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

    # TODO: outros metodos da classe


class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""
        self.initial_state = TakuzuState(board)
        super().__init__(self.initial_state)
        
        # TODO
        pass

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
                        # TODO remove
                        continue
                    if (option == -1):
                        option = self.pick_conditioned_by_number_of_occurences(row, col, state.board)


                    if (option != -1):
                        actions += [(row, col, option)]
                        action_picked = True
                        break
            row = row + 1
            
        row = 0
        while (row < side and not action_picked):
            for col in range(side):
                if (state.board.is_empty_cell(row, col)):
                    actions += [(row, col, 0), (row, col, 1)]
                    action_picked = True
                    break
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
        new_board.x += 1

        return TakuzuState(new_board)

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""
        board = state.board
        num_occ = True
        for i in range(board.side):
        
            num_0 = 0
            num_1 = 0
            for j in range(board.side):
                if (board.get_number(j, i) == 2):
                    return False
                if (board.get_number(j, i) == 1):
                    num_1 += 1
                if (board.get_number(j, i) == 0):
                    num_0 += 1
                    
            if (num_0 >= num_1):
                num_occ = self.check_num_occurences(board.side, num_0)
            else:
                num_occ = self.check_num_occurences(board.side, num_1)
            if (not num_occ):
                return False
                
        # TODO podemos optimizar ao meter o código do check_adjacencies no for ali em cima
        
        return self.check_adjacencies(board) and self.check_equal_lines(board)
            

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""
        # TODO
        pass


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
        
        if (board.side < 3):
            vizinhos = [num for num in vertical if isinstance(num, int)]
            vizinhos += [num for num in horiz if isinstance(num, int)]
            
            for num in vizinhos:
                if (num != 2): # TODO Este 2 estar aqui é má abstração
                    return Takuzu.get_complementary_value(num)
            return -1
            
        
        horizontal_move = self.horizontal_adjacencies(row, col, horiz, board)
        vertical_move = self.vertical_adjacencies(row, col, vertical, board)
        
        if ((horizontal_move != vertical_move) and (horizontal_move != -1) and (vertical_move != -1)):
            # Há inconsistências e o tabuleiro já é inválido
            return -2
        elif (horizontal_move != -1):
            return horizontal_move
        elif (vertical_move != -1):
            return vertical_move
        
        return -1
    
    
    def horizontal_adjacencies(self, row: int, col: int, horiz, board: Board):
        # TODO 
        # TODO Ver se dá para cortar ramos
        # TODO
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
        # TODO
        # TODO Ver se dá para cortar ramos
        # TODO
        if (vert[0] == vert[1]):
            return Takuzu.get_complementary_value(vert[0])
        
        elif (not (row in (0,1)) and (vert[0] == board.get_number(row - 2, col))):
            return Takuzu.get_complementary_value(vert[0])
        
        elif (not (row in (board.side - 2, board.side - 1)) and 
              (vert[1] == board.get_number(row + 2, col))):
            return Takuzu.get_complementary_value(vert[1])
        
        return -1
        
    
        
    def adjacencies_edge_cell(self, row: int, col: int, vert_adj: list,
                                  horiz_adj: list, board: Board):
        if (None in vert_adj or row in (1, board.side - 2)):
            move = self.edge_cell_vertical_adjacencies(row, col, vert_adj, board)
            if (move != -1):
                return move
        if (None in horiz_adj or col in (1, board.side - 2)):
            return self.edge_cell_horizontal_adjacencies(row, col, horiz_adj, board)


    def edge_cell_vertical_adjacencies(self, row: int, col: int, vert_adj: list,
                                       board: Board):
        if (None == vert_adj[0] or row == 1):
            if (vert_adj[1] == board.get_number(row + 2, col)):
                return Takuzu.get_complementary_value(vert_adj[1])
            
        elif (None == vert_adj[1] or row == (board.side - 2)):
            if (vert_adj[0] == board.get_number(row - 2, col)):
                return Takuzu.get_complementary_value(vert_adj[0])
        
        return -1
        
        
    def edge_cell_horizontal_adjacencies(self, row: int, col: int, horiz_adj: list,
                                         board: Board):
        if (None == horiz_adj[0] or col == 1):  # None imediatamente a esquerda
            if (horiz_adj[1] == board.get_number(row, col + 2)):
                return Takuzu.get_complementary_value(horiz_adj[1])
        
        elif (None == horiz_adj[1] or col == (board.side - 2)):
            if (horiz_adj[0] == board.get_number(row, col - 2)):
                return Takuzu.get_complementary_value(horiz_adj[0])
    
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
        # TODO
        # TODO abstrair os ifs para outra função
        # TODO
        # TODO Tentar cortar ramos desnecessários ou comparar o resultado das colunas vs linhas
        # TODO
        
        num_0 = 0
        num_1 = 0
        for num in board.get_row(row):
            if (num == 0):
                num_0 += 1
            elif (num == 1):
                num_1 += 1
        
        if (num_0 > num_1 and self.check_num_occurences(board.side, num_0)):
            return 1
        elif (num_1 > num_0 and self.check_num_occurences(board.side, num_1)):
            return 0

        num_0 = 0
        num_1 = 0
        for row_n in range(board.side):
            if (board.get_number(row_n, col) == 0):
                num_0  += 1
            elif (board.get_number(row, col) == 1):
                num_1 += 1
                
        if (num_0 > num_1 and self.check_num_occurences(board.side, num_0)):
            return 1
        elif (num_1 > num_0 and self.check_num_occurences(board.side, num_1)):
            return 0
        
        return -1
        
    
    def check_adjacencies(self, board: Board):
        
        for i in range(board.side):
            row = board.get_row(i)
            size = board.side
            if (not self.check_row(row,size, row[0], 2, 0)):
                return False
            if (not self.check_column(board, board.get_number(0, i), 2, i, 0)):
                return False
            
        return True
    

    def check_row(self, row, size_row: int, last_value: int, limit: int,
                  index: int):
        
        if (index == size_row):
            return True
        elif (limit == 0 and row[index] == last_value):
            if (row[index] == last_value):
                return False
            else:
                return self.check_row(row,size_row,row[index], 2, index + 1)
        elif (index == 0):
            return self.check_row(row, size_row, row[index], limit - 1, index + 1)
        elif (row[index] == last_value):
            return self.check_row(row,size_row,last_value, limit - 1, index + 1)
        else:
            return self.check_row(row,size_row,row[index], 2, index + 1)


    def check_column(self, board: Board, last_value: int, limit: int, col: int,
                    row: int):
        
        # TODO juntar os 2 elses num só
        
        if (row == board.side):
            return True
        elif (limit == 0 and board.get_number(row, col) == last_value):
            if (board.get_number(row, col) == last_value):
                return False
            else:
                return self.check_column(board, board.get_number(row, col), 2, col, row + 1)
        elif (row == 0):
            return self.check_column(board, board.get_number(row, col), limit - 1, col, row + 1)
        elif (board.get_number(row, col) == last_value):
            return self.check_column(board, last_value, limit - 1, col, row + 1)
        else:
            return self.check_column(board, board.get_number(row, col), 2, col, row + 1)
        
    
    def check_equal_lines(self, board: Board):
        size = board.side
        
        for row_1 in range(board.side):
            for row_2 in range(board.side):
                col_equalities = 0
                row_equalities = 0
                
                if (row_1 == row_2):
                    continue
                
                for i in range(board.side):
                    if (board.get_number(row_1, 1) == board.get_number(row_2, i)):
                        row_equalities += 1
                    if (board.get_number(i, row_1) == board.get_number(i, row_2)):
                        col_equalities += 1

                    if (row_equalities == board.side or col_equalities == board.side):
                        return False
        
        return True
        
        
    
    # TODO: outros metodos da classe


if __name__ == "__main__":

    board = Board.parse_instance_from_stdin()
    #print("Initial:")
    #print(board)
    problem = Takuzu(board)

    solution_node = depth_first_tree_search(problem)
    if (solution_node != None):
        solution_state = solution_node.state
        final_board = solution_state.board
        print(final_board)
