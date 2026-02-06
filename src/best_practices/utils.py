def add_numbers(a: int, b: int) -> int:
    """Adds two integers and returns the result."""
    return a + b


def format_greeting(name: str) -> str:
    """Returns a formatted greeting string."""
    if not name:
        return "Hello, Stranger!"
    return f"Hello, {name}!"
