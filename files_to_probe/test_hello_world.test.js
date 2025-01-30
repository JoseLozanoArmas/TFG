const helloWorld = require('./print_hello_world.js');

describe('Hello world function', () => {
  test('should return \"Hello World\"', () => {
    expect(helloWorld()).toBe("Hello World");
  });
});