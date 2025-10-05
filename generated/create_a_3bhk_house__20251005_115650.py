import FreeCAD, Part, FreeCADGui
doc = FreeCAD.newDocument("Professional_Model")
# Ground Floor
ground_floor = doc.addObject("Part::Box","Ground_Floor")
ground_floor.Length = 15000
ground_floor.Width = 12000
ground_floor.Height = 100
# Parking
parking = doc.addObject("Part::Box","Parking")
parking.Length = 6000
parking.Width = 4000
parking.Height = 2500
parking.Placement = FreeCAD.Placement(FreeCAD.Vector(0, -5000, 0), FreeCAD.Rotation(0, 0, 0))
# Living Room Floor
living_room_floor = doc.addObject("Part::Box","Living_Room_Floor")
living_room_floor.Length = 8000
living_room_floor.Width = 6000
living_room_floor.Height = 100
living_room_floor.Placement = FreeCAD.Placement(FreeCAD.Vector(0, 0, 2500), FreeCAD.Rotation(0, 0, 0))
# Living Room Walls
living_room_wall1 = doc.addObject("Part::Box","Living_Room_Wall1")
living_room_wall1.Length = 8000
living_room_wall1.Width = 200
living_room_wall1.Height = 2500
living_room_wall1.Placement = FreeCAD.Placement(FreeCAD.Vector(-4000, 0, 2500), FreeCAD.Rotation(0, 0, 0))
living_room_wall2 = doc.addObject("Part::Box","Living_Room_Wall2")
living_room_wall2.Length = 8000
living_room_wall2.Width = 200
living_room_wall2.Height = 2500
living_room_wall2.Placement = FreeCAD.Placement(FreeCAD.Vector(4000, 0, 2500), FreeCAD.Rotation(0, 0, 0))
living_room_wall3 = doc.addObject("Part::Box","Living_Room_Wall3")
living_room_wall3.Length = 200
living_room_wall3.Width = 6000
living_room_wall3.Height = 2500
living_room_wall3.Placement = FreeCAD.Placement(FreeCAD.Vector(0, -3000, 2500), FreeCAD.Rotation(0, 0, 0))
living_room_wall4 = doc.addObject("Part::Box","Living_Room_Wall4")
living_room_wall4.Length = 200
living_room_wall4.Width = 6000
living_room_wall4.Height = 2500
living_room_wall4.Placement = FreeCAD.Placement(FreeCAD.Vector(0, 3000, 2500), FreeCAD.Rotation(0, 0, 0))
# Living Room Windows
living_room_window1 = doc.addObject("Part::Box","Living_Room_Window1")
living_room_window1.Length = 2000
living_room_window1.Width = 1000
living_room_window1.Height = 100
living_room_window1.Placement = FreeCAD.Placement(FreeCAD.Vector(-3500, 0, 2800), FreeCAD.Rotation(0, 0, 0))
living_room_window2 = doc.addObject("Part::Box","Living_Room_Window2")
living_room_window2.Length = 2000
living_room_window2.Width = 1000
living_room_window2.Height = 100
living_room_window2.Placement = FreeCAD.Placement(FreeCAD.Vector(1500, 0, 2800), FreeCAD.Rotation(0, 0, 0))
# Living Room Door
living_room_door = doc.addObject("Part::Box","Living_Room_Door")
living_room_door.Length = 1000
living_room_door.Width = 200
living_room_door.Height = 2000
living_room_door.Placement = FreeCAD.Placement(FreeCAD.Vector(0, 3000, 2500), FreeCAD.Rotation(0, 0, 0))
# Kitchen Floor
kitchen_floor = doc.addObject("Part::Box","Kitchen_Floor")
kitchen_floor.Length = 4000
kitchen_floor.Width = 3000
kitchen_floor.Height = 100
kitchen_floor.Placement = FreeCAD.Placement(FreeCAD.Vector(5000, 0, 2500), FreeCAD.Rotation(0, 0, 0))
# Kitchen Walls
kitchen_wall1 = doc.addObject("Part::Box","Kitchen_Wall1")
kitchen_wall1.Length = 4000
kitchen_wall1.Width = 200
kitchen_wall1.Height = 2500
kitchen_wall1.Placement = FreeCAD.Placement(FreeCAD.Vector(7000, 0, 2500), FreeCAD.Rotation(0, 0, 0))
kitchen_wall2 = doc.addObject("Part::Box","Kitchen_Wall2")
kitchen_wall2.Length = 4000
kitchen_wall2.Width = 200
kitchen_wall2.Height = 2500
kitchen_wall2.Placement = FreeCAD.Placement(FreeCAD.Vector(3000, 0, 2500), FreeCAD.Rotation(0, 0, 0))
kitchen_wall3 = doc.addObject("Part::Box","Kitchen_Wall3")
kitchen_wall3.Length = 200
kitchen_wall3.Width = 3000
kitchen_wall3.Height = 2500
kitchen_wall3.Placement = FreeCAD.Placement(FreeCAD.Vector(5000, -1500, 2500), FreeCAD.Rotation(0, 0, 0))
kitchen_wall4 = doc.addObject("Part::Box","Kitchen_Wall4")
kitchen_wall4.Length = 200
kitchen_wall4.Width = 3000
kitchen_wall4.Height = 2500
kitchen_wall4.Placement = FreeCAD.Placement(FreeCAD.Vector(5000, 1500, 2500), FreeCAD.Rotation(0, 0, 0))
# Kitchen Windows
kitchen_window1 = doc.addObject("Part::Box","Kitchen_Window1")
kitchen_window1.Length = 1500
kitchen_window1.Width = 1000
kitchen_window1.Height = 100
kitchen_window1.Placement = FreeCAD.Placement(FreeCAD.Vector(5500, 0, 2800), FreeCAD.Rotation(0, 0, 0))
# Kitchen Door
kitchen_door = doc.addObject("Part::Box","Kitchen_Door")
kitchen_door.Length = 1000
kitchen_door.Width = 200
kitchen_door.Height = 2000
kitchen_door.Placement = FreeCAD.Placement(FreeCAD.Vector(5000, 1500, 2500), FreeCAD.Rotation(0, 0, 0))
# Bedroom 1 Floor
bedroom1_floor = doc.addObject("Part::Box","Bedroom1_Floor")
bedroom1_floor.Length = 4000
bedroom1_floor.Width = 3000
bedroom1_floor.Height = 100
bedroom1_floor.Placement = FreeCAD.Placement(FreeCAD.Vector(-5000, 0, 2500), FreeCAD.Rotation(0, 0, 0))
# Bedroom 1 Walls
bedroom1_wall1 = doc.addObject("Part::Box","Bedroom1_Wall1")
bedroom1_wall1.Length = 4000
bedroom1_wall1.Width = 200
bedroom1_wall1.Height = 2500
bedroom1_wall1.Placement = FreeCAD.Placement(FreeCAD.Vector(-7000, 0, 2500), FreeCAD.Rotation(0, 0, 0))
bedroom1_wall2 = doc.addObject("Part::Box","Bedroom1_Wall2")
bedroom1_wall2.Length = 4000
bedroom1_wall2.Width = 200
bedroom1_wall2.Height = 2500
bedroom1_wall2.Placement = FreeCAD.Placement(FreeCAD.Vector(-3000, 0, 2500), FreeCAD.Rotation(0, 0, 0))
bedroom1_wall3 = doc.addObject("Part::Box","Bedroom1_Wall3")
bedroom1_wall3.Length = 200
bedroom1_wall3.Width = 3000
bedroom1_wall3.Height = 2500
bedroom1_wall3.Placement = FreeCAD.Placement(FreeCAD.Vector(-5000, -1500, 2500), FreeCAD.Rotation(0, 0, 0))
bedroom1_wall4 = doc.addObject("Part::Box","Bedroom1_Wall4")
bedroom1_wall4.Length = 200
bedroom1_wall4.Width = 3000
bedroom1_wall4.Height = 2500
bedroom1_wall4.Placement = FreeCAD.Placement(FreeCAD.Vector(-5000, 1500, 2500), FreeCAD.Rotation(0, 0, 0))
# Bedroom 1 Windows
bedroom1_window1 = doc.addObject("Part::Box","Bedroom1_Window1")
bedroom1_window1.Length = 1500
bedroom1_window1.Width = 1000
bedroom1_window1.Height = 100
bedroom1_window1.Placement = FreeCAD.Placement(FreeCAD.Vector(-4500, 0, 2800), FreeCAD.Rotation(0, 0, 0))
# Bedroom 1 Door
bedroom1_door = doc.addObject("Part::Box","Bedroom1_Door")
bedroom1_door.Length = 1000
bedroom1_door.Width = 200
bedroom1_door.Height = 2000
bedroom1_door.Placement = FreeCAD.Placement(FreeCAD.Vector(-5000, 1500, 2500), FreeCAD.Rotation(0, 0, 0))
# Bedroom 2 Floor
bedroom2_floor = doc.addObject("Part::Box","Bedroom2_Floor")
bedroom2_floor.Length = 4000
bedroom2_floor.Width = 3000
bedroom2_floor.Height = 100
bedroom2_floor.Placement = FreeCAD.Placement(FreeCAD.Vector(-5000, 0, 5000), FreeCAD.Rotation(0, 0, 0))
# Bedroom 2 Walls
bedroom2_wall1 = doc.addObject("Part::Box","Bedroom2_Wall1")
bedroom2_wall1.Length = 4000
bedroom2_wall1.Width = 200
bedroom2_wall1.Height = 2500
bedroom2_wall1.Placement = FreeCAD.Placement(FreeCAD.Vector(-7000, 0, 5000), FreeCAD.Rotation(0, 0, 0))
bedroom2_wall2 = doc.addObject("Part::Box","Bedroom2_Wall2")
bedroom2_wall2.Length = 4000
bedroom2_wall2.Width = 200
bedroom2_wall2.Height = 2500
bedroom2_wall2.Placement = FreeCAD.Placement(FreeCAD.Vector(-3000, 0, 5000), FreeCAD.Rotation(0, 0, 0))
bedroom2_wall3 = doc.addObject("Part::Box","Bedroom2_Wall3")
bedroom2_wall3.Length = 200
bedroom2_wall3.Width = 3000
bedroom2_wall3.Height = 2500
bedroom2_wall3.Placement = FreeCAD.Placement(FreeCAD.Vector(-5000, -1500, 5000), FreeCAD.Rotation(0, 0, 0))
bedroom2_wall4 = doc.addObject("Part::Box","Bedroom2_Wall4")
bedroom2_wall4.Length = 200
bedroom2_wall4.Width = 3000
bedroom2_wall4.Height = 2500
bedroom2_wall4.Placement = FreeCAD.Placement(FreeCAD.Vector(-5000, 1500, 5000), FreeCAD.Rotation(0, 0, 0))
# Bedroom 2 Windows
bedroom2_window1 = doc.addObject("Part::Box","Bedroom2_Window1")
bedroom2_window1.Length = 1500
bedroom2_window1.Width = 1000
bedroom2_window1.Height = 100
bedroom2_window1.Placement = FreeCAD.Placement(FreeCAD.Vector(-4500, 0, 5300), FreeCAD.Rotation(0, 0, 0))
# Bedroom 2 Door
bedroom2_door = doc.addObject("Part::Box","Bedroom2_Door")
bedroom2_door.Length = 1000
bedroom2_door.Width = 200
bedroom2_door.Height = 2000
bedroom2_door.Placement = FreeCAD.Placement(FreeCAD.Vector(-5000, 1500, 5000), FreeCAD.Rotation(0, 0, 0))
# Bedroom 3 Floor
bedroom3_floor = doc.addObject("Part::Box","Bedroom3_Floor")
bedroom3_floor.Length = 4000
bedroom3_floor.Width = 3000
bedroom3_floor.Height = 100
bedroom3_floor.Placement = FreeCAD.Placement(FreeCAD.Vector(5000, 0, 5000), FreeCAD.Rotation(0, 0, 0))
# Bedroom 3 Walls
bedroom3_wall1 = doc.addObject("Part::Box","Bedroom3_Wall1")
bedroom3_wall1.Length = 4000
bedroom3_wall1.Width = 200
bedroom3_wall1.Height = 2500
bedroom3_wall1.Placement = FreeCAD.Placement(FreeCAD.Vector(7000, 0, 5000), FreeCAD.Rotation(0, 0, 0))
bedroom3_wall2 = doc.addObject("Part::Box","Bedroom3_Wall2")
bedroom3_wall2.Length = 4000
bedroom3_wall2.Width = 200
bedroom3_wall2.Height = 2500
bedroom3_wall2.Placement = FreeCAD.Placement(FreeCAD.Vector(3000, 0, 5000), FreeCAD.Rotation(0, 0, 0))
bedroom3_wall3 = doc.addObject("Part::Box","Bedroom3_Wall3")
bedroom3_wall3.Length = 200
bedroom3_wall3.Width = 3000
bedroom3_wall3.Height = 2500
bedroom3_wall3.Placement = FreeCAD.Placement(FreeCAD.Vector(5000, -1500, 5000), FreeCAD.Rotation(0, 0, 0))
bedroom3_wall4 = doc.addObject("Part::Box","Bedroom3_Wall4")
bedroom3_wall4.Length = 200
bedroom3_wall4.Width = 3000
bedroom3_wall4.Height = 2500
bedroom3_wall4.Placement = FreeCAD.Placement(FreeCAD.Vector(5000, 1500, 5000), FreeCAD.Rotation(0, 0, 0))
# Bedroom 3 Windows
bedroom3_window1 = doc.addObject("Part::Box","Bedroom3_Window1")
bedroom3_window1.Length = 1500
bedroom3_window1.Width = 1000
bedroom3_window1.Height = 100
bedroom3_window1.Placement = FreeCAD.Placement(FreeCAD.Vector(5500, 0, 5300), FreeCAD.Rotation(0, 0, 0))
# Bedroom 3 Door
bedroom3_door = doc.addObject("Part::Box","Bedroom3_Door")
bedroom3_door.Length = 1000
bedroom3_door.Width = 200
bedroom3_door.Height = 2000
bedroom3_door.Placement = FreeCAD.Placement(FreeCAD.Vector(5000, 1500, 5000), FreeCAD.Rotation(0, 0, 0))
# Balcony
balcony = doc.addObject("Part::Box","Balcony")
balcony.Length = 4000
balcony.Width = 2000
balcony.Height = 100
balcony.Placement = FreeCAD.Placement(FreeCAD.Vector(5000, 0, 5000), FreeCAD.Rotation(0, 0, 0))
# Balcony Door
balcony_door = doc.addObject("Part::Box","Balcony_Door")
balcony_door.Length = 1000
balcony_door.Width = 200
balcony_door.Height = 2000
balcony_door.Placement = FreeCAD.Placement(FreeCAD.Vector(5000, 1500, 5000), FreeCAD.Rotation(0, 0, 0))