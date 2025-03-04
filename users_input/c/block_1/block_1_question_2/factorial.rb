def factorial(number)
    result = 1
    (1..number).each do |i|
        result *= i
    end
    result
end

def process_file(filename)
    begin
        File.readlines(filename).each do |line|
            num = line.strip.to_i
            if line.strip.match?(/^\d+$/)
                puts "#{factorial(num)}"
            else
                puts "Error: '#{line.strip}' no es un número entero válido."
            end
        end
    rescue Errno::ENOENT
        puts "Error: El archivo no existe."
    rescue => e
        puts "Error inesperado: #{e.message}"
    end
end

if ARGV.length != 1
    puts "Uso: ruby script.rb <archivo>"
    exit
end

process_file(ARGV[0])