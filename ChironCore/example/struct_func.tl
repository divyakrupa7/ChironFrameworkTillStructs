to makestruct :a :b
 :p = Point()
 :p.x = :a
 :p.y = :b
 goto(:p.x,:p.y)
end
struct Point :x :y
end
:var=makestruct(50,70)