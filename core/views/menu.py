"""Module for handling menu interactions."""

import inquirer


class MenuView:
    """Class for displaying menu options and retrieving user commands."""

    def get_command(self) -> str:
        """
        Prompt the user to select a command from a list of options.

        Returns
        -------
        str
            The selected command.
        """
        questions = [
            inquirer.List(
                "command",
                message="Please select an option",
                choices=["Login", "Register", "Quit"],
            ),
        ]
        answers = inquirer.prompt(questions)
        command: str = answers["command"][0]
        return command
