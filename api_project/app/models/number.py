class NumbersSet:
    def __init__(self, n: int = 100):
        #Inicia el conjunto de numeros
        self.n = n
        self.numbers = set(range(1, n + 1))
        self.extracted = None

    def extract(self, number: int):
        #Extrae el numero faltante
        if number < 1 or number > self.n:
            raise ValueError(f"El número debe estar entre 1 y {self.n}")
        if number not in self.numbers:
            raise ValueError("El número ya fue extraído o no existe en el conjunto")
        self.numbers.remove(number)
        self.extracted = number

    def find_missing(self) -> int:
        #Calcula el numero faltante con sumas
        expected_sum = self.n * (self.n + 1) // 2
        current_sum = sum(self.numbers)
        return expected_sum - current_sum
