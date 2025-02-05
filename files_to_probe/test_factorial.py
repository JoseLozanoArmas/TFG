import unittest
from factorial import factorial

class TestFactorial(unittest.TestCase):
    def test_factorial_of_one(self):
        self.assertEqual(factorial(1), 1)

    def test_factorial_of_five(self):
        self.assertEqual(factorial(5), 120)

    def test_factorial_of_ten(self):
        self.assertEqual(factorial(10), 3628800)

    def test_fail(self):
        self.assertEqual(factorial(10), 2)

if __name__ == "__main__":
    unittest.main()