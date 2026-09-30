from cards import to_string, make_card

for i in range(52):
    print(to_string(i))
    
for i in range(13):
    for j in range(4):
        print(to_string(make_card(i,j)))