from enum import Enum


class ImpactClass(Enum):
    YELLOW = 'icon--ff-impact-yel'
    ORANGE = 'icon--ff-impact-ora'
    RED = 'icon--ff-impact-red'
    GRAY = 'icon--ff-impact-gra'

    @staticmethod
    def from_text(text):
        if text is None:
            raise ValueError("Input text cannot be None")
        text = text.strip().lower()
        mapping = {
            'yellow': ImpactClass.YELLOW,
            'orange': ImpactClass.ORANGE,
            'red': ImpactClass.RED,
            'gray': ImpactClass.GRAY,
            'icon--ff-impact-yel': ImpactClass.YELLOW,
            'icon--ff-impact-ora': ImpactClass.ORANGE,
            'icon--ff-impact-red': ImpactClass.RED,
            'icon--ff-impact-gra': ImpactClass.GRAY,
        }
        if text not in mapping:
            raise ValueError(f"Invalid text for ImpactClass: '{text}'")
        return mapping[text]

    @staticmethod
    def to_text(enum_value):
        reverse_mapping = {
            ImpactClass.YELLOW: 'yellow',
            ImpactClass.ORANGE: 'orange',
            ImpactClass.RED: 'red',
            ImpactClass.GRAY: 'gray'
        }
        if enum_value not in reverse_mapping:
            raise ValueError(f"Invalid ImpactClass value: '{enum_value}'")
        return reverse_mapping[enum_value]

# Example usage
# try:
#     print(ImpactClass.from_text(' Yellow '))  # Output: ImpactClass.YELLOW
#     print(ImpactClass.from_text('RED'))       # Output: ImpactClass.RED
#     print(ImpactClass.from_text('blue'))      # Raises ValueError: Invalid text for ImpactClass: 'blue'
# except ValueError as e:
#     print(e)

# print(ImpactClass.to_text(ImpactClass.RED))  # Output: 'red'

# try:
#     print(ImpactClass.to_text("BLUE"))       # Raises ValueError: Invalid ImpactClass value: 'BLUE'
# except ValueError as e:
#     print(e)
