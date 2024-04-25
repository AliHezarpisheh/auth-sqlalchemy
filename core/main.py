"""Main module for handling user interactions with the application."""

from auth.controllers import UserController

from .commands.enums import Menu
from .views import MenuView


class Main:
    """Main class for controlling the flow of the application."""

    def __init__(self) -> None:
        """Initialize the Main class."""
        self.menu_view = MenuView()
        self.user_controller = UserController()

    def run(self) -> None:
        """
        Run the main loop of the application.

        Displays a welcome message, gets user input, and executes corresponding actions.
        """
        self.user_controller.show_welcome_msg()

        while True:
            command = self.menu_view.get_command()

            if command == Menu.LOGIN:
                self.user_controller.login()
            elif command == Menu.REGISTER:
                self.user_controller.register()
            elif command == Menu.QUIT:
                print("Bye Bye!" + "\U0001f44b\U0001f60a")  # Bye Bye! 👋😊
                break
            else:
                print("Invalid Options")
