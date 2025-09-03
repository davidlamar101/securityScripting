# Calculatoring circle for Diameter and Area

puts "Circle Calculator"
puts "Do you have the radius, circumference, or area? (r/c/a)"
choice = gets.chomp.downcase

pi = Math::PI 

case choice
when "r"
  print "enter the radius: "
  radius = gets.to_f
  diameter = 2 * radius
  area = pi * radius**2
when "c"
  print "Enter the circumference: "
  circumference = gets.to_f
  diameter = circumference / pi
  radius = diameter / 2
  area = pi * radius**2
when "a"
  print "enter the area: "
  area = gets.to_f
  diameter = 2 * Math.sqrt(area / pi)
else
  puts "invalid choice"
  exit
end

puts "\nResults:"
puts "Diameter: #{diameter}"
puts "Area: #{area}"