from PIL import Image
def broad(im):
	f = open("_board.txt","w")
	broad = []
	im_pixel = im.load()
	for i in range(9):
		line = []
		for j in range(9-abs(-i+4)):
			if im_pixel[85 + 35 * abs(4 - i) + 70 * j,290 + 60 * i] == (77, 77, 75, 255):
				line.append(0)
				f.write("0")
			else:
				line.append(1)
				f.write("1")
		broad.append(line)
	f.close();
	return broad


def piece(im):
	f = open("_piece.txt","w")
	im_pixel = im.load()
	color = {
				"A": (137, 140, 255, 255),
				"B": (207, 243, 129, 255),
				"C": (245, 162, 111, 255),
				"D": (255, 220, 137, 255),
				"E": (255, 137, 181, 255),
				"F": (113, 224, 150, 255)
			}
	piece = []
	for i in range(3):
		piece_pixel = im.crop((29 + i * 221,810,229 + i * 221,1010)).load()

		# piecef = im.crop((29 + i * 221,810,229 + i * 221,1010))
		# piecef.save(str(i) + "p.png")

		if piece_pixel[105, 78] == color["A"]:
			piece.append("A0")
			f.write("a")

		elif piece_pixel[105, 20] == color["B"]:
			piece.append("B0")
			f.write("b")
		elif piece_pixel[162, 77] == color["B"]:
			piece.append("B1")
			f.write("c")
		elif piece_pixel[45, 77] == color["B"]:
			piece.append("B2")
			f.write("d")

		elif piece_pixel[170,30] == color["C"]:
			piece.append("C5")
			f.write("j")
		elif piece_pixel[43,31] == color["C"]:
			piece.append("C4")
			f.write("i")	
		elif piece_pixel[153,31] == color["C"]:
			piece.append("C1")
			f.write("f")
		elif piece_pixel[72,30] == color["C"]:
			piece.append("C3")
			f.write("h")
		elif piece_pixel[137,30] == color["C"]:
			piece.append("C2")
			f.write("g")
		elif piece_pixel[80,123] == color["C"]:
			piece.append("C0")
			f.write("e")

		elif piece_pixel[43, 29] == color["D"]:
			piece.append("D0")
			f.write("k")
		elif piece_pixel[163, 121] == color["D"]:
			piece.append("D1")
			f.write("l")
		elif piece_pixel[72, 124] == color["D"] and piece_pixel[82, 31] == color["D"]:
			piece.append("D2")
			f.write("m")
		elif piece_pixel[176, 75] == color["D"] and piece_pixel[131, 31] == color["D"]:
			piece.append("D3")
			f.write("n")
		elif piece_pixel[72, 124] == color["D"]:
			piece.append("D4")
			f.write("o")

		elif piece_pixel[61, 129] == color["E"]:
			piece.append("E2")
			f.write("r")
		elif piece_pixel[169, 32] == color["E"]:
			piece.append("E4")
			f.write("t")
		elif piece_pixel[147, 30] == color["E"]:
			piece.append("E3")
			f.write("s")
		elif piece_pixel[134, 123] == color["E"]:
			piece.append("E1")
			f.write("q")	
		elif piece_pixel[81, 30] == color["E"]:
			piece.append("E0")
			f.write("p")		
		
		elif piece_pixel[11, 77] == color["F"]:
			piece.append("F0")
			f.write("u")
		elif piece_pixel[151, 19] == color["F"]:
			piece.append("F1")
			f.write("v")
		elif piece_pixel[58, 19] == color["F"]:
			piece.append("F2")
			f.write("w")
	return piece