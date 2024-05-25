items = {
    "pizza": {"cost": 50, "calories": 300},
    "hamburger": {"cost": 40, "calories": 250},
    "hot-dog": {"cost": 30, "calories": 200},
    "pepsi": {"cost": 10, "calories": 100},
    "cola": {"cost": 15, "calories": 220},
    "potato": {"cost": 25, "calories": 350}
}

def greedy_algorithm(items, budget):
    # Сортуємо елементи за співвідношенням калорій до вартості (від більшого до меншого)
    sorted_items = sorted(items.items(), key=lambda x: x[1]['calories'] / x[1]['cost'], reverse=True)
    
    total_calories = 0
    total_cost = 0
    chosen_items = []

    for item, info in sorted_items:
        if total_cost + info['cost'] <= budget:
            chosen_items.append(item)
            total_cost += info['cost']
            total_calories += info['calories']

    return chosen_items, total_calories

def dynamic_programming(items, budget):
    # Ініціалізуємо таблицю DP
    dp = [[0 for _ in range(budget + 1)] for _ in range(len(items) + 1)]
    item_list = list(items.items())

    for i in range(1, len(items) + 1):
        item_name, item_info = item_list[i - 1]
        cost = item_info['cost']
        calories = item_info['calories']
        
        for b in range(budget + 1):
            if cost > b:
                dp[i][b] = dp[i - 1][b]
            else:
                dp[i][b] = max(dp[i - 1][b], dp[i - 1][b - cost] + calories)

    total_calories = dp[len(items)][budget]
    b = budget
    chosen_items = []

    for i in range(len(items), 0, -1):
        if dp[i][b] != dp[i - 1][b]:
            item_name = item_list[i - 1][0]
            chosen_items.append(item_name)
            b -= items[item_name]['cost']

    chosen_items.reverse()
    return chosen_items, total_calories

# Тестування
budget = 100

greedy_result = greedy_algorithm(items, budget)
print("Greedy Algorithm Result:", greedy_result)

dp_result = dynamic_programming(items, budget)
print("Dynamic Programming Result:", dp_result)
