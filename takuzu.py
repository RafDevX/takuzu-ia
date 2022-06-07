# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

from copy import deepcopy
from sys import stdin
from typing import List, Tuple, Union
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)


class Board:
    """Representação interna de um tabuleiro de Takuzu."""

    matrix: Tuple[Tuple[int]]
    domains: Tuple[Tuple[Tuple[int]]]
    size: int
    free_squares: int

    def __init__(self, matrix: Tuple[Tuple[int]], domains: Tuple[Tuple[Tuple[int]]], size: int, free_squares: int):
        """Construtor.
        Recebe uma matriz de inteiros representando o tabuleiro.
        """

        self.matrix = matrix
        self.domains = domains
        self.size = size
        self.free_squares = free_squares

    def __str__(self):
        """Imprime o tabuleiro."""

        string = ""
        for row in self.matrix:
            string += "\t".join(str(x) for x in row) + "\n"
        return string

    def __repr__(self) -> str:
        """Representação interna do tabuleiro."""

        return f"Board({self.size}, {self.matrix})"

    def get_number(self, row: int, col: int) -> Union[int, None]:
        """Devolve o valor na respetiva posição do tabuleiro, ou None se a posição for inválida."""

        if row < 0 or row >= self.size or col < 0 or col >= self.size:
            return None
        return self.matrix[row][col]

    def adjacent_vertical_numbers(self, row: int, col: int) -> Tuple[Union[int, None], Union[int, None]]:
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""

        return (self.get_number(row - 1, col), self.get_number(row + 1, col))

    def adjacent_horizontal_numbers(self, row: int, col: int) -> Tuple[Union[int, None], Union[int, None]]:
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""

        return (self.get_number(row, col - 1), self.get_number(row, col + 1))

    def get_column(self, col: int) -> Tuple[int]:
        """Devolve a coluna indicada."""

        return (row[col] for row in self.matrix)

    def get_row(self, row: int) -> Tuple[int]:
        """Devolve a linha indicada."""

        return self.matrix[row]

    def count_1s_col(self, col: int) -> int:
        """Devolve o número de 1s na coluna indicada."""

        return self.get_column(col).count(1)

    def count_1s_row(self, row: int) -> int:
        """Devolve o número de 1s na linha indicada."""

        return self.get_row(row).count(1)

    def count_0s_col(self, col: int) -> int:
        """Devolve o número de 0s na coluna indicada."""

        return self.get_column(col).count(0)

    def count_0s_row(self, row: int) -> int:
        """Devolve o número de 0s na linha indicada."""

        return self.get_row(row).count(0)

    # Não estamos a usar esta função, mas pode ser útil para implementar outras funções.
    def check_valid_row(self, row: int) -> bool:
        """Devolve True se a linha indicada for válida."""

        for n in range(self.size):
            number = self.get_number(row, n)
            if number == None:
                return False
            (left, right) = self.adjacent_horizontal_numbers(row, n)
            if number == right:
                left, right = self.adjacent_horizontal_numbers(row, n + 1)
                if right == number:
                    return False
        return True

    # Não estamos a usar esta função, mas pode ser útil para implementar outras funções.
    def check_valid_col(self, col: int) -> bool:
        """Devolve True se a coluna indicada for válida."""

        for n in range(self.size):
            number = self.get_number(n, col)
            if number == None:
                return False
            (up, down) = self.adjacent_vertical_numbers(n, col)
            if number == down:
                up, down = self.adjacent_vertical_numbers(n + 1, col)
                if down == number:
                    return False
        return True

    def has_repeated_rows(self) -> bool:
        """Devolve True se o tabuleiro tiver linhas repetidas."""

        for n in range(self.size):
            if self.matrix.count(self.get_row(n)) > 1:
                return True
        return False

    def has_repeated_cols(self) -> bool:
        """Devolve True se o tabuleiro tiver colunas repetidas."""

        for n in range(self.size):
            if self.matrix.count(self.get_column(n)) > 1:
                return True
        return False

    def possible_values_for_square(self, row: int, col: int) -> List[int]:
        """Devolve uma lista com os valores possíveis para a posição indicada."""

        possible_values = []

        if self.get_number(row, col) != 2:
            return possible_values

        for x in (0, 1):
            ok = True

            for (adj_fn, abs_delta) in (
                (self.adjacent_vertical_numbers, (1, 0)),
                (self.adjacent_horizontal_numbers, (0, 1)),
            ):
                (before, after) = adj_fn(row, col)
                if x == before == after:
                    ok = False
                    break
                if before == x:
                    if adj_fn(row - abs_delta[0], col - abs_delta[1])[0] == x:
                        ok = False
                        break
                if after == x:
                    if adj_fn(row + abs_delta[0], col + abs_delta[1])[1] == x:
                        ok = False
                        break

            if ok:
                possible_values.append(x)

        return possible_values

    def place(self, row: int, col: int, value: int):
        """Devolve um novo tabuleiro com o valor colocado na posição indicada."""

        copy_matrix = [[self.matrix[i][j] for j in range(len(self.matrix[i]))] for i in range(self.size)]
        copy_matrix[row][col] = value
        new_matrix = tuple(tuple(row) for row in copy_matrix)
        return Board(new_matrix, self.size, self.free_squares - 1)

    def filled(self):
        return self.free_squares == 0

    @staticmethod
    def parse_instance_from_stdin():
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 takuzu.py < input_T01

            > from sys import stdin
            > stdin.readline()
        """

        size = int(stdin.readline())
        free_squares = size * size
        matrix = []
        for _ in range(size):
            row = []
            for entry in stdin.readline().split("\t"):
                row.append(int(entry))
                if int(entry) != 2:
                    free_squares -= 1
            matrix.append(tuple(row))
        matrix = tuple(matrix)
        return Board(matrix, size, free_squares)


class TakuzuState:
    state_id = 0
    board: Board

    def __init__(self, board):
        self.board = board
        self.id = TakuzuState.state_id
        TakuzuState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id

    def place(self, row: int, col: int, value: int):
        return TakuzuState(self.board.place(row, col, value))

    def board_filled(self):
        return self.board.filled()

    # TODO: outros metodos da classe


class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""

        initial_state = TakuzuState(board)
        super().__init__(initial_state)

    def actions(self, state: TakuzuState) -> List[Tuple[int, int, int]]:
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""

        actions = []

        if state.board_filled():
            return actions

        for row in range(board.size):
            for col in range(board.size):
                if board.get_number(row, col) == 2:
                    for value in board.possible_values_for_square(row, col):
                        actions.append((row, col, value))

        return actions

    def result(self, state: TakuzuState, action: Tuple[int, int, int]):
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""

        (row, col, val) = action
        return state.place(row, col, val)

    def goal_test(self, state: TakuzuState):
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""

        board = state.board

        if not state.board_filled():
            return False

        # NOTA: Não se verifica a restrição de números adjacentes pois esta é
        # verificada noutro sítio.

        maxAllowedDiff = board.size % 2
        # Verificar se existe o mesmo número de 0s e 1s em todas as linhas e colunas
        for n in range(board.size):
            if (
                abs(board.count_0s_row(n) - board.count_1s_row(n)) > maxAllowedDiff
                or abs(board.count_0s_col(n) - board.count_1s_col(n)) > maxAllowedDiff
            ):
                return False

        # Verificar se todas as linhas e colunas são diferentes
        return not (board.has_repeated_rows() or board.has_repeated_cols())

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
    board = Board.parse_instance_from_stdin()
    problem = Takuzu(board)
    print(problem.actions(problem.initial))
    # TODO:
