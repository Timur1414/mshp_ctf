class BlockElevateImporter:
    def find_spec(self, fullname, path, target=None):
        if fullname == 'elevate':
            raise ImportError("Использование библиотеки 'elevate' запрещено.")
