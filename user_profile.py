import colorama
colorama.init(autoreset=True)

class UserProfile:
    def __init__(self, attendance_file: str = "attendance.csv") -> None:
        """
        Initializes a new UserProfile instance and automatically sets the user's name 
        by reading the last line of the attendance CSV file.

        :param attendance_file: The file path for the attendance CSV file.
        """
        self._user_name = None
        self.attendance_file = attendance_file
        # Automatically initialize the user's name during object construction.
        self.init_user_name()

    def get_user_name(self) -> str:
        """
        Gets the user's name.
        
        :return: The user's name.
        """
        return self._user_name

    def set_user_name(self, name: str) -> None:
        """
        Sets the user's name.
        
        :param name: The name to set.
        """
        self._user_name = name

    def init_user_name(self) -> None:
        """
        Initializes the user's name by reading the last line of the attendance file.
        Extracts the name from that line and sets it via the setter.
        """
        try:
            with open(self.attendance_file, "r+") as attendance:
                lines = attendance.readlines()
                if lines:
                    # Assume the name is the first element of the last line after stripping quotes.
                    last_line = lines[-1]
                    extracted_name = last_line.replace("'", "").split(",")[0].strip()
                    self.set_user_name(extracted_name)
                else:
                    print(colorama.Fore.LIGHTRED_EX + "Attendance file is empty.")
                    self.set_user_name("Unknown")
        except Exception as e:
            print(colorama.Fore.LIGHTRED_EX + f"An error occurred while initializing user name: {e}")
            self.set_user_name("Unknown")

    def __str__(self) -> str:
        return f"UserProfile(user_name={self.get_user_name()})"


if __name__ == "__main__":
    user_profile = UserProfile()
    print("User Name:", user_profile.get_user_name())


# Run Command: python UserProfile.py