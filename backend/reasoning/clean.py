import re


def remove_ansi_escape_codes(text: str) -> str:
    """
    Remove ANSI escape codes from the given text.

    ANSI escape codes are often used for terminal text formatting (e.g., colors).
    This function removes these codes to clean up the text.

    Args:
        text (str): The input text containing ANSI escape codes.

    Returns:
        str: The cleaned text with ANSI escape codes removed.
    """
    ansi_escape = re.compile(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])")
    return ansi_escape.sub("", text)


def clean_reasoning(raw_text: str) -> str:
    """
    Extract and clean the reasoning steps from raw text.

    This function processes the raw reasoning text, capturing relevant lines
    such as "Thought", "Action", "Action Input", "Observation", and "Final Answer".
    It returns the reasoning steps for the final answer block.

    Args:
        raw_text (str): The raw reasoning text to process.

    Returns:
        str: The cleaned reasoning steps for the final answer block, joined as a string.
    """
    reasoning_lines = []
    temp_block = []
    final_reasoning_blocks = []
    capture = False

    for line in raw_text.splitlines():
        line = line.strip()
        if not line:
            continue

        # Start capturing reasoning when a "Question:" line is encountered
        if re.match(r"^Question:", line):
            capture = True

        if capture:
            # Capture lines matching reasoning steps
            if re.match(
                r"^(Thought:|Action:|Action Input:|Observation:|Final Answer:)", line
            ):
                temp_block.append(line)
                # If "Final Answer:" is encountered, save the block and reset
                if line.startswith("Final Answer:"):
                    final_reasoning_blocks.append(temp_block)
                    temp_block = []

    # Use the last reasoning block if available
    if final_reasoning_blocks:
        reasoning_lines = final_reasoning_blocks[-1]

    return "\n".join(reasoning_lines)
