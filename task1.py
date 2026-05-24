"""
Завдання 1. Структури даних. Сортування. Робота з однозв'язним списком

- реверсування однозв'язного списку (зміна посилань між вузлами)
- сортування вставками для однозв'язного списку
- об'єднання двох відсортованих однозв'язних списків в один відсортований
"""


# ── Вузол та базовий клас списку ──────────────────────────────────────────────

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    # ── допоміжні методи ──────────────────────────────────────────────────────

    def append(self, data):
        """Додає елемент у кінець списку."""
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        current = self.head
        while current.next:
            current = current.next
        current.next = new_node

    def to_list(self):
        """Повертає звичайний Python-список значень."""
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def __str__(self):
        return " -> ".join(str(x) for x in self.to_list()) or "Empty"

    # ── 1. Реверсування ───────────────────────────────────────────────────────

    def reverse(self):
        """
        Реверсує однозв'язний список, змінюючи посилання між вузлами.
        Складність: O(n) час, O(1) пам'ять.
        """
        prev = None
        current = self.head
        while current:
            next_node = current.next   # зберігаємо наступний вузол
            current.next = prev        # змінюємо посилання назад
            prev = current             # рухаємо prev вперед
            current = next_node        # рухаємо current вперед
        self.head = prev               # новий початок списку

    # ── 2. Сортування вставками ───────────────────────────────────────────────

    def insertion_sort(self):
        """
        Сортує однозв'язний список методом вставок.
        Складність: O(n²) час, O(1) пам'ять.
        """
        sorted_head = None            # голова відсортованої частини

        current = self.head
        while current:
            next_node = current.next  # збережемо наступний необроблений вузол

            # Вставляємо current у правильне місце відсортованої частини
            if sorted_head is None or current.data <= sorted_head.data:
                # Вставка перед головою відсортованої частини
                current.next = sorted_head
                sorted_head = current
            else:
                search = sorted_head
                while search.next and search.next.data < current.data:
                    search = search.next
                current.next = search.next
                search.next = current

            current = next_node       # переходимо до наступного необробленого

        self.head = sorted_head

    # ── 3. Злиття двох відсортованих списків ─────────────────────────────────

    @staticmethod
    def merge_sorted(list_a: "LinkedList", list_b: "LinkedList") -> "LinkedList":
        """
        Об'єднує два відсортовані однозв'язні списки в один відсортований список.
        Повертає новий LinkedList.
        Складність: O(n + m) час, O(1) пам'ять (переставляємо вузли).
        """
        # "Фіктивний" початковий вузол спрощує вставку
        dummy = Node(0)
        tail = dummy

        a = list_a.head
        b = list_b.head

        while a and b:
            if a.data <= b.data:
                tail.next = a
                a = a.next
            else:
                tail.next = b
                b = b.next
            tail = tail.next

        # Приєднуємо залишок того списку, що ще не вичерпаний
        tail.next = a if a else b

        merged = LinkedList()
        merged.head = dummy.next
        return merged


# ── Демонстрація ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("=" * 55)
    print("  1. Реверсування однозв'язного списку")
    print("=" * 55)
    ll = LinkedList()
    for val in [1, 2, 3, 4, 5]:
        ll.append(val)
    print(f"  До реверсування : {ll}")
    ll.reverse()
    print(f"  Після реверсування: {ll}")

    print()
    print("=" * 55)
    print("  2. Сортування вставками")
    print("=" * 55)
    ll2 = LinkedList()
    for val in [4, 2, 7, 1, 9, 3]:
        ll2.append(val)
    print(f"  До сортування   : {ll2}")
    ll2.insertion_sort()
    print(f"  Після сортування: {ll2}")

    print()
    print("=" * 55)
    print("  3. Злиття двох відсортованих списків")
    print("=" * 55)
    a = LinkedList()
    b = LinkedList()
    for val in [1, 3, 5, 7]:
        a.append(val)
    for val in [2, 4, 6, 8, 10]:
        b.append(val)
    print(f"  Список A : {a}")
    print(f"  Список B : {b}")
    merged = LinkedList.merge_sorted(a, b)
    print(f"  Злитий   : {merged}")
    print("=" * 55)

