import copy


class Node:
    def __init__(self, state, parent=None, action=None, depth=0):
        self.state = state  # trạng thái hiện tại của puzzle
        self.parent = parent  # node cha (node trước đó)
        self.action = action  # hành động từ node cha đến node này
        self.depth = depth  # độ sâu trong cây tìm kiếm

    def __eq__(self, other):
        """Kiểm tra xem hai node có cùng trạng thái không"""
        return self.state == other.state

    def __hash__(self):
        """Để có thể dùng trong set"""
        return hash(tuple(tuple(row) for row in self.state))

    def find_zero(self):
        """Tìm vị trí của số 0 trong puzzle"""
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    return (i, j)
        return None

    def get_neighbors(self):
        """Trả về danh sách các node hàng xóm """
        neighbors = []
        zero_pos = self.find_zero()
        i, j = zero_pos

        # Các hướng có thể di chuyển: lên, xuống, trái, phải
        directions = [(-1, 0, "UP"), (1, 0, "DOWN"), (0, -1, "LEFT"), (0, 1, "RIGHT")]

        for di, dj, action_name in directions:
            ni, nj = i + di, j + dj

            # Kiểm tra xem vị trí mới có hợp lệ không
            if 0 <= ni < 3 and 0 <= nj < 3:
                # Tạo trạng thái mới bằng cách hoán đổi
                new_state = copy.deepcopy(self.state)
                new_state[i][j], new_state[ni][nj] = new_state[ni][nj], new_state[i][j]

                # Tạo node mới
                new_node = Node(
                    new_state, parent=self, action=action_name, depth=self.depth + 1
                )
                neighbors.append(new_node)

        return neighbors


def DFS(start_state, target_state, max_depth=100):
    """Thuật toán DFS để giải 8 puzzle"""
    start_node = Node(start_state, parent=None, action=None, depth=0)

    # Kiểm tra xem start_node có phải là target không
    if start_node.state == target_state:
        return start_node, 0

    # Stack để lưu các node cần khám phá
    stack = [start_node]
    # Set để lưu các trạng thái đã khám phá (để tránh lặp)
    visited = {tuple(tuple(row) for row in start_state)}

    nodes_explored = 0

    while stack:
        current_node = stack.pop()
        nodes_explored += 1

        # Giới hạn độ sâu để tránh tìm kiếm vô hạn
        if current_node.depth >= max_depth:
            continue

        # Lấy các hàng xóm của node hiện tại
        for neighbor in current_node.get_neighbors():
            neighbor_state_tuple = tuple(tuple(row) for row in neighbor.state)

            # Nếu trạng thái hàng xóm chưa được khám phá
            if neighbor_state_tuple not in visited:
                visited.add(neighbor_state_tuple)

                # Kiểm tra xem đã tìm thấy target không
                if neighbor.state == target_state:
                    return neighbor, nodes_explored

                # Thêm vào stack để khám phá tiếp
                stack.append(neighbor)

    # Không tìm thấy đường đi
    return None, nodes_explored


def reconstruct_path(node):
    """Tái tạo đường đi từ start đến target"""
    path = []
    current = node

    while current is not None:
        path.append((current.state, current.action))
        current = current.parent

    # Đảo ngược vì ta xây dựng từ target về start
    path.reverse()
    return path


def print_state(state):
    for row in state:
        print(row)


def print_solution(path):
    print("\n" + "=" * 50)
    print("GIẢI PHÁP DFS CHO 8-PUZZLE")
    print("=" * 50)

    print("\nTRẠNG THÁI BAN ĐẦU:")
    if path:
        print_state(path[0][0])

    print("\n" + "-" * 50)
    print("ĐƯỜNG ĐI NGẮN NHẤT:")
    print("-" * 50)

    # In ra chuỗi hành động
    actions = [action for state, action in path if action is not None]
    if actions:
        print("\nCác hành động: " + " → ".join(actions))
    else:
        print("\nĐã ở trạng thái mục tiêu từ đầu!")

    print("\n" + "-" * 50)
    print("TRẠNG THÁI CUỐI CÙNG (MỤC TIÊU):")
    print("-" * 50)
    if path:
        print_state(path[-1][0])

    print(f"\nTổng số bước: {len(path) - 1}")


def main():
    start = [[2, 8, 3], [1, 6, 4], [7, 0, 5]]
    target = [[1, 2, 3], [8, 0, 4], [7, 6, 5]]

    print("TRẠNG THÁI BAN ĐẦU:")
    print_state(start)

    print("\n\nTRẠNG THÁI MỤC TIÊU:")
    print_state(target)

    print("\n\nDang thực hiện DFS...")

    # Thực hiện DFS
    solution_node, nodes_explored = DFS(start, target)

    if solution_node:
        # Tái tạo và in ra đường đi
        path = reconstruct_path(solution_node)
        print_solution(path)
        print(f"\nTổng số node đã khám phá: {nodes_explored}")
        print(f"Độ sâu giải pháp: {solution_node.depth}")
    else:
        print("Không tìm thấy giải pháp!")


if __name__ == "__main__":
    main()
