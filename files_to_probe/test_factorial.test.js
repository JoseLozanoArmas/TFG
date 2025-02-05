const factorial = require('./factorial.js');

describe('factorial', () => {
  test('Works for positive numbers', () => {
    expect(factorial(1)).toBe(1);
    expect(factorial(5)).toBe(120);
    expect(factorial(10)).toBe(3628800);
  });

  test('Returns -1 if the number is less or equal to 0', () => {
    expect(factorial(0)).toBe(-1);
    expect(factorial(-5)).toBe(-1);
    expect(factorial(-10)).toBe(-1);
  });
});

describe('factorial', () => {
  test('Works for positive numbers', () => {
    expect(factorial(1)).toBe(1);
    expect(factorial(5)).toBe(120);
    expect(factorial(10)).toBe(3628800);
  });

  test('Returns -1 if the number is less or equal to 0', () => {
    expect(factorial(0)).toBe(-1);
    expect(factorial(-5)).toBe(-1);
    expect(factorial(-10)).toBe(-1);
  });
});