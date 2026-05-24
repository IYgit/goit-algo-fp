"""
Завдання 6. Жадібні алгоритми та динамічне програмування

Задача: обрати страви з максимальною сумарною калорійністю
        в межах заданого бюджету.

Два підходи:
  1. greedy_algorithm      — жадібний алгоритм (сортування за ratio кал/грн)
  2. dynamic_programming   — ДП (задача про рюкзак 0/1), гарантує оптимум
"""

# ── Вхідні дані ───────────────────────────────────────────────────────────────

items = {
    "pizza":     {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog":   {"cost": 30, "calories": 200},
    "pepsi":     {"cost": 10, "calories": 100},
    "cola":      {"cost": 15, "calories": 220},
    "potato":    {"cost": 25, "calories": 350},
}


# ── 1. Жадібний алгоритм ──────────────────────────────────────────────────────

def greedy_algorithm(items: dict, budget: int) -> tuple[list[str], int, int]:
    """
    Жадібно обирає страви, гортаючи їх у порядку спадання
    співвідношення калорії / вартість.

    Args:
        items  : словник страв {назва: {cost, calories}}
        budget : максимальний бюджет

    Returns:
        (chosen, total_cost, total_calories)
    """
    # Сортуємо за спаданням ratio = calories / cost
    sorted_items = sorted(
        items.items(),
        key=lambda x: x[1]["calories"] / x[1]["cost"],
        reverse=True,
    )

    chosen:          list[str] = []
    total_cost:      int       = 0
    total_calories:  int       = 0

    for name, props in sorted_items:
        if total_cost + props["cost"] <= budget:
            chosen.append(name)
            total_cost     += props["cost"]
            total_calories += props["calories"]

    return chosen, total_cost, total_calories


# ── 2. Динамічне програмування (задача 0/1 «рюкзак») ─────────────────────────

def dynamic_programming(items: dict, budget: int) -> tuple[list[str], int, int]:
    """
    Знаходить оптимальний набір страв методом динамічного програмування
    (задача про рюкзак 0/1).

    Таблиця dp[i][w] = максимальна калорійність при використанні перших i
    страв і бюджеті w.

    Args:
        items  : словник страв {назва: {cost, calories}}
        budget : максимальний бюджет

    Returns:
        (chosen, total_cost, total_calories)
    """
    names = list(items.keys())
    costs = [items[n]["cost"]     for n in names]
    cals  = [items[n]["calories"] for n in names]
    n     = len(names)

    # Будуємо таблицю ДП розміром (n+1) × (budget+1)
    dp = [[0] * (budget + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        cost_i = costs[i - 1]
        cal_i  = cals[i - 1]
        for w in range(budget + 1):
            # Не беремо страву i
            dp[i][w] = dp[i - 1][w]
            # Беремо страву i (якщо вміщається)
            if cost_i <= w:
                with_item = dp[i - 1][w - cost_i] + cal_i
                if with_item > dp[i][w]:
                    dp[i][w] = with_item

    # Відновлення вибраних страв (backtracking)
    chosen:         list[str] = []
    total_cost:     int       = 0
    w = budget
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:          # страва i була взята
            chosen.append(names[i - 1])
            total_cost += costs[i - 1]
            w          -= costs[i - 1]

    total_calories = dp[n][budget]
    return chosen[::-1], total_cost, total_calories


# ── Демонстрація ──────────────────────────────────────────────────────────────

def print_result(method: str,
                 chosen: list[str],
                 total_cost: int,
                 total_calories: int,
                 budget: int) -> None:
    print(f"\n  {method}")
    print(f"  {'Страва':<14} {'Вартість':>10} {'Калорії':>10}  (ratio)")
    print("  " + "-" * 50)
    for name in chosen:
        c  = items[name]["cost"]
        ca = items[name]["calories"]
        print(f"  {name:<14} {c:>10} {ca:>10}    {ca/c:.2f}")
    print("  " + "-" * 50)
    print(f"  {'Разом':<14} {total_cost:>10} {total_calories:>10}")
    print(f"  Залишок бюджету: {budget - total_cost}")


def main() -> None:
    budget = 100

    print("=" * 56)
    print(f"  Бюджет: {budget} грн")
    print("=" * 56)

    # Таблиця доступних страв
    print(f"\n  {'Страва':<14} {'Вартість':>10} {'Калорії':>10}  (ratio)")
    print("  " + "-" * 50)
    for name, props in sorted(items.items(),
                               key=lambda x: x[1]["calories"] / x[1]["cost"],
                               reverse=True):
        ratio = props["calories"] / props["cost"]
        print(f"  {name:<14} {props['cost']:>10} {props['calories']:>10}    {ratio:.2f}")

    # ── Жадібний алгоритм ──
    chosen_g, cost_g, cal_g = greedy_algorithm(items, budget)
    print_result("Жадібний алгоритм", chosen_g, cost_g, cal_g, budget)

    # ── Динамічне програмування ──
    chosen_d, cost_d, cal_d = dynamic_programming(items, budget)
    print_result("Динамічне програмування (оптимум)", chosen_d, cost_d, cal_d, budget)

    # ── Порівняння ──
    print(f"\n{'='*56}")
    print(f"  Порівняння результатів:")
    print(f"  Жадібний:  {cal_g} кал  (витрачено {cost_g} грн)")
    print(f"  ДП:        {cal_d} кал  (витрачено {cost_d} грн)")
    if cal_d > cal_g:
        print(f"  → ДП знайшло кращий розв'язок на {cal_d - cal_g} кал")
    elif cal_d == cal_g:
        print(f"  → Обидва методи дали однаковий результат")
    print("=" * 56)


if __name__ == "__main__":
    main()

