import turtle
import math

def draw_pythagoras_tree(t, length, level):
    if level == 0:
        t.forward(length)
        t.backward(length)
        return

    # Draw the trunk
    t.forward(length)

    # Save the current position and heading
    start_pos = t.pos()
    start_heading = t.heading()

    # Draw the left branch
    t.left(45)
    draw_pythagoras_tree(t, length / math.sqrt(2), level - 1)

    # Restore position and heading
    t.setpos(start_pos)
    t.setheading(start_heading)

    # Draw the right branch
    t.right(45)
    draw_pythagoras_tree(t, length / math.sqrt(2), level - 1)

    # Restore position and heading
    t.setpos(start_pos)
    t.setheading(start_heading)

    # Move back to the starting position
    t.backward(length)

def main():
    level = int(input("Enter the level of recursion: "))
    length = 100  # Initial length of the trunk

    # Setup the turtle
    screen = turtle.Screen()
    screen.bgcolor("white")
    t = turtle.Turtle()
    t.speed(0)  # Fastest drawing speed
    t.left(90)  # Start facing upwards
    t.up()
    t.goto(0, -250)  # Start position
    t.down()

    # Draw the Pythagoras Tree
    draw_pythagoras_tree(t, length, level)

    # Hide the turtle and display the result
    t.hideturtle()
    turtle.done()

if __name__ == "__main__":
    main()
