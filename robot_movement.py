# robot_movement.py

from collections import deque
import heapq

# Yönler: Yukarı, Sağ, Aşağı, Sol
DIRECTIONS = [(-1, 0), (0, 1), (1, 0), (0, -1)]

class VacuumRobot:
    def __init__(self, grid, row, col, grid_width, grid_height):
        self.grid = grid  # Ortam ızgarası
        self.row = row  # Robotun mevcut satırı
        self.col = col  # Robotun mevcut sütunu
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.cleaned = set()  # Temizlenmiş konumların kümesi
        self.obstacles = set()  # Engel konumlarının kümesi
        self.map = [[-1 for _ in range(self.grid_width)] for _ in range(self.grid_height)]  # Robotun iç haritası
        self.phase = 'exploration'  # Aşamalar: keşif, temizlik, geri dönüş, bitmiş
        self.start_position = (row, col)
        self.cleaned.add((self.row, self.col))
        self.map[self.row][self.col] = 0  # Başlangıç pozisyonunu serbest alan olarak işaretle
        self.coverage_path = []
        self.path = []
        self.returning = False  # Başlangıç pozisyonuna geri dönme bayrağı
        self.dir_index = 0  # Başlangıç yönü (0: Yukarı)

    def explore(self):
        if self.phase == 'exploration':
            self.explore_environment()
        elif self.phase == 'cleaning':
            self.clean()
        elif self.phase == 'returning':
            self.return_to_start()
        elif self.phase == 'finished':
            return False  # Temizlik tamamlandı
        return True

    def explore_environment(self):
        # BFS kullanarak çevreyi keşfet
        queue = deque()
        queue.append((self.row, self.col))
        visited = set()
        visited.add((self.row, self.col))
        while queue:
            current = queue.popleft()
            for dr, dc in DIRECTIONS:
                nr, nc = current[0] + dr, current[1] + dc
                if 0 <= nr < self.grid_height and 0 <= nc < self.grid_width:
                    if (nr, nc) not in visited:
                        if self.grid[nr][nc] == 0:
                            self.map[nr][nc] = 0  # Serbest alan olarak işaretler
                            visited.add((nr, nc))
                            queue.append((nr, nc))
                        else:
                            self.map[nr][nc] = 1  # Engel olarak işaretler
                            self.obstacles.add((nr, nc))
        # Keşiften sonra temizlik yolunu planlar
        self.plan_cleaning_path()
        self.phase = 'cleaning'

    def plan_cleaning_path(self):
        # Sistematik bir kapsama yolu planlama (CPP) yöntemi kullan
        # Basit bir satır-satır (çim biçme makinesi) desenini uygular
        for r in range(self.grid_height):
            col_range = range(self.grid_width) if r % 2 == 0 else range(self.grid_width - 1, -1, -1)
            for c in col_range:
                if self.map[r][c] == 0:
                    self.coverage_path.append((r, c))

    def clean(self):
        if self.path:
            # Planlanmış yolu takip et
            next_pos = self.path.pop(0)
            self.move_to(next_pos)
        elif self.coverage_path:
            next_cell = self.coverage_path.pop(0)
            if (next_cell[0], next_cell[1]) not in self.cleaned:
                # A* algoritmasını kullanarak bir sonraki hücreye yol planlar
                self.path = self.plan_path((self.row, self.col), next_cell)
                if self.path:
                    self.path.pop(0)  # Mevcut pozisyonu kaldır
                else:
                    # Bir sonraki hücreye yol bulunamadıysa (muhtemelen engellenmiş), atlar
                    pass
        else:
            # Temizlik tamamlandı, başlangıç pozisyonuna geri dön
            self.phase = 'returning'
            self.path = self.plan_path((self.row, self.col), self.start_position)
            if self.path:
                self.path.pop(0)  # Mevcut pozisyonu kaldır

    def return_to_start(self):
        if self.path:
            next_pos = self.path.pop(0)
            self.move_to(next_pos)
        else:
            self.phase = 'finished'
            print("Temizlik tamamlandı ve başlangıç pozisyonuna geri dönüldü.")

    def move_to(self, position):
        self.row, self.col = position
        self.cleaned.add((self.row, self.col))

    def plan_path(self, start, goal):
        # Yol bulma için A* algoritmasını uygular
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        g_score = {start: 0}
        while open_set:
            _, current = heapq.heappop(open_set)
            if current == goal:
                return self.reconstruct_path(came_from, current)
            for dr, dc in DIRECTIONS:
                neighbor = (current[0] + dr, current[1] + dc)
                if 0 <= neighbor[0] < self.grid_height and 0 <= neighbor[1] < self.grid_width:
                    if self.map[neighbor[0]][neighbor[1]] == 1:
                        continue  # Engelleri atlar
                    tentative_g_score = g_score[current] + 1
                    if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                        came_from[neighbor] = current
                        g_score[neighbor] = tentative_g_score
                        f_score = tentative_g_score + self.heuristic(neighbor, goal)
                        heapq.heappush(open_set, (f_score, neighbor))
        return []

    def reconstruct_path(self, came_from, current):
        # Bulunan yolu yeniden oluştur
        path = [current]
        while current in came_from:
            current = came_from[current]
            path.append(current)
        path.reverse()
        return path

    def heuristic(self, a, b):
        # Manhattan mesafe heuristiğini kullan
        return abs(a[0] - b[0]) + abs(a[1] - b[1])
