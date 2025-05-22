
# my stuff
import pieces.chessPiece
from pieces.pieceMove import PieceMove
import ai.ai
import chessBoard

# Pi stuff
import serial
import chess
import time
import logging
import threading
import os

# Old display
import board
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306
import adafruit_gfx


#oled display
i2c = busio.I2C(board.SCL, board.SDA)
display = adafruit_ssd1306.SSD1306_I2C(128, 64, i2c)
image = Image.new("1", (display.width, display.height))
draw = ImageDraw.Draw(image)
font_size = 24
font = ImageFont.load_default()

#global variables
current_move = ""
reset_move = False

#display stuff
def StartGameDisplay():
    display.fill(0)
    display.show()
    draw.text((0, 20), "ready to play", font=font, fill=255)
    draw.text((0, 32), "enter a move", font=font, fill=255)
    display.image(image)
    display.show()

def DisplayText(text):
    draw.rectangle((0, 0, display.width, display.height), outline=0, fill=0)
    draw.text((0, 32), text, font=font, fill=255)
    display.image(image)
    display.show()

def DisplayMove():
    draw.rectangle((0, 0, display.width, display.height), outline=0, fill=0)
    draw.text((0, 0), "Current Move:", font=font, fill=255)
    draw.text((0, 20), current_move, font=font, fill=255)
    display.image(image)
    display.show()

# loggin to text file
logging.basicConfig(
    filename="chess_log.txt",
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
console.setFormatter(formatter)
logging.getLogger().addHandler(console)

#connect to arduino
try:
    arduino = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    time.sleep(2)
    logging.info("✅ Connected to Arduino on /dev/ttyUSB1")
except Exception as e:
    logging.error(f"❌ Could not connect to Arduino: {e}")
    exit()

#initalize game
fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
chessboard = chessBoard.Board.from_fen(fen)
logging.info("✅ Game board initialized.")

#led messages for the arduino
def flash_check(king_square):
    for _ in range(6):
        arduino.write(f"FLASH:{king_square}\n".encode())
        time.sleep(0.5)

def flash_capture(square):
    arduino.write(f"FLASH_CAPTURE:{square}\n".encode())
    time.sleep(0.5)

def show_checkmate(result):
    if result == "ai":
        DisplayText("CHECKMATE: AI WINS")
        arduino.write(b"CHECKMATE:RED\n")
    elif result == "player":
        DisplayText("CHECKMATE: PLAYER WINS")
        arduino.write(b"CHECKMATE:GREEN\n")
    time.sleep(5)
    arduino.write(b"RESET\n")
    chessboard.reset()

#main loop
logging.info("all done, waiting for move")

#message to duisplay
time.sleep(3.0)
DisplayText("HELLO... lets play")

#move accumulation buffer
move_buffer = ""

try:
    while True:
        if arduino.in_waiting:
            raw = arduino.readline()
            logging.debug(f"arduino input: {raw}")

            move_str = raw.decode().strip()
            logging.info(f"recieved: '{move_str}' (current length: {len(move_buffer)})")

            #cancel move
            if move_str == "CANCEL":
                DisplayText("Cancelling Move")
                current_move = ""
                move_buffer = ""
                reset_move = True
                time.sleep(0.1)
                DisplayMove()
                continue

            #reset board
            if move_str == "RESET":
                DisplayText("Resetting")
                chessboard = chessboard.Board()
                time.sleep(3.5)
                DisplayText("Enter a Move")
                continue
                
            #quit -- this has to be lowercase so that the arduino/pi dont get confused
            if move_str == "quit":
                logging.info("quitting")
                DisplayText("goodbye :)")
                arduino.write(b"QUIT\n")
                time.sleep(2.0)
                DisplayText("")
                arduino.close()
                time.sleep(2)
                os.system("sudo shutdown -h now")
                sys.exit()

            #increase buffer until length is 4 eg e2e4
            if len(move_buffer) < 4:
                move_buffer += move_str
                current_move = move_buffer
                DisplayMove()
                continue

            #wait for enter button if length is 4
            if len(move_buffer) == 4:

                logging.info(f"received: {move_buffer}")
                
                #enter button from arduino
                enter_button_pressed = True
                if enter_button_pressed:
                    try:
                        #users move - we can use uci a library in python (chess) to keep better track
                        move = chess.Move.from_uci(move_buffer)

                        #check that the move is legal then push the move
                        if move in chessboard.legal_chess_piece_moves:
                            chessboard.push(move)
                            logging.info(f"player move: {move.uci()}")

                            #use ai to get its move
                            ai_move = ai.AI.get_ai_move(chessboard, [])
                            chessboard.push(ai_move)
                            logging.info(f"ai move: {ai_move}")

                            #check for captures
                            capture_square = ai_move.to_square if chessboard.is_capture(ai_move) else None

                            #send move to arduino
                            reply = ai_move.uci()
                            logging.info(f"ai move: {reply}")
                            DisplayText(f"AI Move: {reply}")
                            arduino.write((reply + "\n").encode())

                            #flash if its a capture
                            if capture_square is not None:
                                square_name = chess.square_name(capture_square)
                                logging.info(f"captured piece: {square_name}")
                                threading.Thread(target=flash_capture, args=(square_name,)).start()

                            #log info
                            logging.info(f"current board:\n{chessboard}")
                            logging.info(f"turn: {'CHESS_PIECE_WHITE' if chessboard.turn == chess.CHESS_PIECE_WHITE else 'CHESS_PIECE_BLACK'}")
                            logging.info(f"is check: {chessboard.is_check()}")
                            logging.info(f"is checkmate: {chessboard.is_checkmate()}")

                            current_move = ""

                            #check for checks and checkmate
                            if chessboard.is_checkmate():
                                winner = "ai" if chessboard.turn != chess.CHESS_PIECE_BLACK else "player"
                                show_checkmate(winner)
                            elif chessboard.is_check():
                                king_square = chessboard.king(chessboard.turn)
                                if king_square is not None:
                                    square_name = chess.square_name(king_square)
                                    threading.Thread(target=flash_check, args=(square_name,)).start()

                        else:
                            #illegal chess_piece_moves
                            logging.warning(f"illegal move received: {move_buffer}")
                            DisplayText("Illegal Move!")
                            arduino.write(b"ILLEGAL\n")
                            time.sleep(0.5)
                            arduino.write(b"0000\n")

                    #errors with parsing
                    except Exception as move_error:
                        logging.error(f"error converting move '{move_buffer}': {move_error}")

                    #reset the buffer from before
                    move_buffer = ""

                else:
                    #wait for enter
                    logging.info("waiting for enter to be pressed")
                    continue

        else:
            time.sleep(0.1)

except KeyboardInterrupt:
    logging.info("exiting")
    DisplayText("goodbye :)")
    arduino.write(b"QUIT\n")
    time.sleep(2.0)
    DisplayText("")
    arduino.close()