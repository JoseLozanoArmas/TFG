def factorial(number)
    result = 1
    (1..number).each do |i|
        result *= i
    end
    result
end

puts factorial(5)