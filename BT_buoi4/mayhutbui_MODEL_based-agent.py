import random


# tìm các bước có thể đi
def RULES(pos):

    x, y = pos

    moves = []

    if x > 0:
        moves.append("up")

    if x < 3:
        moves.append("down")

    if y > 0:
        moves.append("left")

    if y < 3:
        moves.append("right")

    return moves


# thử di chuyển nhưng không sửa ma trận thật
def fake_move(pos, action):

    x, y = pos

    if action == "up":
        return (x-1, y)

    elif action == "down":
        return (x+1, y)

    elif action == "left":
        return (x, y-1)

    elif action == "right":
        return (x, y+1)


# chọn action chưa tạo trạng thái cũ
def choose_action(pos, matrix, model):

    moves = RULES(pos)

    valid_moves = []

    for move in moves:

        # vị trí mới
        next_pos = fake_move(pos, move)

        # copy ma trận
        temp = [row[:] for row in matrix]

        x, y = next_pos

        # giả sử robot qua ô đó và hút bụi
        if temp[x][y] == 1:
            temp[x][y] = 0

        # trạng thái mới
        next_state = str((next_pos, temp))

        # nếu trạng thái chưa từng gặp
        if next_state not in model:
            valid_moves.append(move)

    # còn đường mới
    if valid_moves:
        return random.choice(valid_moves)

    # bí thì đi đại
    return random.choice(moves)


# di chuyển thật
def UPDATE_STATE(pos, action):

    x, y = pos

    if action == "up":
        return (x-1, y)

    elif action == "down":
        return (x+1, y)

    elif action == "left":
        return (x, y-1)

    elif action == "right":
        return (x, y+1)


# kiểm tra sạch hết chưa
def done(matrix):

    for row in matrix:

        if 1 in row:
            return False

    return True


def solve(pos, matrix):

    model = []

    step = 0

    while not done(matrix):

        x, y = pos

        # hút bụi
        if matrix[x][y] == 1:
            matrix[x][y] = 0

        # lưu trạng thái hiện tại
        current_state = str((pos, matrix))

        model.append(current_state)

        print(f"\nBước {step}")
        print("Robot:", pos)

        for row in matrix:
            print(row)

        # chọn bước đi
        action = choose_action(pos, matrix, model)

        print("Action:", action)

        # cập nhật vị trí
        pos = UPDATE_STATE(pos, action)

        step += 1

        if step > 100:
            print("Dừng")
            break

    print("\nĐã hút xong")


def main():

    matrix = [
        [1,0,1,1],
        [0,1,0,1],
        [1,1,0,0],
        [1,0,1,1]
    ]

    print("Ban đầu:")

    for row in matrix:
        print(row)

    pos = (0,0)

    solve(pos, matrix)


main()