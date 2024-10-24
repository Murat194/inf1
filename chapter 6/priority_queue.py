class PriorityQueue:
    def __init__(self):
        self.elements = []

    def is_empty(self):
        return len(self.elements) == 0

    def push(self, item, priority):
        self.elements.append((item, priority))
        self.elements.sort(key=lambda x: x[1])

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty priority queue")
        return self.elements.pop(0)[0]

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty priority queue")
        return self.elements[0][0]

    def size(self):
        return len(self.elements)

# Пример использования
pq = PriorityQueue()

pq.push("Задача 1", priority=2)
pq.push("Задача 2", priority=5)
pq.push("Задача 3", priority=1)

print("Первый элемент с наивысшим приоритетом:", pq.peek())  # Ожидаемый вывод: Задача 3

while not pq.is_empty():
    print("Обработка:", pq.pop())
