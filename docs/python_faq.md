# Python FAQ

## What is a virtual environment?

A virtual environment is an isolated Python installation that lets you install packages for a specific project without affecting your system Python. You create one with `python -m venv myenv` and activate it with `source myenv/bin/activate` on Mac/Linux or `myenv\Scripts\activate` on Windows. Once activated, `pip install` puts packages only inside that environment.

## How do decorators work?

A decorator is a function that wraps another function to extend its behavior. You apply it with the `@` symbol above a function definition. For example, `@login_required` above a view function checks if the user is logged in before running the view. Under the hood, `@decorator` is just shorthand for `func = decorator(func)`.

## What is the difference between a list and a tuple?

Lists are mutable - you can add, remove, or change items after creation. Tuples are immutable - once created, their contents cannot be changed. Use lists when you need a collection that changes over time, and tuples when you want a fixed group of values (like returning multiple values from a function). Tuples are also slightly faster and use less memory than lists.

## How does pip work?

pip is Python's package installer. It downloads packages from PyPI (Python Package Index) and installs them into your current environment. Common commands: `pip install requests` to install a package, `pip freeze > requirements.txt` to save your current packages, and `pip install -r requirements.txt` to install from a saved list.

## What are list comprehensions?

List comprehensions are a compact way to create lists. Instead of writing a for loop to build a list, you write it in one line: `[x * 2 for x in range(10)]` creates `[0, 2, 4, 6, 8, 10, 12, 14, 16, 18]`. You can also add conditions: `[x for x in range(20) if x % 3 == 0]` gives all multiples of 3 under 20.

## What is __init__ in a Python class?

`__init__` is the constructor method that runs when you create a new instance of a class. It sets up the initial state of the object. For example: `def __init__(self, name): self.name = name` stores the name when you do `person = Person("Alice")`. The `self` parameter refers to the instance being created.
