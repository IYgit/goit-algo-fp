class ListNode:
    def __init__(self, value=0, next=None):
        self.value = value
        self.next = next

def reverse_linked_list(head):
    prev = None
    current = head
    
    while current:
        next_node = current.next
        current.next = prev
        prev = current
        current = next_node
        
    return prev

def insertion_sort_linked_list(head):
    if not head or not head.next:
        return head
    
    sorted_head = ListNode(0)  # Додатковий фіктивний вузол
    current = head
    
    while current:
        prev = sorted_head
        next_node = current.next
        
        # Знайти місце для вставки
        while prev.next and prev.next.value < current.value:
            prev = prev.next
        
        # Вставити вузол
        current.next = prev.next
        prev.next = current
        current = next_node
    
    return sorted_head.next

def merge_sorted_linked_lists(l1, l2):
    dummy = ListNode(0)
    tail = dummy
    
    while l1 and l2:
        if l1.value < l2.value:
            tail.next = l1
            l1 = l1.next
        else:
            tail.next = l2
            l2 = l2.next
        tail = tail.next
    
    if l1:
        tail.next = l1
    if l2:
        tail.next = l2
    
    return dummy.next

def print_linked_list(head):
    current = head
    while current:
        print(current.value, end=" -> ")
        current = current.next
    print("None")

# Функція для створення однозв'язного списку зі списку значень
def create_linked_list(values):
    if not values:
        return None
    head = ListNode(values[0])
    current = head
    for value in values[1:]:
        current.next = ListNode(value)
        current = current.next
    return head

# Тестування функцій
if __name__ == "__main__":
    # Створення однозв'язного списку
    values = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]
    head = create_linked_list(values)
    print("Оригінальний список:")
    print_linked_list(head)
    
    # Тестування реверсування
    reversed_head = reverse_linked_list(head)
    print("Реверсований список:")
    print_linked_list(reversed_head)
    
    # Тестування сортування
    sorted_head = insertion_sort_linked_list(reversed_head)
    print("Відсортований список:")
    print_linked_list(sorted_head)
    
    # Створення двох відсортованих списків для тестування об'єднання
    list1 = create_linked_list([1, 3, 5])
    list2 = create_linked_list([2, 4, 6])
    print("Перший відсортований список:")
    print_linked_list(list1)
    print("Другий відсортований список:")
    print_linked_list(list2)
    
    # Тестування об'єднання
    merged_head = merge_sorted_linked_lists(list1, list2)
    print("Об'єднаний відсортований список:")
    print_linked_list(merged_head)
