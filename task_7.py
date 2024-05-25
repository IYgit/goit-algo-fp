import random
import matplotlib.pyplot as plt

def simulate_dice_rolls(num_rolls):
    results = {}
    for _ in range(num_rolls):
        roll = random.randint(1, 6) + random.randint(1, 6)
        if roll in results:
            results[roll] += 1
        else:
            results[roll] = 1
    return results

def calculate_probabilities(results, total_rolls):
    probabilities = {}
    for sum_, count in results.items():
        probabilities[sum_] = count / total_rolls * 100
    return probabilities

# Симулюємо кидки двох кубиків
num_rolls = 1000000
results = simulate_dice_rolls(num_rolls)

# Обчислюємо ймовірності для кожної суми
probabilities = calculate_probabilities(results, num_rolls)

# Виводимо результати
for sum_, probability in probabilities.items():
    print(f"Сума: {sum_}, Ймовірність: {probability:.2f}%")

# Порівнюємо з аналітичними розрахунками
analytical_probabilities = {
    2: 2.78, 3: 5.56, 4: 8.33, 5: 11.11, 6: 13.89, 7: 16.67,
    8: 13.89, 9: 11.11, 10: 8.33, 11: 5.56, 12: 2.78
}

print("\nПорівняння з аналітичними розрахунками:")
for sum_, probability in analytical_probabilities.items():
    print(f"Сума: {sum_}, Ймовірність (аналітично): {probability:.2f}%")

def plot_probabilities(probabilities_mc, probabilities_analytical):
    plt.figure(figsize=(10, 6))
    plt.bar(probabilities_mc.keys(), probabilities_mc.values(), color='skyblue', alpha=0.7, label='Метод Монте-Карло')
    plt.plot(probabilities_analytical.keys(), probabilities_analytical.values(), marker='o', color='orange', linestyle='-', linewidth=2, label='Аналітичні розрахунки')
    plt.xlabel('Сума чисел на кубиках')
    plt.ylabel('Ймовірність')
    plt.title('Порівняння ймовірностей сум при киданні двох кубиків')
    plt.legend()
    plt.xticks(range(2, 13))
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.show()

# Викликаємо функцію для побудови графіку
plot_probabilities(probabilities, analytical_probabilities)
