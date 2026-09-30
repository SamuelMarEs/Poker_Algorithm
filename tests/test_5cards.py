from poker.evaluator import evaluate5
from poker.cards import hand_to_list

hand1 = []
hand2 = []

print("Enter the first hand")
for _ in range(5):
    rank, suit = map(str, input().split())
    hand1.append((rank, suit))

print("Enter the second hand")
for _ in range(5):
    rank, suit = map(str, input().split())
    hand2.append((rank, suit))
    
new_hand1 = hand_to_list(hand1)
new_hand2 = hand_to_list(hand2)

if evaluate5(new_hand1) >= evaluate5(new_hand2):
    print(f'The higher hand is {hand1}')
else:
    print(f'The higher hand is {hand2}')