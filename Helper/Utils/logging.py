"""File which stores the NexusLogging Class"""
from typing import Optional

from Helper.NexusColors.color import NexusColor
from Helper.NexusColors.gradient import GradientPrinter

class NexusLogging:
    """A class for Logging"""

    LC = f"{NexusColor.NEXUS}[{NexusColor.LIGHTBLACK}NEXUS{NexusColor.NEXUS}]"


    @staticmethod
    def print_status(
        token: str, message: str, color: str, prefix: Optional[str] = None, length: Optional[int] = 45
    ) -> None:
        """
        Prints the current status of an operation with a gradient effect.

        Args:
            token (str): The token associated with the operation.
            message (str): The status message to display.
            color (str): The color code for the message text.
        """
        GradientPrinter.gradient_print(
            input_text=token[:length],
            end_text=f"{NexusColor.RESET} -> {color}{message}",
            start_color="#ff08b5",
            end_color="#8308ff",
            prefix=prefix
        )

    @staticmethod
    def print_error(
        token: str, message: str, response: str
    ) -> None:
        """
        Prints error details in case of a failed operation.

        Args:
            token (str): The token associated with the failed operation.
            message (str): The error message to display.
            response (requests.Response): The server response containing error details.
        """
        GradientPrinter.gradient_print(
            input_text=token[:45],
            end_text=f"{NexusColor.RESET} -> {NexusColor.RED}{message}: {response.text} ({response.status_code})",
            start_color="#ff08b5",
            end_color="#8308ff",
            correct=False,
        )
