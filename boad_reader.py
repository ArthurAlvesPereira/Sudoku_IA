archive = open("board_easy", "r")

board = archive.read()
print(board)

board1 = [[0, 0, 0, 0, 0, 0, 0, 0, 0] for i in range(9)]



archive.close()