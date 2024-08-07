from enum import Enum


class PathType(Enum):
    PATH_TO_STANDARD = 5.2
    PATH_TO_ADVANCED = 5.3
    ADVANCED = 'advanced'
    STANDARD = 'standard'

    def __str__(self):
        if self.value == 5.2:
            return "Path to Standard"
        elif self.value == 5.3:
            return "Path to Advanced"
        elif self.value == 'advanced':
            return "Advanced"
        elif self.value == 'standard':
            return "Standard"
        else:
            return super().__str__()


# Example usage:
print(PathType.PATH_TO_STANDARD)  # Output: Path to Standard
print(PathType.PATH_TO_ADVANCED)  # Output: Path to Advanced
