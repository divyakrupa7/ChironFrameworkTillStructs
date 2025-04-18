to goleft :c 
 left 90 
 forward :c 
 :result=:c
end 
to goback :d 
 :d=:d+100
 backward :d
 :result=:d
end 
to goright :a 
 right 90
 forward :a 
 :varr=goback(:a)
 :var= goleft(:varr)
 :result=:a
end
:a=100
:va=goright(:a)