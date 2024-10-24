class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next

def map_linked_list(head, mapping_function):
    # Создаем фиктивный узел для удобства добавления элементов в новый список
    dummy = Node(None)
    current_new = dummy
    current_old = head

    while current_old:
        current_new.next = Node(mapping_function(current_old.data))
        current_new = current_new.next
        current_old = current_old.next

    return dummy.next

# Пример использования
# Определяем связный список: 1 -> 2 -> 3
original_list = Node(1, Node(2, Node(3)))

# Определяем функцию отображения: x => x * 2
def mapping_function(x):
    return x * 2

# Применяем функцию отображения
mapped_list = map_linked_list(original_list, mapping_function)

# Выводим результат
current = mapped_list
while current:
    print(current.data, end=" -> ")
    current = current.next
# Вывод: 2 -> 4 -> 6 ->
