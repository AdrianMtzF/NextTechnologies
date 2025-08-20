class NumbersSet:
    def __init__(self, n: int = 100):
        #Inicia el conjunto de numeros
        self.n = n
        self.numbers = set(range(1, n + 1))
        self.extracted = None

    def extract(self, number: int):
        if self.extracted is not None:
            raise ValueError("Ya se extrajo un número, reinicia el conjunto para extraer otro")
        if number < 1 or number > self.n:
            raise ValueError(f"El número debe estar entre 1 y {self.n}")
        self.numbers.remove(number)
        self.extracted = number

    def find_missing(self) -> int:
        if self.extracted is None:
            raise ValueError("No se ha extraído ningún número todavía")
        expected_sum = self.n * (self.n + 1) // 2
        current_sum = sum(self.numbers)
        return expected_sum - current_sum


    def reset(self):
        self.numbers = set(range(1, self.n + 1))
        self.extracted = None