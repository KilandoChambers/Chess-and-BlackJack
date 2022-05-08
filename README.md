# Chess-and-BlackJack
Chess is a logical, deterministic game that is not largely based on luck or randomness. 
For this project, I coded a chess engine AI using the minimax algorithm with alpha beta 
pruning. I evaluated static positions for each player to determine what is the computer's 
next optimal move. The twist I added in was a black jack game. Black Jack, unlike chess,
is not deterministic and is built on randomness. After every fourth half move (or when each 
player moves twice), the computer initiates a black jack game. If the player wins, the 
computer chooses a random move, implementing both randomness and luck into the chess game. 
If the computer wins, it will continue to play optimally. 

Mobility Function: Most of the components I used to analyze the static position is my
computational implementation of chess theory that has already existed. My mobility 
function is slightly different. The mobility function is used to analyze how much can
a player move on their next turn. Current mobility functions typically analyze how pieces
can move and how many possible moves each piece can make. My mobility function does this
but also takes into account the positional value (see the square tables initialized in the
Evaluations Class) of each next move!

Other subcomponents that I would like to edit into my code later:
1. Allow the player to choose to play as white and black. Meaning the minimax algorithm 
   would have to be altered to incorporate the computer as the *minimizer*.
2. Change the game so that if a player loses the blackjack game the computer selects a
   random move for them.
3. Update the evaluation formula to add or deduct points for doubled pawns, castling, rooks
   on the second/seventh rank, king safety, attacking pieces, pins, forks, windmills, etc.
4. Write a script for a neural network that determines the appropriate weights for each
   component of the evaluation function.
