import subprocess
from operator import itemgetter
import loadData, movePiece
from PIL import Image
import time

check_direction = {
	"A0": (),
	"B0": (2,4,2), "B1": (1,3,4), "B2": (1,2,4),
	"C0": (2,1,6), "C1": (6,1,2), "C2": (1,6,5), "C3": (3,2,1), "C4": (1,2,3), "C5": (4,3,2),
	"D0": (2,2,6), "D1": (6,2,2), "D2": (1,3,3), "D3": (1,1,5), "D4": (2,6,1),
	"E0": (6,2,1), "E1": (1,1,3), "E2": (2,4,3), "E3": (1,3,2), "E4": (2,6,6),
	"F0": (1,1,1), "F1": (3,3,3), "F2": (2,2,2)
}

def sort_solution():
	pass
	
def copy_broad(broad):
	return [k.copy() for k in broad]

def rotate_broad(broad):
	rbroad = copy_broad(broad)
	rstart = [(4,0),(5,0),(6,0),(7,0),(8,0),(8,1),(8,2),(8,3),(8,4),(8,5)]
	for i in range(9):
		bi,bj = rstart[i]
		for j in range(9-abs(-i+4)):
			rbroad[i][j] = broad[bi][bj]
			bi,bj = go_direction(bi,bj,6)
	return rbroad


def check_broad(broad, piece):
	solution = []
	for i in range(9):
		for j in range(9-abs(-i+4)):
			if not broad[i][j]:
				bi, bj = i, j
				flag = True
				for d in check_direction[piece]:
					bi,bj = go_direction(bi,bj,d)
					if (bi < 0) or (bi >= 9) or (bj < 0) or (bj >= 9-abs(-bi+4)):
						flag = False
						continue
					if broad[bi][bj]:
						flag = False
						continue
				if flag:
					solution.append((i,j))
	return solution

def go_direction(bi,bj,d):
	if d == 1:
		return (bi,bj+1)
	elif d == 4:
		return (bi,bj-1)
	elif d == 2:
		if bi < 4:
			return (bi+1, bj+1)
		else:
			return (bi+1, bj)
	elif d == 3:
		if bi < 4:
			return (bi+1, bj)
		else:
			return (bi+1, bj-1)
	elif d == 5:
		if bi <= 4:
			return (bi-1, bj-1)
		else:
			return (bi-1, bj)
	elif d == 6:
		if bi <= 4:
			return (bi-1, bj)
		else:
			return (bi-1, bj+1) 


def screenshot(filename):
	subprocess.call('adb shell screencap -p /sdcard/' + filename)
	subprocess.call('adb pull /sdcard/' + filename)

def display_broad(broad):
	for i in range(9):
		for j in range(abs(4 - i)):
			print(" ",end = "")
		for j in range(9-abs(-i+4)):
			if broad[i][j] == 1:
				print("x",end = " ")
			elif broad[i][j] == 0:
				print("-",end = " ")
			elif broad[i][j] == 2:
				print("o",end = " ")
			elif broad[i][j] == 3:
				print("~",end = " ")
		print("");
	print("")

def place_piece(broad, piece, pos):
	i, j = pos
	rbroad = copy_broad(broad)
	rbroad[i][j] = 2
	for d in check_direction[piece]:
		i, j = go_direction(i,j,d)
		rbroad[i][j] = 2
	return rbroad

def count_line(line):
	count = 0
	for i in line:
		if i != 0:
			count += 1
	return count

def check_line(broad):
	line_count = 0
	hexagon_count = 0
	hexagon_before = sum([count_line(line) for line in broad])
	for rotate_i in range(3):
		for line in broad:
			line_flag = True
			for hexagon in line:
				if hexagon == 0:
					line_flag = False
					break;
			if line_flag:
				hexagon_count += len(line)
				line_count += 1
				for i in range(len(line)):
					line[i] = 3
		broad = rotate_broad(broad)

	rbroad = copy_broad(broad)
	for line in rbroad:
		line.reverse()
	rbroad.reverse()
	for line in rbroad:
		for i in range(len(line)):
			if line[i] == 3:
				line[i] = 0
			elif line[i] == 2:
				line[i] = 1
	hexagon_after = sum([sum(line) for line in rbroad])
	hexagon_count = hexagon_before - hexagon_after
	return line_count,hexagon_count,rbroad

def next_way(broad, piece):
	way = 0
	way_score = 0
	for p in piece:
		solution = check_broad(broad,p)
		for s in solution:
			new_broad = place_piece(broad, p, s)
			clear_line, clear_hexagon, rbroad = check_line(new_broad)
			if clear_hexagon > way_score:
				way_score = clear_hexagon
		way += len(solution)
	return way,way_score

if __name__ == "__main__":
	while True:
		pass
		# screenshot("af.png")
		# subprocess.call("adb shell input swipe 360 1080 360 1080 300")
		im = Image.open('./af.png')
		broad = loadData.broad(im)
		# display_broad(broad)
		piece = loadData.piece(im)
		subprocess.call("hexagon -e")
		time.sleep(30)
		'''	
		print(piece)
		data = []
		for pi in range(len(piece)):
			solution = check_broad(broad,piece[pi])
			for s in solution:
				other2piece = [piece[i] for i in range(3) if i != pi]
				new_broad = place_piece(broad, piece[pi], s)
				clear_line, clear_hexagon, rbroad = check_line(new_broad)
				way,way_score = next_way(rbroad,other2piece)

				data.append({"pieceID": piece[pi],
							 "piece": pi,
							 "place": s,
							 "clear line": clear_line,
							 "clear hexagon": clear_hexagon,
							 "next_way":way,
							 "way_score":way_score,
							 "score":(clear_hexagon + way  * 0.2 + way_score)})
		data = sorted(data, key=itemgetter('score'), reverse=True)

		# movePiece.move_piece(data[0]["pieceID"], data[0]["piece"], data[0]["place"])
		
		for i in range(3):
			try:
				if i == 0:
					display_broad(place_piece(broad, data[i]["pieceID"], data[i]["place"]))
			except:
				pass
		screenshot("hexagon.png")
		'''