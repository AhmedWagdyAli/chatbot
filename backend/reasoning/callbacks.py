from langchain.callbacks.base import BaseCallbackHandler


class ReasoningCallbackHandler(BaseCallbackHandler):
    """
    A custom callback handler to capture reasoning steps during the execution
    of a chain or agent. This handler collects intermediate steps, tool usage,
    and final outputs for debugging or explanation purposes.
    """

    def __init__(self):
        """
        Initialize the callback handler with an empty list to store reasoning steps.
        """
        self.reasoning_steps = []

    def on_chain_start(self, serialized, inputs, **kwargs):
        """
        Called when a chain starts execution.

        Args:
            serialized (dict): Serialized representation of the chain.
            inputs (dict): Inputs provided to the chain.
        """
        self.reasoning_steps.append(f"Chain started with inputs: {inputs}")

    def on_chain_end(self, outputs, **kwargs):
        """
        Called when a chain finishes execution.

        Args:
            outputs (dict): Outputs produced by the chain.
        """
        self.reasoning_steps.append(f"Chain ended with outputs: {outputs}")

    def on_tool_start(self, serialized, input_str, **kwargs):
        """
        Called when a tool starts execution.

        Args:
            serialized (dict): Serialized representation of the tool.
            input_str (str): Input provided to the tool.
        """
        if (
            not self.reasoning_steps
            or self.reasoning_steps[-1] != f"Tool started with input: {input_str}"
        ):
            self.reasoning_steps.append(f"Tool started with input: {input_str}")

    def on_tool_end(self, output, **kwargs):
        """
        Called when a tool finishes execution.

        Args:
            output (str): Output produced by the tool.
        """
        if (
            not self.reasoning_steps
            or self.reasoning_steps[-1] != f"Tool ended with output: {output}"
        ):
            self.reasoning_steps.append(f"Tool ended with output: {output}")

    def on_text(self, text, **kwargs):
        """
        Called when intermediate text is generated during execution.

        Args:
            text (str): The intermediate text generated.
        """
        if text.strip() and (
            not self.reasoning_steps or self.reasoning_steps[-1] != text.strip()
        ):
            self.reasoning_steps.append(text.strip())
