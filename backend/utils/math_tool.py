import math
from langchain.tools import tool


@tool
def calculator_tool(expression: str) -> str:
    """
    Evaluate a simple mathematical expression.

    This tool evaluates mathematical expressions provided as strings.
    It supports basic arithmetic operations (e.g., addition, subtraction,
    multiplication, division) and mathematical functions from the `math` module.
    The result is rounded to two decimal places.

    Args:
        expression (str): The mathematical expression to evaluate.
                        Multiplication can be represented using 'x' or '*'.

    Returns:
        str: The result of the evaluation as a string, rounded to two decimal places.
            If an error occurs during evaluation, an error message is returned.
    """
    try:
        expression = expression.replace("x", "*")
        result = eval(expression, {"__builtins__": {}}, vars(math))
        return str(round(result, 2))
    except Exception as e:
        return f"Error: {e}"
