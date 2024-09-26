import json

class Config_Manager:
    # Singleton pattern to ensure only one instance handles configuration data
    singleton_instance = None
    data = None

    def __new__(cls, *args, **kwargs):
        # Check if an instance already exists
        if cls.singleton_instance is None:
            # Create a new instance if it does not exist
            cls.singleton_instance = super(Config_Manager, cls).__new__(cls, *args, **kwargs)
        return cls.singleton_instance

    def load(self, file):
        # Load configuration data from file if not already loaded
        if self.data is None:
            # Open the file and load its JSON content into the 'data' attribute
            with open(file) as f:
                self.data = json.load(f)
        return self.data