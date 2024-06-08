import numpy as np
from game import Actions

regular_table_strat = {
    (0, 0): Actions.HT, (0, 1): Actions.HT, (0, 2): Actions.HT, (0, 3): Actions.HT, (0, 4): Actions.HT, (0, 5): Actions.HT, (0, 6): Actions.HT, (0, 7): Actions.HT, (0, 8): Actions.HT, (0, 9): Actions.HT, #5
    (1, 0): Actions.HT, (1, 1): Actions.HT, (1, 2): Actions.HT, (1, 3): Actions.HT, (1, 4): Actions.HT, (1, 5): Actions.HT, (1, 6): Actions.HT, (1, 7): Actions.HT, (1, 8): Actions.HT, (1, 9): Actions.HT, #6
    (2, 0): Actions.HT, (2, 1): Actions.HT, (2, 2): Actions.HT, (2, 3): Actions.HT, (2, 4): Actions.HT, (2, 5): Actions.HT, (2, 6): Actions.HT, (2, 7): Actions.HT, (2, 8): Actions.HT, (2, 9): Actions.HT, #7
    (3, 0): Actions.HT, (3, 1): Actions.HT, (3, 2): Actions.HT, (3, 3): Actions.HT, (3, 4): Actions.HT, (3, 5): Actions.HT, (3, 6): Actions.HT, (3, 7): Actions.HT, (3, 8): Actions.HT, (3, 9): Actions.HT, #8
    (4, 0): Actions.HT, (4, 1): Actions.DH, (4, 2): Actions.DH, (4, 3): Actions.DH, (4, 4): Actions.DH, (4, 5): Actions.HT, (4, 6): Actions.HT, (4, 7): Actions.HT, (4, 8): Actions.HT, (4, 9): Actions.HT, #9
    (5, 0): Actions.DH, (5, 1): Actions.DH, (5, 2): Actions.DH, (5, 3): Actions.DH, (5, 4): Actions.DH, (5, 5): Actions.DH, (5, 6): Actions.DH, (5, 7): Actions.DH, (5, 8): Actions.HT, (5, 9): Actions.HT, #10
    (6, 0): Actions.DH, (6, 1): Actions.DH, (6, 2): Actions.DH, (6, 3): Actions.DH, (6, 4): Actions.DH, (6, 5): Actions.DH, (6, 6): Actions.DH, (6, 7): Actions.DH, (6, 8): Actions.DH, (6, 9): Actions.DH, #11 
    (7, 0): Actions.HT, (7, 1): Actions.HT, (7, 2): Actions.ST, (7, 3): Actions.ST, (7, 4): Actions.ST, (7, 5): Actions.HT, (7, 6): Actions.HT, (7, 7): Actions.HT, (7, 8): Actions.HT, (7, 9): Actions.HT, #12
    (8, 0): Actions.ST, (8, 1): Actions.ST, (8, 2): Actions.ST, (8, 3): Actions.ST, (8, 4): Actions.ST, (8, 5): Actions.HT, (8, 6): Actions.HT, (8, 7): Actions.HT, (8, 8): Actions.HT, (8, 9): Actions.HT, #13
    (9, 0): Actions.ST, (9, 1): Actions.ST, (9, 2): Actions.ST, (9, 3): Actions.ST, (9, 4): Actions.ST, (9, 5): Actions.HT, (9, 6): Actions.HT, (9, 7): Actions.HT, (9, 8): Actions.HT, (9, 9): Actions.HT, #14
    (10, 0): Actions.ST, (10, 1): Actions.ST, (10, 2): Actions.ST, (10, 3): Actions.ST, (10, 4): Actions.ST, (10, 5): Actions.HT, (10, 6): Actions.HT, (10, 7): Actions.HT, (10, 8): Actions.HT, (10, 9): Actions.HT, #15
    (11, 0): Actions.ST, (11, 1): Actions.ST, (11, 2): Actions.ST, (11, 3): Actions.ST, (11, 4): Actions.ST, (11, 5): Actions.HT, (11, 6): Actions.HT, (11, 7): Actions.HT, (11, 8): Actions.HT, (11, 9): Actions.HT, #16
    (12, 0): Actions.ST, (12, 1): Actions.ST, (12, 2): Actions.ST, (12, 3): Actions.ST, (12, 4): Actions.ST, (12, 5): Actions.ST, (12, 6): Actions.ST, (12, 7): Actions.ST, (12, 8): Actions.ST, (12, 9): Actions.ST, #17
    (13, 0): Actions.ST, (13, 1): Actions.ST, (13, 2): Actions.ST, (13, 3): Actions.ST, (13, 4): Actions.ST, (13, 5): Actions.ST, (13, 6): Actions.ST, (13, 7): Actions.ST, (13, 8): Actions.ST, (13, 9): Actions.ST, #18
    (14, 0): Actions.ST, (14, 1): Actions.ST, (14, 2): Actions.ST, (14, 3): Actions.ST, (14, 4): Actions.ST, (14, 5): Actions.ST, (14, 6): Actions.ST, (14, 7): Actions.ST, (14, 8): Actions.ST, (14, 9): Actions.ST, #19
    (15, 0): Actions.ST, (15, 1): Actions.ST, (15, 2): Actions.ST, (15, 3): Actions.ST, (15, 4): Actions.ST, (15, 5): Actions.ST, (15, 6): Actions.ST, (15, 7): Actions.ST, (15, 8): Actions.ST, (15, 9): Actions.ST, #20
}

ace_table_strat = {
    (0, 0): Actions.HT, (0, 1): Actions.HT, (0, 2): Actions.HT, (0, 3): Actions.DH, (0, 4): Actions.DH, (0, 5): Actions.HT, (0, 6): Actions.HT, (0, 7): Actions.HT, (0, 8): Actions.HT, (0, 9): Actions.HT, #2
    (1, 0): Actions.HT, (1, 1): Actions.HT, (1, 2): Actions.HT, (1, 3): Actions.DH, (1, 4): Actions.DH, (1, 5): Actions.HT, (1, 6): Actions.HT, (1, 7): Actions.HT, (1, 8): Actions.HT, (1, 9): Actions.HT, #3
    (2, 0): Actions.HT, (2, 1): Actions.HT, (2, 2): Actions.DH, (2, 3): Actions.DH, (2, 4): Actions.DH, (2, 5): Actions.HT, (2, 6): Actions.HT, (2, 7): Actions.HT, (2, 8): Actions.HT, (2, 9): Actions.HT, #4
    (3, 0): Actions.HT, (3, 1): Actions.HT, (3, 2): Actions.DH, (3, 3): Actions.DH, (3, 4): Actions.DH, (3, 5): Actions.HT, (3, 6): Actions.HT, (3, 7): Actions.HT, (3, 8): Actions.HT, (3, 9): Actions.HT, #5
    (4, 0): Actions.HT, (4, 1): Actions.DH, (4, 2): Actions.DH, (4, 3): Actions.DH, (4, 4): Actions.DH, (4, 5): Actions.HT, (4, 6): Actions.HT, (4, 7): Actions.HT, (4, 8): Actions.HT, (4, 9): Actions.HT, #6
    (5, 0): Actions.ST, (5, 1): Actions.DS, (5, 2): Actions.DS, (5, 3): Actions.DS, (5, 4): Actions.DS, (5, 5): Actions.ST, (5, 6): Actions.ST, (5, 7): Actions.HT, (5, 8): Actions.HT, (5, 9): Actions.HT, #7
    (6, 0): Actions.ST, (6, 1): Actions.ST, (6, 2): Actions.ST, (6, 3): Actions.ST, (6, 4): Actions.ST, (6, 5): Actions.ST, (6, 6): Actions.ST, (6, 7): Actions.ST, (6, 8): Actions.ST, (6, 9): Actions.ST, #8 
    (7, 0): Actions.ST, (7, 1): Actions.ST, (7, 2): Actions.ST, (7, 3): Actions.ST, (7, 4): Actions.ST, (7, 5): Actions.ST, (7, 6): Actions.ST, (7, 7): Actions.ST, (7, 8): Actions.ST, (7, 9): Actions.ST, #9
}

pair_table_strat = {
    (0, 0): Actions.SP, (0, 1): Actions.SP, (0, 2): Actions.SP, (0, 3): Actions.SP, (0, 4): Actions.SP, (0, 5): Actions.SP, (0, 6): Actions.SP, (0, 7): Actions.SP, (0, 8): Actions.SP, (0, 9): Actions.SP,  # A
    (1, 0): Actions.SP, (1, 1): Actions.SP, (1, 2): Actions.SP, (1, 3): Actions.SP, (1, 4): Actions.SP, (1, 5): Actions.SP, (1, 6): Actions.HT, (1, 7): Actions.HT, (1, 8): Actions.HT, (1, 9): Actions.HT,  # 2
    (2, 0): Actions.SP, (2, 1): Actions.SP, (2, 2): Actions.SP, (2, 3): Actions.SP, (2, 4): Actions.SP, (2, 5): Actions.SP, (2, 6): Actions.HT, (2, 7): Actions.HT, (2, 8): Actions.HT, (2, 9): Actions.HT,  # 3
    (3, 0): Actions.HT, (3, 1): Actions.HT, (3, 2): Actions.HT, (3, 3): Actions.SP, (3, 4): Actions.SP, (3, 5): Actions.HT, (3, 6): Actions.HT, (3, 7): Actions.HT, (3, 8): Actions.HT, (3, 9): Actions.HT,  # 4
    (4, 0): Actions.DH, (4, 1): Actions.DH, (4, 2): Actions.DH, (4, 3): Actions.DH, (4, 4): Actions.DH, (4, 5): Actions.DH, (4, 6): Actions.DH, (4, 7): Actions.DH, (4, 8): Actions.HT, (4, 9): Actions.HT,  # 5
    (5, 0): Actions.SP, (5, 1): Actions.SP, (5, 2): Actions.SP, (5, 3): Actions.SP, (5, 4): Actions.SP, (5, 5): Actions.HT, (5, 6): Actions.HT, (5, 7): Actions.HT, (5, 8): Actions.HT, (5, 9): Actions.HT,  # 6
    (6, 0): Actions.SP, (6, 1): Actions.SP, (6, 2): Actions.SP, (6, 3): Actions.SP, (6, 4): Actions.SP, (6, 5): Actions.SP, (6, 6): Actions.HT, (6, 7): Actions.HT, (6, 8): Actions.HT, (6, 9): Actions.HT,  # 7
    (7, 0): Actions.SP, (7, 1): Actions.SP, (7, 2): Actions.SP, (7, 3): Actions.SP, (7, 4): Actions.SP, (7, 5): Actions.SP, (7, 6): Actions.SP, (7, 7): Actions.SP, (7, 8): Actions.SP, (7, 9): Actions.SP,  # 8
    (8, 0): Actions.SP, (8, 1): Actions.SP, (8, 2): Actions.SP, (8, 3): Actions.SP, (8, 4): Actions.SP, (8, 5): Actions.ST, (8, 6): Actions.SP, (8, 7): Actions.SP, (8, 8): Actions.ST, (8, 9): Actions.ST,  # 9
    (9, 0): Actions.ST, (9, 1): Actions.ST, (9, 2): Actions.ST, (9, 3): Actions.ST, (9, 4): Actions.ST, (9, 5): Actions.ST, (9, 6): Actions.ST, (9, 7): Actions.ST, (9, 8): Actions.ST, (9, 9): Actions.ST,  # 10
}


def move_last_column_to_front(table):
    return np.roll(table, 1, axis=1)

# Convert strategy dictionaries to numpy arrays
regular_table_known = move_last_column_to_front(np.array([[regular_table_strat.get((x, y), "") for y in range(10)] for x in range(16)]))
ace_table_known = move_last_column_to_front(np.array([[ace_table_strat.get((x, y), "") for y in range(10)] for x in range(8)]))
pair_table_known = move_last_column_to_front(np.array([[pair_table_strat.get((x, y), "") for y in range(10)] for x in range(10)]))

# Displaying the arrays
# print("Regular Table:\n", regular_table)
# print("\nAce Table:\n", ace_table)
# print("\nPair Table:\n", pair_table)
    

    