from enum import Enum


class Currencies(Enum):
    AUD = 'AUD'
    CAD = 'CAD'
    CHF = 'CHF'
    EUR = 'EUR'
    GBP = 'GBP'
    JPY = 'JPY'
    NZD = 'NZD'
    USD = 'USD'

    @staticmethod
    def from_text(text):
        if text is None:
            raise ValueError("Input text cannot be None")
        text = text.strip().upper()
        mapping = {
            'AUD': Currencies.AUD,
            'CAD': Currencies.CAD,
            'CHF': Currencies.CHF,
            'EUR': Currencies.EUR,
            'GBP': Currencies.GBP,
            'JPY': Currencies.JPY,
            'NZD': Currencies.NZD,
            'USD': Currencies.USD
        }
        if text not in mapping:
            raise ValueError(f"Invalid text for Currencies: '{text}'")
        return mapping[text]

    @staticmethod
    def to_text(enum_value):
        reverse_mapping = {
            Currencies.AUD: 'AUD',
            Currencies.CAD: 'CAD',
            Currencies.CHF: 'CHF',
            Currencies.EUR: 'EUR',
            Currencies.GBP: 'GBP',
            Currencies.JPY: 'JPY',
            Currencies.NZD: 'NZD',
            Currencies.USD: 'USD'
        }
        if enum_value not in reverse_mapping:
            raise ValueError(f"Invalid Currencies value: '{enum_value}'")
        return reverse_mapping[enum_value]


# Example usage
# try:
#     print(Currencies.from_text(' aud '))  # Output: Currencies.AUD
#     print(Currencies.from_text('USD'))    # Output: Currencies.USD
#     # Raises ValueError: Invalid text for Currencies: 'inr'
#     print(Currencies.from_text('inr'))
# except ValueError as e:
#     print(e)

# print(Currencies.to_text(Currencies.EUR))  # Output: 'EUR'

# try:
#     # Raises ValueError: Invalid Currencies value: 'INR'
#     print(Currencies.to_text("INR"))
# except ValueError as e:
#     print(e)
