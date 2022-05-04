import random
from art import logo

cards = [11, 10, "Jack", "King", "Queen", 9, 8, 7, 6, 5, 4, 3, 2]

def evaluate(hand):
    duplicate = hand.copy()
    for i in range(len(duplicate)):
        if duplicate[i] == "Jack" or duplicate[i] == "King" or duplicate[i] == "Queen":
            duplicate[i] = 10
    if sum(duplicate) > 21 and 11 in duplicate:
        a = hand.index(11)
        hand[a] = 1
        duplicate[a] = 1
    hand_total = sum(duplicate)
    return hand_total

def assess_win(human, computer):
    if human > 21:
        return "lose"
    
    if human == 21 and computer == 21:
        return "draw"

    elif human == 21 or computer == 21:
        if human == 21:
            return "win"
        else:
            return "lose"

    elif computer >= 17:
        if human > computer and computer <= 21:
            return "win"
        elif human == computer:
            return "draw"
        elif computer > 21 and human < 21:
            return "win"
        else:
            return "lose"

def playblackjack():
    compcards = []
    humcards = []
    print(logo)
    for i in range(2):
        compcards.append(random.choice(cards))
        humcards.append(random.choice(cards))

    print(f"Your cards: {humcards}")
    print(f"Computer's first card: {compcards[0]} \n")

    hum_tot = evaluate(humcards)
    comp_tot = evaluate(compcards)
    
    if hum_tot == 21 or comp_tot == 21:
        first_outcome = assess_win(human = hum_tot, computer = comp_tot)
        
        if first_outcome == "draw" or first_outcome == "win" or first_outcome == "lose":
            print(f"You {first_outcome}! \nHere are your cards: {humcards}. And here is your total: {hum_tot}.")
            print( f"Here are the computer's cards: {compcards}. And here is the computers total: {comp_tot}.")
            return first_outcome
    else:
        game = True
        while game is True:
            pass_marker = True
            while pass_marker is True:
                response = input("Do you want to hit or pass? ").lower()
                if response != "hit" and response != "pass":
                    pass
                else:
                    pass_marker = False
        
            if response == "hit":
                humcards.append(random.choice(cards))
                hum_tot = evaluate(humcards)
                comp_tot = evaluate(compcards)
                outcome = assess_win(hum_tot, comp_tot)

                if outcome == "draw" or outcome == "win" or outcome == "lose":
                    print(f"\nYou {outcome}! Here are your cards: {humcards}. And here is your total: {hum_tot}.")
                    print( f"Here are the computer's cards: {compcards}. And here is the computers total: {comp_tot}.")
                    game = False
                    return outcome
                
                else:
                    print(f"Your cards: {humcards}")
            
            else:
                while evaluate(compcards) < 17:
                    compcards.append(random.choice(cards))
                hum_tot = evaluate(humcards)
                comp_tot = evaluate(compcards)
                outcome = assess_win(hum_tot, comp_tot)
                print(f"\nYou {outcome}! Here are your cards: {humcards}. And here is your total: {hum_tot}.")
                print( f"Here are the computer's cards: {compcards}. And here is the computers total: {comp_tot}.")
                game = False
                return outcome

var = playblackjack()
print(var)

            
            






