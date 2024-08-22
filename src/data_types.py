from enum import Enum


class PathType(Enum):
    PATH_TO_STANDARD = 5.2
    PATH_TO_ADVANCED = 5.3
    ADVANCED = 'advanced'
    STANDARD = 'standard'

    def __str__(self):
        if self.value == 5.2:
            return "Standard"
        elif self.value == 5.3:
            return "Advanced"
        elif self.value == 'advanced':
            return "Advanced"
        elif self.value == 'standard':
            return "Standard"
        else:
            return super().__str__()
