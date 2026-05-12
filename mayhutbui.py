import random

def P_moves(pos, matrix):
    moves = []
    x, y = pos

    if x < 3:
        moves.append((x + 1, y))
    if x > 0:
        moves.append((x - 1, y))
    if y < 3:
        moves.append((x, y + 1))
    if y > 0:
        moves.append((x, y - 1))

    return moves


def Rule(pos, matrix):

    x, y = pos

    if matrix[x][y] == 1:
        matrix[x][y] = 0

    moves = P_moves(pos, matrix)
    action=random.choice(moves)

    return random


def solve(pos, matrix, step=0):

    
    if step > 10000:
        return pos

    stop = False

    for i in range(4):
        for j in range(4):
            if matrix[i][j] == 1:
                stop = True
                break

        if stop:
            break

    if stop:
        new_pos = Rule(pos, matrix)

        return solve(new_pos, matrix, step + 1)

    else:
        return pos


def main():
# ma trận với 0 là sạch còn 1 là bẩn 
    matrix = [[random.randint(0, 1) for _ in range(4)] for _ in range(4)]

    print("Ban đầu:")
    for row in matrix:
        print(row)

    pos = (0, 0)

    pos = solve(pos, matrix)

    print("\nSau khi hút:")
    for row in matrix:
        print(row)

    print("Vị trí cuối:", pos)


main()