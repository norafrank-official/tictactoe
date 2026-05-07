import cv2
from cvzone.HandTrackingModule import HandDetector
import serial
import time

# Initialize the camera and hand detector
cap = cv2.VideoCapture(0)
detector = HandDetector(detectionCon=0.8, maxHands=2)

# Define the positions for the 9 circles in a 3x3 grid
positions = [(x, y) for y in range(100, 600, 200) for x in range(100, 600, 200)]
game_board = [''] * 9  # Empty game board

# Initialize scores
score_X = 0
score_O = 0

# Initialize turn variable
turn = 'Left'  # Start with the left hand

# Initialize serial communication
ser = serial.Serial('COM6', 9600)  # Replace 'COM3' with your Arduino port
time.sleep(2)  # Wait for the serial connection to initialize

def check_winner(board):
    # Define winning combinations
    winning_combinations = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
        [0, 4, 8], [2, 4, 6]              # Diagonals
    ]
    for combo in winning_combinations:
        if board[combo[0]] == board[combo[1]] == board[combo[2]] and board[combo[0]] != '':
            return board[combo[0]]
    return None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Resize the frame to ensure all circles fit within the window
    frame = cv2.resize(frame, (800, 800))

    # Detect hands
    hands, frame = detector.findHands(frame, flipType=False)  # Do not mirror the video

    # Draw the circles and the game board
    for i, (px, py) in enumerate(positions):
        cv2.circle(frame, (px, py), 40, (255, 255, 255), 2)
        if game_board[i] == 'X':
            cv2.putText(frame, 'X', (px - 20, py + 20), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)
        elif game_board[i] == 'O':
            cv2.putText(frame, 'O', (px - 20, py + 20), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 0, 0), 5)

    # Check for hand gestures
    if hands:
        for hand in hands:
            lmList = hand['lmList']
            handType = hand['type']
            for i, (px, py) in enumerate(positions):
                if lmList[8][0] in range(px - 40, px + 40) and lmList[8][1] in range(py - 40, py + 40):
                    if handType == turn and game_board[i] == '':
                        if turn == 'Left':
                            game_board[i] = 'X'
                            turn = 'Right'  # Switch turn to right hand
                            ser.write(b'X')  # Send 'X' to Arduino
                        elif turn == 'Right':
                            game_board[i] = 'O'
                            turn = 'Left'  # Switch turn to left hand
                            ser.write(b'O')  # Send 'O' to Arduino

    # Check for a winner
    winner = check_winner(game_board)
    if winner:
        if winner == 'X':
            score_X += 1
            ser.write(b'W')  # Send 'W' to Arduino to turn LEDs green for X win
        elif winner == 'O':
            score_O += 1
            ser.write(b'L')  # Send 'L' to Arduino to turn LEDs green for O win
        game_board = [''] * 9  # Reset the game board

    # Display the scores
    cv2.putText(frame, f'Score X: {score_X}', (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(frame, f'Score O: {score_O}', (600, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)

    # Display the current turn in black
    cv2.putText(frame, f'Turn: {turn}', (350, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

    cv2.imshow('Tic-Tac-Toe', frame)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
ser.close()
