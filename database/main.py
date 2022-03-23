from setting import session
from board import *

board = Board()
board.title = 'title1'
board.body = 'test body1'
board.writer = 'tester'
board.email = 'test@localhost'
board.password = '1111'

session.add(board)
session.commit()

# query関連の条件指定は参考サイトを参照してください。
boards = session.query(Board).all()
for board in boards:
    print(board.title)