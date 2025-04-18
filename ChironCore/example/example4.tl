to fact :n
  if (:n == 1) [
    :result = 1 
  ]
  else [
    :temp = :n - 1
    :partial = fact(:temp)
    right 90
    :result = :n * :partial 
  ]
end
:output = fact(7)
forward :output
