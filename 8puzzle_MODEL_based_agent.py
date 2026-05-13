import random


def search_state(matrix):

    for i in range(3):
        for j in range(3):

            if matrix[i][j] == 0:
                return (i, j)


def RULES(state):

    x, y = state

    moves = []

    if x > 0:
        moves.append('up')

    if x < 2:
        moves.append('down')

    if y > 0:
        moves.append('left')

    if y < 2:
        moves.append('right')

    return moves

def UPDATE_STATE(state, action, matrix, model):

    x, y = state

    if action == 'up':

        matrix[x][y], matrix[x-1][y] = \
        matrix[x-1][y], matrix[x][y]

        state = (x-1, y)

    elif action == 'down':

        matrix[x][y], matrix[x+1][y] = \
        matrix[x+1][y], matrix[x][y]

        state = (x+1, y)

    elif action == 'left':

        matrix[x][y], matrix[x][y-1] = \
        matrix[x][y-1], matrix[x][y]

        state = (x, y-1)

    elif action == 'right':

        matrix[x][y], matrix[x][y+1] = \
        matrix[x][y+1], matrix[x][y]

        state = (x, y+1)

    model.append(str(matrix))

    return state


def action(state):

    moves = RULES(state)

    return random.choice(moves)


def solve_puzzle(matrix, model, target):

    state = search_state(matrix)

    step = 0

    while matrix != target:

        action_ = action(state)

        old = str(matrix)

        state = UPDATE_STATE(
            state,
            action_,
            matrix,
            model
        )

        
        if model.count(str(matrix)) > 1:

            matrix[:] = eval(old)

            state = search_state(matrix)

            continue

        step += 1

        print(f"\nBước {step}: {action_}")

        for row in matrix:
            print(row)

        if step > 50:
            print("Dừng")
            break

    if matrix == target:
        print("\nĐã giải xong")

def main():

    matrix = [
        [1,2,3],
        [5,6,0],
        [7,8,4]
    ]

    target = [
        [1,2,3],
        [4,5,6],
        [7,8,0]
    ]

    model = []

    model.append(str(matrix))

    solve_puzzle(matrix, model, target)

main()