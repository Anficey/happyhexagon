import subprocess
def move_piece(pieceID, piece, place):
	i, j = place
	# offset = {
	# 	"A0": (107, 77),
	# 	"B0": (104, 32), "B1": (92, 76), "B2": (62,77),
	# 	"C0": (55, 79), "C1": (51, 78), "C2": (65, 125), "C3": (93, 29), "C4": (66, 30), "C5": (144, 28),
	# 	"D0": (65, 31), "D1": (67, 77), "D2": (79, 32), "D3": (54, 78), "D4": (52, 76),
	# 	"E0": (55, 75), "E1": (52, 75), "E2": (119, 32), "E3": (80, 31), "E4": (66, 74),
	# 	"F0": (25, 78), "F1": (148, 28), "F2": (65, 31)
	# }
	e_offset = {
		"A0": (0 , 20),
		"B2": (0, 0),
		"C1": (70, 80),
		"D0": (30, 150),
		"F0": (10 , 10), "F1": (0, 0), "F2": (20, 40)
	}
	# offset_x = offset[pieceID][0]
	# offset_y = offset[pieceID][1]

	sx = 29 + piece * 221 + 100
	sy = 810 + 100
	
	e_offset_x = e_offset[pieceID][0]
	e_offset_y = e_offset[pieceID][1]

	ex = 85 + 35 * abs(4 - i) + 70 * j + e_offset_x
	ey = 290 + 60 * i  + e_offset_y

	press_time = 2000

	cmd = 'adb shell input swipe {sx} {sy} {ex} {ey} {duration}'.format(
        sx=sx,
        sy=sy,
        ex=ex,
        ey=ey,
        duration=press_time
    )
	subprocess.call(cmd)

