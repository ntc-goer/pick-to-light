import sys

from PyQt6.QtWidgets import QApplication
from dotenv import load_dotenv

from db.db_manager import init_db
from page.MainWindow import MainWindow

if __name__ == '__main__':
    # app = QApplication(sys.argv)
    # load_dotenv()
    # init_db()
    #
    # window = MainWindow()
    #
    # # window.showFullScreen()
    # window.show()
    #
    # sys.exit(app.exec())

    import heapq


    def dijkstra(graph, start):
        # graph: dict {node: [(neighbor, weight), ...]}
        # start: đỉnh bắt đầu

        # khoảng cách ban đầu: vô cùng
        distances = {node: float('inf') for node in graph}
        distances[start] = 0  # đỉnh bắt đầu có khoảng cách = 0

        # dùng priority queue (min-heap)
        pq = [(0, start)]  # (khoảng cách, node)

        while pq:
            current_distance, current_node = heapq.heappop(pq)

            # Nếu khoảng cách lấy ra lớn hơn đã biết thì bỏ qua
            if current_distance > distances[current_node]:
                continue

            # duyệt các node kề
            for neighbor, weight in graph[current_node]:
                distance = current_distance + weight

                # Nếu tìm được đường đi ngắn hơn
                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    heapq.heappush(pq, (distance, neighbor))

        return distances


    # Ví dụ: đồ thị
    graph = {
        'A': [('B', 4), ('C', 2)],
        'B': [('A', 4), ('C', 5), ('D', 10)],
        'C': [('A', 2), ('B', 5), ('D', 3)],
        'D': [('B', 10), ('C', 3)]
    }

    start_node = 'A'
    shortest_paths = dijkstra(graph, start_node)

    print(f"Khoảng cách ngắn nhất từ {start_node}:")
    for node, dist in shortest_paths.items():
        print(f"{start_node} -> {node}: {dist}")
