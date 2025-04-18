struct Point :x :y
end

to makePoint :a :b
  :p = Point()
  :p.x = :a
  :p.y = :b
  :result = :p
end

:mypt = makePoint(50, 200)
goto(:mypt.x, :mypt.y)
forward :mypt.x