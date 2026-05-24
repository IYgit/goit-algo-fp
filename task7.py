"""
Завдання 7. Використання методу Монте-Карло

Симуляція кидання двох кубиків велику кількість разів.
Обчислення ймовірності кожної суми (2–12) методом Монте-Карло
та порівняння з аналітичними значеннями.

Виводить:
  - таблицю порівняння (консоль)
  - стовпчастий графік з обома рядами (matplotlib)
"""

import random
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

# ── Аналітичні ймовірності ────────────────────────────────────────────────────

ANALYTICAL: dict[int, float] = {
    2:  1 / 36,
    3:  2 / 36,
    4:  3 / 36,
    5:  4 / 36,
    6:  5 / 36,
    7:  6 / 36,
    8:  5 / 36,
    9:  4 / 36,
    10: 3 / 36,
    11: 2 / 36,
    12: 1 / 36,
}


# ── Симуляція Монте-Карло ─────────────────────────────────────────────────────

def monte_carlo_dice(num_rolls: int = 1_000_000) -> dict[int, float]:
    """
    Кидає два кубики num_rolls разів і повертає словник
    {сума → відносна частота}.

    Args:
        num_rolls: кількість кидань (за замовчуванням 1 000 000)

    Returns:
        Словник {сума (2..12): ймовірність}
    """
    counts: dict[int, int] = {s: 0 for s in range(2, 13)}

    for _ in range(num_rolls):
        roll = random.randint(1, 6) + random.randint(1, 6)
        counts[roll] += 1

    return {s: counts[s] / num_rolls for s in range(2, 13)}


# ── Виведення таблиці ─────────────────────────────────────────────────────────

def print_table(mc_probs: dict[int, float], num_rolls: int) -> None:
    fractions = {
        2: "1/36", 3: "2/36", 4: "3/36", 5: "4/36",  6: "5/36",
        7: "6/36", 8: "5/36", 9: "4/36", 10: "3/36", 11: "2/36", 12: "1/36",
    }
    header = f"{'Сума':>5}  {'Аналіт. (точна)':>18}  {'Монте-Карло':>13}  {'Різниця':>9}"
    print(f"\nСимуляція: {num_rolls:,} кидань двох кубиків")
    print("=" * len(header))
    print(header)
    print("-" * len(header))
    for s in range(2, 13):
        a  = ANALYTICAL[s]
        mc = mc_probs[s]
        print(f"{s:>5}  {a*100:>7.2f}% ({fractions[s]:>4})  "
              f"{mc*100:>11.2f}%  {abs(a - mc)*100:>7.4f}%")
    print("=" * len(header))


# ── Графік ────────────────────────────────────────────────────────────────────

def plot_comparison(mc_probs: dict[int, float], num_rolls: int) -> None:
    sums    = list(range(2, 13))
    anal    = [ANALYTICAL[s] * 100 for s in sums]
    mc      = [mc_probs[s]   * 100 for s in sums]

    x      = range(len(sums))
    width  = 0.38

    fig, ax = plt.subplots(figsize=(11, 6))
    bars_a  = ax.bar([i - width / 2 for i in x], anal, width,
                     label="Аналітична (точна)", color="#2196F3", alpha=0.85)
    bars_mc = ax.bar([i + width / 2 for i in x], mc,   width,
                     label=f"Монте-Карло ({num_rolls:,} кидань)",
                     color="#FF5722", alpha=0.85)

    # Підписи значень над стовпцями
    for bar in bars_a:
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.15,
                f"{bar.get_height():.2f}%",
                ha="center", va="bottom", fontsize=7.5, color="#1565C0")
    for bar in bars_mc:
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.15,
                f"{bar.get_height():.2f}%",
                ha="center", va="bottom", fontsize=7.5, color="#BF360C")

    ax.set_xticks(list(x))
    ax.set_xticklabels([str(s) for s in sums])
    ax.set_xlabel("Сума двох кубиків", fontsize=12)
    ax.set_ylabel("Імовірність (%)", fontsize=12)
    ax.set_title("Імовірності сум при киданні двох кубиків\n"
                 "Аналітичний розрахунок vs Метод Монте-Карло",
                 fontsize=13, fontweight="bold")
    ax.yaxis.set_major_formatter(mticker.FormatStrFormatter("%.1f%%"))
    ax.legend(fontsize=11)
    ax.set_ylim(0, max(anal) * 1.25)
    ax.grid(axis="y", linestyle="--", alpha=0.5)

    plt.tight_layout()
    plt.show()


# ── Головна функція ───────────────────────────────────────────────────────────

def main() -> None:
    NUM_ROLLS = 1_000_000

    print(f"Запускаємо симуляцію ({NUM_ROLLS:,} кидань)…")
    mc_probs = monte_carlo_dice(NUM_ROLLS)

    print_table(mc_probs, NUM_ROLLS)
    plot_comparison(mc_probs, NUM_ROLLS)


if __name__ == "__main__":
    main()

