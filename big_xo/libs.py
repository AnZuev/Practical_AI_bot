import numpy as np
import itertools

# 0 - empty cell
# 1 - 'x'
# -1 - 'o'
PLAYER_TYPE = dict({
    'x': 1,
    'o': -1
})


PATTERNS_TO_INDEX_MAPPING = dict()

PATTERNS = np.array([
    '0xxxxx',
    'xxxxx0',
    'x00000',
    '0x0000',
    '00x000',
    '000x00',
    '0000x0',
    '00000x',
    'xxxx00',
    '0xxxx0',
    '00xxxx',
    'xxx000',
    '0xxx00',
    '00xxx0',
    '000xxx',
    'xx0000',
    '0xx000',
    '00xx00',
    '000xx0',
    '0000xx'
])

SCORES = dict({
    'five': 500000,
    'open_four': 5000,
    'semiopen_four': 3000,
    'open_three': 2000,
    'semiopen_three': 1000,
    'open_two': 550,
    'semiopen_two': 300,
    'middle_one': 200,
    'semiopen_one': 100,
    'none': 0
})

WINDOW_SIZE = 6


def init_vectors():
    result = []
    for i, pattern in enumerate(PATTERNS):
        result.append(np.array(list(map(lambda x: int(x), pattern.replace('x', str(1))))))
        PATTERNS_TO_INDEX_MAPPING[pattern] = i
    return np.array(result)


VECTORS = init_vectors()


def iof(pattern):
    return PATTERNS_TO_INDEX_MAPPING[pattern]


def extract_diagonals(matrix):
    diags = list()
    diags.append(np.diag(matrix))
    diags.append(np.diag(np.flipud(matrix)))
    return np.array(diags)


def evaluate_board(board):
    size = len(board) - WINDOW_SIZE + 1
    result = np.zeros(shape=(size, size), dtype=object)
    for i in range(size):
        for j in range(size):
            result[i, j] = evaluate_window(board[i: i + WINDOW_SIZE, j:j + WINDOW_SIZE])
    return result


# 0 - for rows
# 1 - for columns
# 2 - for diagonals
def patterns_extraction(characterize, x_window_info, o_window_info, type_of=0):
    for i, info in enumerate(characterize):
        # evaluating for x
        if (info[iof('xxxxx0')] == 5 * PLAYER_TYPE['x']) or (info[iof('0xxxxx')] == 5 * PLAYER_TYPE['x']):
            x_window_info[type_of].append((i, SCORES["five"]))
        elif info[iof('0xxxx0')] == 4 * PLAYER_TYPE['x']:
            if (info[iof('x00000')] == 0) and (info[iof('00000x')] == 0):
                x_window_info[type_of].append((i, SCORES['open_four']))
            elif (info[iof('x00000')] == 0) or (info[iof('00000x')] == 0):
                x_window_info[type_of].append((i, SCORES['semiopen_four']))
        elif (info[iof('xxxx00')] == 4 * PLAYER_TYPE['x']) and (info[iof('0000x0')] == 0):
            x_window_info[type_of].append((i, SCORES['semiopen_four']))
        elif (info[iof('00xxxx')] == 4 * PLAYER_TYPE['x']) and (info[iof('0x0000')] == 0):
            x_window_info[type_of].append((i, SCORES['semiopen_four']))
        elif (info[iof('0xxx00')] == 3 * PLAYER_TYPE['x']):
            if (info[iof('x00000')] == 0) and (info[iof('0000x0')] == 0):
                x_window_info[type_of].append((i, SCORES['open_three']))
            elif (info[iof('x00000')] == 0) or (info[iof('0000x0')] == 0):
                x_window_info[type_of].append((i, SCORES['semiopen_three']))
        elif (info[iof('00xxx0')] == 3 * PLAYER_TYPE['x']):
            if (info[iof('0x0000')] == 0) and (info[iof('00000x')] == 0):
                x_window_info[type_of].append((i, SCORES['open_three']))
            elif (info[iof('0x0000')] == 0) or (info[iof('00000x')] == 0):
                x_window_info[type_of].append((i, SCORES['semiopen_three']))
        elif (info[iof('xxx000')] == 3 * PLAYER_TYPE['x']) and (info[iof('000x00')] == 0):
            x_window_info[type_of].append((i, SCORES['semiopen_three']))
        elif (info[iof('000xxx')] == 3 * PLAYER_TYPE['x']) and (info[iof('00x000')] == 0):
            x_window_info[type_of].append((i, SCORES['semiopen_three']))
        elif (info[iof('xx0000')] == 2 * PLAYER_TYPE['x']) and (info[iof('00x000')] == 0):
            x_window_info[type_of].append((i, SCORES['semiopen_two']))
        elif (info[iof('0xx000')] == 2 * PLAYER_TYPE['x']):
            if (info[iof('x00000')] == 0) and (info[iof('000x00')] == 0):
                x_window_info[type_of].append((i, SCORES['open_two']))
            elif (info[iof('x00000')] == 0) or (info[iof('000x00')] == 0):
                x_window_info[type_of].append((i, SCORES['semiopen_two']))
        elif (info[iof('00xx00')] == 2 * PLAYER_TYPE['x']):
            if (info[iof('0x0000')] == 0) and (info[iof('0000x0')] == 0):
                x_window_info[type_of].append((i, SCORES['open_two']))
            elif (info[iof('0x0000')] == 0) or (info[iof('0000x0')] == 0):
                x_window_info[type_of].append((i, SCORES['semiopen_two']))
        elif (info[iof('000xx0')] == 2 * PLAYER_TYPE['x']):
            if (info[iof('00x000')] == 0) and (info[iof('00000x')] == 0):
                x_window_info[type_of].append((i, SCORES['open_two']))
            elif (info[iof('00x000')] == 0) or (info[iof('00000x')] == 0):
                x_window_info[type_of].append((i, SCORES['semiopen_two']))
        elif (info[iof('0000xx')] == 2 * PLAYER_TYPE['x']) and (info[iof('000x00')] == 0):
            x_window_info[type_of].append((i, SCORES['semiopen_two']))
        else:
            t_score = 0
            if (info[iof('0000x0')]):
                t_score += SCORES['semiopen_one']
            if (info[iof('0x0000')]):
                t_score += SCORES['semiopen_one']
            if (info[iof('000x00')]):
                t_score += SCORES['middle_one']
            if (info[iof('00x000')]):
                t_score += SCORES['middle_one']
            x_window_info[type_of].append((i, t_score))

        # evaluating for o
        if (info[iof('xxxxx0')] == 5 * PLAYER_TYPE['o']) or (info[iof('0xxxxx')] == 5 * PLAYER_TYPE['o']):
            o_window_info[type_of].append((i, SCORES["five"]))
        elif info[iof('0xxxx0')] == 4 * PLAYER_TYPE['o']:
            if (info[iof('x00000')] == 0) and (info[iof('00000x')] == 0):
                o_window_info[type_of].append((i, SCORES['open_four']))
            elif (info[iof('x00000')] == 0) or (info[iof('00000x')] == 0):
                o_window_info[type_of].append((i, SCORES['semiopen_four']))
        elif (info[iof('xxxx00')] == 4 * PLAYER_TYPE['o']) and (info[iof('0000x0')] == 0):
            o_window_info[type_of].append((i, SCORES['semiopen_four']))
        elif (info[iof('00xxxx')] == 4 * PLAYER_TYPE['o']) and (info[iof('0x0000')] == 0):
            o_window_info[type_of].append((i, SCORES['semiopen_four']))
        elif (info[iof('0xxx00')] == 3 * PLAYER_TYPE['o']):
            if (info[iof('x00000')] == 0) and (info[iof('0000x0')] == 0):
                o_window_info[type_of].append((i, SCORES['open_three']))
            elif (info[iof('x00000')] == 0) or (info[iof('0000x0')] == 0):
                o_window_info[type_of].append((i, SCORES['semiopen_three']))
        elif (info[iof('00xxx0')] == 3 * PLAYER_TYPE['o']):
            if (info[iof('0x0000')] == 0) and (info[iof('00000x')] == 0):
                o_window_info[type_of].append((i, SCORES['open_three']))
            elif (info[iof('0x0000')] == 0) or (info[iof('00000x')] == 0):
                o_window_info[type_of].append((i, SCORES['semiopen_three']))
        elif (info[iof('xxx000')] == 3 * PLAYER_TYPE['o']) and (info[iof('000x00')] == 0):
            o_window_info[type_of].append((i, SCORES['semiopen_three']))
        elif (info[iof('000xxx')] == 3 * PLAYER_TYPE['o']) and (info[iof('00x000')] == 0):
            o_window_info[type_of].append((i, SCORES['semiopen_three']))
        elif (info[iof('xx0000')] == 2 * PLAYER_TYPE['o']) and (info[iof('00x000')] == 0):
            o_window_info[type_of].append((i, SCORES['semiopen_two']))
        elif (info[iof('0xx000')] == 2 * PLAYER_TYPE['o']):
            if (info[iof('x00000')] == 0) and (info[iof('000x00')] == 0):
                o_window_info[type_of].append((i, SCORES['open_two']))
            elif (info[iof('x00000')] == 0) or (info[iof('000x00')] == 0):
                o_window_info[type_of].append((i, SCORES['semiopen_two']))
        elif (info[iof('00xx00')] == 2 * PLAYER_TYPE['o']):
            if (info[iof('0x0000')] == 0) and (info[iof('0000x0')] == 0):
                o_window_info[type_of].append((i, SCORES['open_two']))
            elif (info[iof('0x0000')] == 0) or (info[iof('0000x0')] == 0):
                o_window_info[type_of].append((i, SCORES['semiopen_two']))
        elif (info[iof('000xx0')] == 2 * PLAYER_TYPE['o']):
            if (info[iof('00x000')] == 0) and (info[iof('00000x')] == 0):
                o_window_info[type_of].append((i, SCORES['open_two']))
            elif (info[iof('00x000')] == 0) or (info[iof('00000x')] == 0):
                o_window_info[type_of].append((i, SCORES['semiopen_two']))
        elif (info[iof('0000xx')] == 2 * PLAYER_TYPE['o']) and (info[iof('000x00')] == 0):
            o_window_info[type_of].append((i, SCORES['semiopen_two']))
        else:
            t_score = 0
            if (info[iof('0000x0')]):
                t_score += SCORES['semiopen_one']
            if (info[iof('0x0000')]):
                t_score += SCORES['semiopen_one']
            if (info[iof('000x00')]):
                t_score += SCORES['middle_one']
            if (info[iof('00x000')]):
                t_score += SCORES['middle_one']
            o_window_info[type_of].append((i, t_score))
    return (x_window_info, o_window_info)


# player_type - for what player we do evaluation
# 1 - 'x'
# -1 - 'o'
def evaluate_window(window):
    x_window_info = ([], [], [])
    o_window_info = ([], [], [])

    characterize = np.dot(window, VECTORS.T)
    # print(characterize)
    x_window_info, o_window_info = patterns_extraction(characterize, x_window_info, o_window_info, 0)

    characterize = np.dot(VECTORS, window).T
    # print(characterize)
    x_window_info, o_window_info = patterns_extraction(characterize, x_window_info, o_window_info, 1)

    diagonals = extract_diagonals(window)
    characterize = np.dot(diagonals, VECTORS.T)
    # print(characterize)
    x_window_info, o_window_info = patterns_extraction(characterize, x_window_info, o_window_info, 2)

    return x_window_info, o_window_info


def get_max_element_index_from_2d_matrix(matrix):
    max_element = matrix[0][0]
    result = (0, 0)
    for i, row in enumerate(matrix):
        for j, element in enumerate(row):
            if element > max_element:
                result = (i, j)
                max_element = element
    return result


def get_total_scores(my_scores, opponent_scores):
    my_total_score = np.sum(my_scores)
    opponent_total_score = np.sum(opponent_scores)
    difference = my_total_score - opponent_total_score
    return my_total_score, opponent_total_score, difference


def score_game(board, player_type):
    evaluation_result = evaluate_board(board)
    size = len(board) - WINDOW_SIZE + 1
    my_scores = np.zeros(shape=(size, size), dtype=object)
    opponent_scores = np.zeros(shape=(size, size), dtype=object)
    for i in range(size):
        for j in range(size):
            my_scores[i, j] = score_window(evaluation_result[i, j], player_type)
            opponent_scores[i, j] = score_window(evaluation_result[i, j], -1 * player_type)
    return (my_scores, opponent_scores)


def find_best_move_within_window(window, player_type):
    t_window = np.copy(window)
    best_move = (-1, -1)
    best_score = -1
    for i in range(WINDOW_SIZE):
        for j in range(WINDOW_SIZE):
            if t_window[i, j] == 0:
                t_window[i, j] = player_type
                n_score = score_window(evaluate_window(t_window), player_type)
                if n_score > best_score:
                    best_move = (i, j)
                    best_score = n_score
                t_window[i, j] = 0
    return best_move, best_score


def score_window(window, player_type):
    return sum(map(lambda x: x[1], itertools.chain(*window[map_player(player_type)])))


def map_player(player_type):
    if player_type == 1:
        return 0
    return 1
