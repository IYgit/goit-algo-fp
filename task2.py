"""
Завдання 2. Рекурсія. Створення фрактала "дерево Піфагора"

Програма малює фрактал "дерево Піфагора" за допомогою рекурсії.
Користувач вказує рівень рекурсії через консоль.
Візуалізація реалізована за допомогою matplotlib.
"""

import math
import matplotlib.pyplot as plt


# ── Параметри малювання ───────────────────────────────────────────────────────

TRUNK_LENGTH = 1.0          # нормована довжина стовбура
ANGLE_LEFT   = 45           # кут лівої гілки (градуси)
ANGLE_RIGHT  = 45           # кут правої гілки (градуси)
SHRINK       = math.sqrt(2) / 2   # ~0.707 — класична пропорція дерева Піфагора

# Кольори: стовбур → листки (RGB 0–1)
COLOR_ROOT = (0.40, 0.26, 0.13)   # темно-коричневий
COLOR_LEAF = (0.13, 0.55, 0.13)   # лісово-зелений


def lerp_color(t: float) -> tuple[float, float, float]:
    """Лінійна інтерполяція кольору між ROOT та LEAF (t від 0 до 1)."""
    return tuple(COLOR_ROOT[i] + (COLOR_LEAF[i] - COLOR_ROOT[i]) * t for i in range(3))  # type: ignore


def draw_pythagorean_tree(ax: plt.Axes,
                          x: float, y: float,
                          angle_deg: float,
                          length: float,
                          level: int,
                          max_level: int) -> None:
    """
    Рекурсивно малює дерево Піфагора.

    Args:
        ax        : осі matplotlib
        x, y      : координати початку гілки
        angle_deg : напрямок гілки (градуси від горизонталі)
        length    : довжина поточної гілки
        level     : залишкова глибина рекурсії (0 = зупинитися)
        max_level : початкова глибина (для кольорової інтерполяції)
    """
    if level == 0:
        return

    # Кінцева точка гілки
    rad = math.radians(angle_deg)
    x2 = x + length * math.cos(rad)
    y2 = y + length * math.sin(rad)

    # Колір та товщина — залежать від рівня
    t = (max_level - level) / max_level
    color = lerp_color(t)
    lw = max(0.5, level * 1.2)

    ax.plot([x, x2], [y, y2], color=color, linewidth=lw, solid_capstyle="round")

    # Рекурсивні гілки
    draw_pythagorean_tree(ax, x2, y2, angle_deg + ANGLE_LEFT,
                          length * SHRINK, level - 1, max_level)
    draw_pythagorean_tree(ax, x2, y2, angle_deg - ANGLE_RIGHT,
                          length * SHRINK, level - 1, max_level)


def get_recursion_level() -> int:
    """Запитує у користувача рівень рекурсії (1–15)."""
    while True:
        try:
            level = int(input("Введіть рівень рекурсії (рекомендовано 1–12): "))
            if 1 <= level <= 15:
                return level
            print("  Будь ласка, введіть число від 1 до 15.")
        except ValueError:
            print("  Помилка: введіть ціле число.")


def main() -> None:
    level = get_recursion_level()

    fig, ax = plt.subplots(figsize=(10, 9))
    fig.patch.set_facecolor("black")
    ax.set_facecolor("black")
    ax.set_aspect("equal")
    ax.axis("off")
    ax.set_title(f"Дерево Піфагора  (рівень рекурсії: {level})",
                 color="white", fontsize=14, pad=12)

    # Стовбур прямовисно вгору (кут 90°), початок знизу по центру
    draw_pythagorean_tree(ax, 0.0, 0.0, 90.0, TRUNK_LENGTH, level, level)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
