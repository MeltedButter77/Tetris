# 🎮 Tetris

Playable [here](https://meltedbutter.xyz/Tetris/).

I think almost everyone knows what Tetris is. Created in Python using PyGame-CE, this little project took me about 6 hours to complete. This project acted as a skill builder and also as an example project in a coding club I teach. 

I very much enjoyed the challenge of moving rotatable pieces. I implemented a class for pieces and defined the piece's origin; each block was then drawn at an offset from that point. To allow the piece to rotate, the list of offsets is simply changed. For most pieces there are 4 lists defining the offsets for each block, one list for each rotation. Some have 2, and the square only has one. Another interesting problem was ensuring that a piece could not be rotated off the screen or into another block. To ensure this, the piece is rotated and collision checked; if a collision occurs, it is rotated back before being drawn to the screen.

![Tetris](https://github.com/user-attachments/assets/8b1c15a9-bc00-4848-9e30-071e1738332c)

## 🤖 Use of AI

All the possible rotations of each piece were generated with ChatGPT. I filled in one rotation for each piece and asked it to fill the rest. Its Z and S pieces were fairly poor, so I did end up doing a significant amount by hand anyway.
