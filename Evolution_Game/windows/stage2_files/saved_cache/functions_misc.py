
# misc functions that are used more than once:

class functions:
    def __init__(self, load_settings, save_settings):
        self.load_settings = load_settings
        self.save_settings = save_settings

    def load_settings(self, file_path):
        settings = {}
        try:
            with open(file_path, "r") as file:
                for line in file:
                    if "=" in line:
                        key, value = line.strip().split("=", 1)
                        settings[key] = value
        except FileNotFoundError:
            # Create empty file if missing
            with open(file_path, "w") as f:
                pass
        return settings


    def save_settings(self, settings, file_path):
        with open(file_path, "w") as file:
            for key, value in settings.items():
                file.write(f"{key}={value}\n")
