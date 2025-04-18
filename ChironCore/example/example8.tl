struct Point :x :y
end

struct Robot :name :loc
end

:r = Robot()
:r.loc = Point()
:p=:r.loc
:p.x = 50
:p.y = 60

goto(:p.x, :p.y)
