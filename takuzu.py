# Grupo 40:
# 99311 Rafael Serra e Oliveira
# 99335 Tiago Vieira da Silva

from sys import stdin
from typing import Dict, List, Set, Tuple, Union
from search import (
    Problem,
    Node,
    astar_search,
    breadth_first_tree_search,
    depth_first_tree_search,
    greedy_search,
    recursive_best_first_search,
)
import numpy as np


class Board:
    """Representação interna de um tabuleiro de Takuzu."""

    matrix: Tuple[Tuple[int, ...], ...]
    domains: Tuple[Tuple[Tuple[int, ...], ...], ...]
    size: int
    free_squares: int

    def __init__(
        self,
        matrix: Tuple[Tuple[int, ...], ...],
        domains: Tuple[Tuple[Tuple[int, ...], ...], ...],
        size: int,
        free_squares: int,
    ):
        """Construtor.
        Recebe uma matriz de inteiros representando o tabuleiro.
        """

        self.matrix = matrix
        self.domains = domains
        self.size = size
        self.free_squares = free_squares

    def __str__(self) -> str:
        """Representação externa do tabuleiro."""

        return "\n".join(["\t".join(str(x) for x in row) for row in self.matrix])

    def __repr__(self) -> str:
        """Representação interna do tabuleiro."""

        return f"Board({self.matrix}, {self.domains}, {self.size}, {self.free_squares})"

    def print_pretty_repr(self) -> None:
        """Devolve uma representação do tabuleiro em formato legível."""

        for i in range(self.size):
            for j in range(self.size):
                print(
                    f"[{self.get_number(i, j)}, {str(self.get_domain(i, j)).ljust(len('(0, 1)'))}]",
                    end="\t",
                )
            print()

    def get_number(self, row: int, col: int) -> Union[int, None]:
        """Devolve o valor na respetiva posição do tabuleiro, ou None se a posição for inválida."""

        if 0 <= row < self.size and 0 <= col < self.size:
            return self.matrix[row][col]
        else:
            return None

    def get_domain(self, row: int, col: int) -> Tuple[int, ...]:
        """Devolve o domínio da posição indicada."""

        if 0 <= row < self.size and 0 <= col < self.size:
            return self.domains[row][col]
        else:
            return ()

    def get_column(self, col: int) -> Tuple[int, ...]:
        """Devolve a coluna indicada."""

        return tuple(row[col] for row in self.matrix)

    def get_row(self, row: int) -> Tuple[int, ...]:
        """Devolve a linha indicada."""

        return self.matrix[row]

    def count_col(self, col: int, num: int) -> int:
        """Devolve o número de num na coluna indicada."""

        return self.get_column(col).count(num)

    def count_row(self, row: int, num: int) -> int:
        """Devolve o número de num na linha indicada."""

        return self.get_row(row).count(num)

    def place(self, row: int, col: int, value: int) -> "Board":
        """Devolve um novo tabuleiro com o valor colocado na posição indicada."""

        new_matrix = tuple(
            tuple(
                value if (i == row and j == col) else self.matrix[i][j]
                for j in range(self.size)
            )
            for i in range(self.size)
        )

        new_board = Board(new_matrix, self.domains, self.size, self.free_squares - 1)
        new_board.recalculate_domains_after_placing(row, col, value)

        return new_board

    def filled(self) -> bool:
        """Devolve True se o tabuleiro estiver completo."""

        return self.free_squares == 0

    def recalculate_domains_after_placing(self, row: int, col: int, value: int) -> None:
        """Recalcula os domínios após a introdução de um valor na posição (row, col)."""

        new_domains: Dict[Tuple[int, int], Set[int]] = {(row, col): {value}}

        # Não permitir três números adjacentes iguais
        for (closest, furthest) in (
            *(((row + delta, col), (row + 2 * delta, col)) for delta in (-1, 1)),
            *(((row - delta, col), (row + delta, col)) for delta in (-1, 1)),
            *(((row, col + delta), (row, col + 2 * delta)) for delta in (-1, 1)),
            *(((row, col - delta), (row, col + delta)) for delta in (-1, 1)),
        ):
            closest_val = self.get_number(*closest)
            furthest_val = self.get_number(*furthest)
            if closest_val == 2 and furthest_val == value:
                new_domains.setdefault(closest, set((0, 1))).difference_update((value,))
            elif closest_val == value and furthest_val == 2:
                new_domains.setdefault(furthest, set((0, 1))).difference_update(
                    (value,)
                )

        # Não permitir linhas nem colunas iguais
        for (key, getter, counter, packer) in (
            (row, self.get_row, self.count_row, lambda x, y: (x, y)),
            (col, self.get_column, self.count_col, lambda x, y: (y, x)),
        ):
            this = getter(key)
            empty_count = counter(key, 2)
            if empty_count == 0:
                for i in range(self.size):
                    if i != key and counter(i, 2) == 1:
                        other = getter(i)
                        empty_j = other.index(2)
                        for possible_value in self.get_domain(*(packer(i, empty_j))):
                            if (
                                tuple(
                                    possible_value if j == empty_j else other[j]
                                    for j in range(self.size)
                                )
                                == this
                            ):
                                new_domains.setdefault(
                                    packer(i, empty_j), set((0, 1))
                                ).difference_update((possible_value,))
            elif empty_count == 1:
                empty_j = this.index(2)
                empty_j_domain = self.get_domain(*(packer(key, empty_j)))
                for i in range(self.size):
                    if i != key and counter(i, 2) == 0:
                        for possible_value in empty_j_domain:
                            if tuple(
                                possible_value if j == empty_j else this[j]
                                for j in range(self.size)
                            ) == getter(i):
                                new_domains.setdefault(
                                    packer(key, empty_j), set((0, 1))
                                ).difference_update((possible_value,))

        # Número de valores por linha e coluna deve ser ~igual
        max_diff = self.size % 2
        for (this, packer) in (
            (self.get_row(row), lambda other_coord: (row, other_coord)),
            (self.get_column(col), lambda other_coord: (other_coord, col)),
        ):
            constraint_domain = set((0, 1))
            for value in (0, 1):
                if this.count(value) >= np.floor(self.size // 2) + max_diff:
                    constraint_domain.difference_update((value,))
            for i in range(self.size):
                if this[i] == 2:
                    new_domains.setdefault(packer(i), set((0, 1))).intersection_update(
                        constraint_domain
                    )

        # Guardar a interseção dos domínios novos com os atuais
        self.domains = tuple(
            tuple(
                tuple(
                    new_domains.setdefault((i, j), set((0, 1))).intersection(
                        self.get_domain(i, j)
                    )
                )
                if (i, j) in new_domains
                else self.get_domain(i, j)
                for j in range(self.size)
            )
            for i in range(self.size)
        )

    @staticmethod
    def parse_instance_from_stdin() -> "Board":
        """Lê o test do standard input (stdin) que é passado como argumento
        e retorna uma instância da classe Board.

        Por exemplo:
            $ python3 takuzu.py < input_T01

            > from sys import stdin
            > stdin.readline()
        """

        size = int(stdin.readline())
        free_squares = size * size
        matrix: List[Tuple[int, ...]] = []
        domains: List[Tuple[Tuple[int, ...]]] = []
        needs_revision: List[Tuple[int, int, int]] = []
        for _ in range(size):
            row: List[int] = []
            row_domains: List[Tuple[int, ...]] = []
            for entry in stdin.readline().split("\t"):
                row.append(int(entry))
                if int(entry) == 2:
                    row_domains.append((0, 1))
                else:
                    row_domains.append((int(entry),))
                    needs_revision.append((len(matrix), len(row) - 1, int(entry)))
                    free_squares -= 1
            matrix.append(tuple(row))
            domains.append(tuple(row_domains))

        board = Board(tuple(matrix), tuple(domains), size, free_squares)
        for action in needs_revision:
            board.recalculate_domains_after_placing(*action)

        return board


class TakuzuState:
    state_id = 0
    board: Board

    def __init__(self, board):
        """Inicializa o estado com o tabuleiro indicado."""

        self.board = board
        self.id = TakuzuState.state_id
        TakuzuState.state_id += 1

    def __lt__(self, other):
        """Devolve True se o estado for anterior a outro."""

        return self.id < other.id

    def __str__(self):
        """Representação externa do estado."""

        return str(self.board)

    def __repr__(self):
        """Representação interna do estado."""

        return f"TakuzuState({repr(self.board)})"

    def place(self, row: int, col: int, value: int) -> "TakuzuState":
        """Devolve um novo estado com o valor colocado na posição indicada."""

        return TakuzuState(self.board.place(row, col, value))

    def board_filled(self):
        """Devolve True se o tabuleiro estiver completo."""

        return self.board.filled()

    def recalculate_domains_after_placing(self, row: int, col: int, val: int) -> None:
        """Recalcula os domínios após a introdução de um valor na posição (row, col)."""

        self.board.recalculate_domains_after_placing(row, col, val)

    def get_domain(self, row: int, col: int) -> Tuple[int, ...]:
        """Devolve uma lista com os valores possíveis para a posição indicada."""

        return self.board.get_domain(row, col)

    def get_square_number(self, row: int, col: int) -> Union[int, None]:
        """Devolve o número da posição indicada."""

        return self.board.get_number(row, col)


class Takuzu(Problem):
    def __init__(self, board: Board):
        """O construtor especifica o estado inicial."""

        initial_state = TakuzuState(board)
        super().__init__(initial_state)

    def actions(self, state: TakuzuState) -> Tuple[Tuple[int, int, int]]:
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""

        if state.board_filled():
            return tuple()

        possible_actions: List[Tuple[Tuple[int, int, int]]] = []

        for row in range(board.size):
            for col in range(board.size):
                # Só considerar as ações para a primeira casa vazia
                if state.get_square_number(row, col) == 2:
                    possible_actions.append(
                        tuple(
                            tuple(
                                (row, col, value)
                                for value in state.get_domain(row, col)
                            ),
                        )
                    )

        # Otimização: ordenar por tamanho de domínio mais pequeno
        sorted_actions = sorted(possible_actions, key=lambda x: len(x))

        if len(sorted_actions) > 0:
            return sorted_actions[0]
        else:
            return tuple()

    def result(self, state: TakuzuState, action: Tuple[int, int, int]) -> TakuzuState:
        """Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de
        self.actions(state)."""

        (row, col, val) = action
        return state.place(row, col, val)

    def goal_test(self, state: TakuzuState) -> bool:
        """Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro
        estão preenchidas com uma sequência de números adjacentes."""

        return state.board_filled()

    def h(self, node: Node):
        """Função heuristica utilizada para a procura A*."""

        # TODO
        pass


if __name__ == "__main__":
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.

    # Ler tabuleiro do ficheiro 'i1.txt'(Figura 1):
    # $ python3 takuzu < i1.txt
    board = Board.parse_instance_from_stdin()
    # Criar uma instância de Takuzu:
    problem = Takuzu(board)
    # Obter o nó solução usando a procura em profundidade:
    goal_node = depth_first_tree_search(problem)
    # Verificar se foi atingida a solução
    if goal_node:
        print(goal_node.state)
    else:
        print("No solution found")
