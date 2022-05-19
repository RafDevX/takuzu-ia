# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 00:
# 00000 Nome1
# 00000 Nome2

from copy import deepcopy
from sys import stdin
from typing import List, Tuple
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

    def place(self, row: int, col: int, value: int):
        return TakuzuState(self.board.place(row, col, value))

    # TODO: outros metodos da classe


class Board:
    """Representação interna de um tabuleiro de Takuzu."""
    matrix: List[List[int]]
    size: int

    def __init__(self, size: int, matrix: List[List[int]]):
        """Construtor.
        Recebe uma matriz de inteiros representando o tabuleiro.
        """
        self.size = size
        self.matrix = matrix


    def get_number(self, row: int, col: int) -> int | None:
        """Devolve o valor na respetiva posição do tabuleiro."""
        if (row < 0 or row >= self.size or col < 0 or col >= self.size):
            return None
        return self.matrix[row][col]

    def adjacent_vertical_numbers(self, row: int, col: int) -> Tuple[int | None, int | None]:
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""
        return (self.get_number(row - 1, col), self.get_number(row + 1, col))

    def adjacent_horizontal_numbers(self, row: int, col: int) -> Tuple[int | None, int | None]:
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""
        return (self.get_number(row, col - 1), self.get_number(row, col + 1))
    
    def place(self, row: int, col: int, value: int):
        """Devolve um novo tabuleiro com o valor colocado na posição indicada."""
        new_matrix = deepcopy(self.matrix)
        new_matrix[row][col] = value
        return Board(self.size, new_matrix)

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
        matrix = [
            [int(entry) for entry in stdin.readline().split('\t')]
            for _ in range(size)
        ]
        return Board(size, matrix)

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
    board = Board.parse_instance_from_stdin()
    # TODO:
