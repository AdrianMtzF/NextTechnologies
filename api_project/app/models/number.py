class NumbersSet:
    def __init__(self, n: int = 100):
        #Inicia el conjunto de numeros
        self.n = n
        self.numbers = set(range(1, n + 1))
        self.extracted = None

    def extract(self, number: int):
        if self.extracted is not None:
            raise ValueError("A number has already been extracted, reset the dataset to extract another")
        if number < 1 or number > self.n:
            raise ValueError(f"The number must be between 1 and {self.n}")
        self.numbers.remove(number)
        self.extracted = number

    def find_missing(self) -> int:
        if self.extracted is None:
            raise ValueError("No number has been extracted yet")
        expected_sum = self.n * (self.n + 1) // 2
        current_sum = sum(self.numbers)
        return expected_sum - current_sum


    def reset(self):
        self.numbers = set(range(1, self.n + 1))
        self.extracted = None