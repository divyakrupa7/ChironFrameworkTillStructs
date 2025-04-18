to square :len :n
 if :n > 0 [
    forward :len
    right 90
    :var=square(:len, :n - 1) 
]
:var=200
:result=:var
end

:sidelength = 100
:sides = 4
:va=square(:sidelength, :sides)