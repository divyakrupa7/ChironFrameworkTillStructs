struct Point :x :y
end

:p = Point()
:p.x = 100
:p.y = 150

:x = Point()
:x.x = :p.x
:x.y = 150

forward :x.x