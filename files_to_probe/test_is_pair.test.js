const isPair = require('./is_pair.js');

describe('isPair function', () => {
  test('should return true for even numbers', () => {
    expect(isPair(4)).toBe(true);
    expect(isPair(2)).toBe(true);
    expect(isPair(0)).toBe(true);
    expect(isPair(-2)).toBe(true);
  });

  test('should return false for odd numbers', () => {
    expect(isPair(7)).toBe(false);
    expect(isPair(3)).toBe(false);
    expect(isPair(1)).toBe(false);
    expect(isPair(-1)).toBe(false);
  });
});
