puts "enter a number"
number = gets.chomp

number = number.gsub("-", "")

digit_count = number.length

puts "#{number} has #{digit_count} digits"
