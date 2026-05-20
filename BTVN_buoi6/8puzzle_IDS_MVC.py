import copy
import tkinter as tk
from tkinter import messagebox, scrolledtext
import threading
import time


# ============================================
# MODEL
# ============================================
class PuzzleNode:
    """Nút trong cây tìm kiếm cho puzzle"""

    def __init__(self, state, parent=None, action=None, depth=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.depth = depth

    def __eq__(self, other):
        return self.state == other.state

    def __hash__(self):
        return hash(tuple(tuple(row) for row in self.state))

    def find_zero(self):
        """Tìm vị trí số 0 trong puzzle"""
        for i in range(3):
            for j in range(3):
                if self.state[i][j] == 0:
                    return (i, j)
        return None

    def get_neighbors(self):
        """Lấy các nút hàng xóm"""
        neighbors = []
        zero_pos = self.find_zero()
        i, j = zero_pos
        directions = [(-1, 0, "UP"), (1, 0, "DOWN"), (0, -1, "LEFT"), (0, 1, "RIGHT")]

        for di, dj, action_name in directions:
            ni, nj = i + di, j + dj
            if 0 <= ni < 3 and 0 <= nj < 3:
                new_state = copy.deepcopy(self.state)
                new_state[i][j], new_state[ni][nj] = new_state[ni][nj], new_state[i][j]
                new_node = PuzzleNode(
                    new_state, parent=self, action=action_name, depth=self.depth + 1
                )
                neighbors.append(new_node)
        return neighbors


class PuzzleModel:
    """Model quản lý logic của puzzle và thuật toán IDS"""

    def __init__(self, start_state, target_state):
        self.start_state = start_state
        self.target_state = target_state
        self.solution_path = []
        self.explored_nodes = []
        self.nodes_count = 0
        self.visited_states = set()

    def state_to_tuple(self, state):
        """Chuyển trạng thái thành tuple"""
        return tuple(tuple(row) for row in state)

    def _dfs_limited(self, node, depth_limit, visited):
        """DFS với giới hạn độ sâu"""
        if node.state == self.target_state:
            return node, True

        if node.depth >= depth_limit:
            return None, False

        stack = [node]
        local_visited = set()

        while stack:
            current_node = stack.pop()
            current_tuple = self.state_to_tuple(current_node.state)

            if current_tuple in local_visited:
                continue
            local_visited.add(current_tuple)

            self.nodes_count += 1
            self.explored_nodes.append(current_node)

            if current_node.depth >= depth_limit:
                continue

            for neighbor in current_node.get_neighbors():
                neighbor_tuple = self.state_to_tuple(neighbor.state)

                if neighbor_tuple not in local_visited:
                    if neighbor.state == self.target_state:
                        self.solution_path = self._reconstruct_path(neighbor)
                        return neighbor, True

                    stack.append(neighbor)

        return None, False

    def ids(self, max_depth=100):
        """Thuật toán IDS (Iterative Deepening Search)"""
        start_node = PuzzleNode(self.start_state, parent=None, action=None, depth=0)

        if start_node.state == self.target_state:
            self.solution_path = [start_node]
            return start_node, 1, True

        self.nodes_count = 0
        self.explored_nodes = []

        for depth_limit in range(0, max_depth + 1):
            self.explored_nodes = []
            visited = set()

            solution_node, found = self._dfs_limited(start_node, depth_limit, visited)

            if found:
                return solution_node, self.nodes_count, True

        return None, self.nodes_count, False

    def _reconstruct_path(self, node):
        """Tái tạo đường đi"""
        path = []
        current = node

        while current is not None:
            path.append(current)
            current = current.parent

        path.reverse()
        return path

    def get_solution_states(self):
        """Lấy danh sách trạng thái trong lời giải"""
        return [node.state for node in self.solution_path]

    def get_solution_actions(self):
        """Lấy danh sách hành động trong lời giải"""
        return [node.action for node in self.solution_path[1:]]


# ============================================
# VIEW
# ============================================
class PuzzleView:
    """View hiển thị giao diện GUI"""

    def __init__(self, root):
        self.root = root
        self.root.title("8 Puzzle Solver - IDS Algorithm (MVC)")
        self.root.geometry("950x750")
        self.root.configure(bg="#2c3e50")
        self.setup_ui()

    def setup_ui(self):
        """Thiết lập các thành phần UI"""
        # Tiêu đề
        title_frame = tk.Frame(self.root, bg="#34495e", height=60)
        title_frame.pack(fill=tk.X, padx=0, pady=0)
        title_label = tk.Label(
            title_frame,
            text="8 PUZZLE SOLVER - IDS (MVC Architecture)",
            font=("Arial", 16, "bold"),
            bg="#34495e",
            fg="white",
        )
        title_label.pack(pady=10)

        # Frame chính
        main_frame = tk.Frame(self.root, bg="#2c3e50")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Frame bên trái - Puzzle display
        left_frame = tk.Frame(main_frame, bg="#2c3e50")
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        state_label = tk.Label(
            left_frame,
            text="CURRENT STATE",
            font=("Arial", 12, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1",
        )
        state_label.pack(pady=10)

        self.canvas = tk.Canvas(
            left_frame,
            width=320,
            height=320,
            bg="#ecf0f1",
            highlightthickness=2,
            highlightbackground="#34495e",
        )
        self.canvas.pack(pady=10)

        # Frame bên phải - Controls
        right_frame = tk.Frame(main_frame, bg="#2c3e50", width=280)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        right_frame.pack_propagate(False)

        # Start state
        start_label = tk.Label(
            right_frame,
            text="START STATE",
            font=("Arial", 11, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1",
        )
        start_label.pack(pady=5)

        self.start_text = tk.Text(right_frame, height=4, width=20, font=("Courier", 9))
        self.start_text.pack(pady=5)
        self.start_text.insert(tk.END, "1 2 3\n5 6 0\n7 8 4")

        # Target state
        target_label = tk.Label(
            right_frame,
            text="TARGET STATE",
            font=("Arial", 11, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1",
        )
        target_label.pack(pady=5)

        self.target_text = tk.Text(right_frame, height=4, width=20, font=("Courier", 9))
        self.target_text.pack(pady=5)
        self.target_text.insert(tk.END, "1 2 3\n4 5 6\n7 8 0")

        # Separator
        separator = tk.Frame(right_frame, bg="#34495e", height=2)
        separator.pack(fill=tk.X, pady=10)

        # Buttons
        button_frame = tk.Frame(right_frame, bg="#2c3e50")
        button_frame.pack(pady=10)

        self.solve_btn = tk.Button(
            button_frame,
            text="SOLVE",
            font=("Arial", 10, "bold"),
            bg="#27ae60",
            fg="white",
            padx=20,
            pady=8,
        )
        self.solve_btn.pack(pady=5)

        self.reset_btn = tk.Button(
            button_frame,
            text="RESET",
            font=("Arial", 10, "bold"),
            bg="#e74c3c",
            fg="white",
            padx=20,
            pady=8,
        )
        self.reset_btn.pack(pady=5)

        # Navigation buttons
        nav_frame = tk.Frame(right_frame, bg="#2c3e50")
        nav_frame.pack(pady=10)

        self.prev_btn = tk.Button(
            nav_frame,
            text="◀ PREV",
            font=("Arial", 9, "bold"),
            bg="#3498db",
            fg="white",
            padx=10,
            pady=5,
        )
        self.prev_btn.pack(side=tk.LEFT, padx=3)

        self.next_btn = tk.Button(
            nav_frame,
            text="NEXT ▶",
            font=("Arial", 9, "bold"),
            bg="#3498db",
            fg="white",
            padx=10,
            pady=5,
        )
        self.next_btn.pack(side=tk.LEFT, padx=3)

        self.auto_btn = tk.Button(
            nav_frame,
            text="AUTO",
            font=("Arial", 9, "bold"),
            bg="#9b59b6",
            fg="white",
            padx=10,
            pady=5,
        )
        self.auto_btn.pack(side=tk.LEFT, padx=3)

        # Info frame
        info_label = tk.Label(
            right_frame,
            text="INFORMATION",
            font=("Arial", 11, "bold"),
            bg="#2c3e50",
            fg="#ecf0f1",
        )
        info_label.pack(pady=5)

        self.info_text = scrolledtext.ScrolledText(
            right_frame,
            height=8,
            width=30,
            font=("Courier", 8),
            bg="#34495e",
            fg="#ecf0f1",
        )
        self.info_text.pack(pady=5, fill=tk.BOTH, expand=True)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(
            self.root,
            textvariable=self.status_var,
            font=("Arial", 9),
            bg="#34495e",
            fg="#ecf0f1",
            relief=tk.SUNKEN,
            anchor=tk.W,
        )
        status_bar.pack(fill=tk.X, side=tk.BOTTOM, padx=0, pady=0)

    def draw_puzzle(self, state):
        """Vẽ puzzle lên canvas"""
        self.canvas.delete("all")

        cell_size = 95
        padding = 5
        start_x = 15
        start_y = 15

        for i in range(3):
            for j in range(3):
                x = start_x + j * (cell_size + padding)
                y = start_y + i * (cell_size + padding)

                number = state[i][j]

                # Vẽ ô
                if number == 0:
                    self.canvas.create_rectangle(
                        x,
                        y,
                        x + cell_size,
                        y + cell_size,
                        fill="#ecf0f1",
                        outline="#2c3e50",
                        width=2,
                    )
                else:
                    self.canvas.create_rectangle(
                        x,
                        y,
                        x + cell_size,
                        y + cell_size,
                        fill="#3498db",
                        outline="#2c3e50",
                        width=2,
                    )
                    self.canvas.create_text(
                        x + cell_size / 2,
                        y + cell_size / 2,
                        text=str(number),
                        font=("Arial", 28, "bold"),
                        fill="#ffffff",
                    )

    def display_info(self, info_text):
        """Hiển thị thông tin"""
        self.info_text.config(state=tk.NORMAL)
        self.info_text.delete("1.0", tk.END)
        self.info_text.insert(tk.END, info_text)
        self.info_text.config(state=tk.DISABLED)

    def update_status(self, message):
        """Cập nhật status bar"""
        self.status_var.set(message)

    def show_error(self, title, message):
        """Hiển thị lỗi"""
        messagebox.showerror(title, message)

    def show_warning(self, title, message):
        """Hiển thị cảnh báo"""
        messagebox.showwarning(title, message)

    def get_start_state_input(self):
        """Lấy input trạng thái ban đầu"""
        text = self.start_text.get("1.0", tk.END)
        try:
            lines = text.strip().split("\n")
            state = []
            for line in lines:
                row = list(map(int, line.split()))
                if len(row) != 3:
                    raise ValueError("Mỗi hàng phải có 3 phần tử")
                state.append(row)
            if len(state) != 3:
                raise ValueError("Phải có 3 hàng")
            return state
        except:
            self.show_error(
                "Lỗi",
                "Định dạng START STATE không hợp lệ!\nVí dụ:\n1 2 3\n4 5 6\n7 8 0",
            )
            return None

    def get_target_state_input(self):
        """Lấy input trạng thái mục tiêu"""
        text = self.target_text.get("1.0", tk.END)
        try:
            lines = text.strip().split("\n")
            state = []
            for line in lines:
                row = list(map(int, line.split()))
                if len(row) != 3:
                    raise ValueError("Mỗi hàng phải có 3 phần tử")
                state.append(row)
            if len(state) != 3:
                raise ValueError("Phải có 3 hàng")
            return state
        except:
            self.show_error(
                "Lỗi",
                "Định dạng TARGET STATE không hợp lệ!\nVí dụ:\n1 2 3\n4 5 6\n7 8 0",
            )
            return None

    def reset_canvas(self):
        """Reset canvas"""
        self.canvas.delete("all")

    def disable_solve_button(self):
        """Disable nút Solve"""
        self.solve_btn.config(state=tk.DISABLED)

    def enable_solve_button(self):
        """Enable nút Solve"""
        self.solve_btn.config(state=tk.NORMAL)

    def disable_auto_button(self):
        """Disable nút Auto"""
        self.auto_btn.config(state=tk.DISABLED)

    def enable_auto_button(self):
        """Enable nút Auto"""
        self.auto_btn.config(state=tk.NORMAL)


# ============================================
# CONTROLLER
# ============================================
class PuzzleController:
    """Controller điều phối Model và View"""

    def __init__(self, view):
        self.view = view
        self.model = None
        self.current_step = 0
        self.solution_states = []
        self.solution_actions = []
        self.is_solving = False
        self.is_animating = False

        self.setup_event_handlers()

    def setup_event_handlers(self):
        """Gắn các event handler cho View"""
        self.view.solve_btn.config(command=self.handle_solve)
        self.view.reset_btn.config(command=self.handle_reset)
        self.view.next_btn.config(command=self.handle_next)
        self.view.prev_btn.config(command=self.handle_prev)
        self.view.auto_btn.config(command=self.handle_auto)

    def handle_solve(self):
        """Xử lý sự kiện Solve"""
        if self.is_solving:
            self.view.show_warning("Cảnh báo", "Đang giải puzzle, vui lòng chờ!")
            return

        start_state = self.view.get_start_state_input()
        target_state = self.view.get_target_state_input()

        if start_state is None or target_state is None:
            return

        self.is_solving = True
        self.view.disable_solve_button()
        self.view.update_status("Solving...")

        # Chạy trong thread riêng
        thread = threading.Thread(
            target=self._solve_thread, args=(start_state, target_state)
        )
        thread.daemon = True
        thread.start()

    def _solve_thread(self, start_state, target_state):
        """Luồng giải puzzle"""
        try:
            self.model = PuzzleModel(start_state, target_state)
            solution_node, nodes_explored, success = self.model.ids(max_depth=100)

            if success:
                self.solution_states = self.model.get_solution_states()
                self.solution_actions = self.model.get_solution_actions()
                self.current_step = 0
                self.view.root.after(0, self._update_after_solve, nodes_explored)
            else:
                self.view.root.after(
                    0, lambda: self.view.show_error("Lỗi", "Không tìm thấy lời giải!")
                )
        except Exception as e:
            self.view.root.after(0, lambda: self.view.show_error("Lỗi", str(e)))
        finally:
            self.is_solving = False
            self.view.root.after(0, lambda: self.view.enable_solve_button())

    def _update_after_solve(self, nodes_explored):
        """Cập nhật UI sau khi giải xong"""
        info = f"✓ SOLUTION FOUND!\n"
        info += f"{'='*28}\n"
        info += f"Total Steps: {len(self.solution_actions)}\n"
        info += f"Nodes Explored: {nodes_explored}\n"
        info += f"Solution Depth: {len(self.solution_states)-1}\n"
        info += f"\nActions:\n"
        for i, action in enumerate(self.solution_actions, 1):
            info += f"{i}. {action}\n"

        self.view.display_info(info)
        self.view.draw_puzzle(self.solution_states[0])
        self.update_step_display()
        self.view.update_status(f"✓ Solved! Steps: {len(self.solution_actions)}")

    def update_step_display(self):
        """Cập nhật hiển thị bước hiện tại"""
        if self.solution_states:
            self.view.draw_puzzle(self.solution_states[self.current_step])
            if self.current_step < len(self.solution_actions):
                step_info = f"Step {self.current_step + 1}/{len(self.solution_actions)}: {self.solution_actions[self.current_step]}"
            else:
                step_info = "COMPLETED!"
            self.view.update_status(step_info)

    def handle_next(self):
        """Xử lý nút Next"""
        if not self.solution_states:
            self.view.show_warning("Cảnh báo", "Vui lòng giải puzzle trước!")
            return

        if self.current_step < len(self.solution_states) - 1:
            self.current_step += 1
            self.update_step_display()

    def handle_prev(self):
        """Xử lý nút Prev"""
        if not self.solution_states:
            self.view.show_warning("Cảnh báo", "Vui lòng giải puzzle trước!")
            return

        if self.current_step > 0:
            self.current_step -= 1
            self.update_step_display()

    def handle_auto(self):
        """Xử lý nút Auto"""
        if not self.solution_states or self.is_animating:
            return

        self.is_animating = True
        self.view.disable_auto_button()

        def animate():
            for step in range(len(self.solution_states)):
                self.current_step = step
                self.view.root.after(0, self.update_step_display)
                time.sleep(0.6)

            self.is_animating = False
            self.view.root.after(0, lambda: self.view.enable_auto_button())

        thread = threading.Thread(target=animate)
        thread.daemon = True
        thread.start()

    def handle_reset(self):
        """Xử lý nút Reset"""
        self.view.reset_canvas()
        self.view.display_info("")
        self.current_step = 0
        self.solution_states = []
        self.solution_actions = []
        self.view.update_status("Ready")
        self.model = None


# ============================================
# MAIN
# ============================================
def main():
    root = tk.Tk()
    view = PuzzleView(root)
    controller = PuzzleController(view)
    root.mainloop()


if __name__ == "__main__":
    main()
