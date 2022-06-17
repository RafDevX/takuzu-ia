# takuzu.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 40:
# 99311 Rafael Serra e Oliveira
# 99335 Tiago Vieira da Silva

from sys import stdin
from typing import Callable, Dict, List, Set, Tuple, Union
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

        try:
            return self.matrix[row][col]
        except IndexError:
            return None

    def get_domain(self, row: int, col: int) -> Tuple[int, ...]:
        """Devolve o domínio da posição indicada."""

        try:
            return self.domains[row][col]
        except IndexError:
            return ()

    def adjacent_vertical_numbers(
        self, row: int, col: int
    ) -> Tuple[Union[int, None], Union[int, None]]:
        """Devolve os valores imediatamente abaixo e acima,
        respectivamente."""

        return (self.get_number(row - 1, col), self.get_number(row + 1, col))

    def adjacent_horizontal_numbers(
        self, row: int, col: int
    ) -> Tuple[Union[int, None], Union[int, None]]:
        """Devolve os valores imediatamente à esquerda e à direita,
        respectivamente."""

        return (self.get_number(row, col - 1), self.get_number(row, col + 1))

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

    def will_be_repeated(self, row: int, col: int, num: int) -> bool:
        """Devolve True se a matriz ficar com duas colunas iguais se se introduzir o num na posição (num, col)"""

        (temp_row, temp_col) = list(self.get_row(row)), list(self.get_column(col))
        temp_row[col] = num
        temp_col[row] = num
        return (tuple(temp_row) in self.matrix) or (tuple(temp_col) in self.matrix)

    def excess_of_num(self, row: int, col: int, num: int) -> bool:
        """Devolve True se a introdução do num na posição (row, col) impossibilitar que o número de 0s e 1s seja igual."""

        t = (num + 1) % 2
        return (
            (self.count_col(col, num) - self.count_col(col, t))
            >= self.count_col(col, 2)
        ) or (
            (self.count_row(row, num) - self.count_row(row, t))
            >= self.count_row(row, 2)
        )

    def possible_values_for_square(self, row: int, col: int) -> List[int]:
        """Devolve uma lista com os valores possíveis para a posição indicada."""

        possible_values = []

        if self.get_number(row, col) != 2:
            return possible_values

        for x in (0, 1):
            ok = True

            if self.will_be_repeated(row, col, x):
                continue

            if self.excess_of_num(row, col, x):
                continue

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

        print("I am looking at ", (row, col))
        self.print_pretty_repr()

        # Não permitir três números adjacentes iguais
        for (closest, furthest) in (
            *(((row + delta, col), (row + 2 * delta, col)) for delta in (-1, 1)),
            *(((row - delta, col), (row + delta, col)) for delta in (-1, 1)),
            *(((row, col + delta), (row, col + 2 * delta)) for delta in (-1, 1)),
            *(((row, col - delta), (row, col + delta)) for delta in (-1, 1)),
        ):
            print("Closest: ", closest, "Furthest: ", furthest)
            closest_val = self.get_number(*closest)
            furthest_val = self.get_number(*furthest)
            if closest_val == 2 and furthest_val == value:
                new_domains.setdefault(closest, set((0, 1))).difference_update((value,))
                print("(1) Did things for ", closest, "; took ", value)  # FIXME: remove
            elif closest_val == value and furthest_val == 2:
                new_domains.setdefault(furthest, set((0, 1))).difference_update(
                    (value,)
                )
                print(
                    "(2) Did things for ", furthest, "; took ", value
                )  # FIXME: remove

        # Não permitir linhas nem colunas iguais
        for (key, getter, counter, packer) in (
            (row, self.get_row, self.count_row, lambda x, y: (x, y)),
            (col, self.get_column, self.count_col, lambda x, y: (y, x)),
        ):
            this = getter(key)
            if counter(key, 2) == 0:
                for i in range(self.size):
                    other = getter(i)
                    if i != key and counter(i, 2) == 1:
                        empty_j = other.index(2)
                        for possible_value in self.get_domain(*(packer(i, empty_j))):
                            if (
                                tuple(
                                    possible_value if j == empty_j else other[j]
                                    for j in range(self.size)
                                )
                                == this
                            ):
                                print(
                                    "(3) Did things for ",
                                    packer(i, empty_j),
                                    "; took ",
                                    possible_value,
                                )  # FIXME: remove
                                new_domains.setdefault(
                                    packer(i, empty_j), set((0, 1))
                                ).difference_update((possible_value,))

        # Número de valores por linha e coluna deve ser ~igual
        max_diff = self.size % 2
        # FIXME: delete the ___key param, only used for debug prints
        for (___key, this, packer) in (
            ("row", self.get_row(row), lambda other_coord: (row, other_coord)),
            ("col", self.get_column(col), lambda other_coord: (other_coord, col)),
        ):
            constraint_domain = set((0, 1))
            for value in (0, 1):
                if this.count(value) >= self.size // 2 + max_diff:
                    constraint_domain.difference_update((value,))
                    print(
                        "(4) Did things for ",
                        ___key,
                        " ",
                        packer("*"),
                        "; took ",
                        value,
                    )  # FIXME: remove
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

        print("AFTER:")
        self.print_pretty_repr()

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
            print("Revisioning ", action)
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

    def actions(self, state: TakuzuState) -> List[Tuple[int, int, int]]:
        """Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento."""

        actions = []

        if state.board_filled():
            return actions

        # for row in range(board.size):
        #     for col in range(board.size):
        #         # Só considerar casas vazias
        #         if state.get_square_number(row, col) == 2:
        #             for value in state.get_domain(row, col):
        #                 actions.append((row, col, value))

        for row in range(board.size):
            for col in range(board.size):
                # Só considerar as ações para a primeira casa vazia
                if state.get_square_number(row, col) == 2:
                    # TODO: change to tuple
                    l = [(row, col, value) for value in state.get_domain(row, col)]
                    print("Actions:", l)
                    return l

        print("ACTIONS: ", actions)

        return actions

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

    # TODO: outros metodos da classe


if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro do standard input,
    # Usar uma técnica de procura para resolver a instância,
    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.

    # Ler tabuleiro do ficheiro 'i1.txt'(Figura 1):
    # $ python3 takuzu < i1.txt
    board = Board.parse_instance_from_stdin()
    # Criar uma instância de Takuzu:
    problem = Takuzu(board)

    # FIXME: remove below debug code
    # state = problem.initial
    # correct = ( # test 3
    #     (0, 1, 1, 0, 0, 1, 1, 0),
    #     (1, 0, 0, 1, 0, 0, 1, 1),
    #     (1, 0, 1, 0, 1, 0, 0, 1),
    #     (0, 1, 0, 1, 0, 1, 1, 0),
    #     (1, 0, 1, 0, 1, 1, 0, 0),
    #     (0, 1, 1, 0, 1, 0, 0, 1),
    #     (1, 0, 0, 1, 0, 1, 1, 0),
    #     (0, 1, 0, 1, 1, 0, 0, 1),
    # )
    # while stdin.readline():
    #     state = problem.result(state, problem.actions(state)[0])
    #     print("------------------- NEW ACTION -------------------")
    #     state.board.print_pretty_repr()
    #     for i in range(state.board.size):
    #         for j in range(state.board.size):
    #             guess = state.get_square_number(i, j)
    #             if guess != 2 and guess != correct[i][j]:
    #                 print("ERROR:", i, j, guess, correct[i][j])

    # exit(1)

    # Obter o nó solução usando a procura em profundidade:
    goal_node = depth_first_tree_search(problem)
    # Verificar se foi atingida a solução
    if goal_node:
        print(goal_node.state)
    else:
        print("No solution found")

    # TODO:
