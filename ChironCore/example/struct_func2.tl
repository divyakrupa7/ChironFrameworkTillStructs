struct Point :x :y
end

to moveTo :pt
  goto(:pt.x, :pt.y)
end

:p = Point()
:p.x = 50
:p.y = 100
:var=moveTo(:p)