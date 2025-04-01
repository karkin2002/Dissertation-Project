class FileHandler:
    def __init__(self, file_path):
        """
        Constructor to initialize the file path and in-memory content.
        """
        self.file_path = file_path
        self.content = ""

    def load(self):
        """
        Load the content of the file into the `content` attribute.
        """
        try:
            with open(self.file_path, 'r', encoding='utf-8') as file:
                self.content = file.read()
        except FileNotFoundError:
            self.content = ""  # If the file doesn't exist, initialize content as empty.

    def save(self):
        """
        Save the current in-memory `content` to the file.
        """
        with open(self.file_path, 'w', encoding='utf-8') as file:
            file.write(self.content)