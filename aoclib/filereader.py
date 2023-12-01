class FileReader:
    """File reader"""

    def __init__(self, filename):
        self.filename = filename

    def lines(self, func=lambda x: x):
        """Reads each line in file and applies f before returning the result"""
        with open(self.filename, "r", encoding="utf-8") as f:
            for line in f:
                yield func(line.rstrip("\n"))
