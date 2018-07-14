import subprocess
def move_piece(pieceID, piece, place)
	i, j = place

	sx = 29 + piece * 221 + offset_x
	sy = 810 + offset_y
	
	ex = 85 + 35 * abs(4 - i) + 70 * j
	ey = 290 + 60 * i

	cmd = 'adb shell input swipe {sx} {sy} {ex} {ey} 400'
	subprocess.call(cmd)

