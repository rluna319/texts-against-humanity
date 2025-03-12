import json

with open('cah-all-compact.json', 'r') as f:
    data = json.load(f)
    
print('Black cards:', len(data['black']))
print('White cards:', len(data['white']))

print('\nSample black cards:')
for i in range(5):
    print(f"{i+1}. {data['black'][i]}")

print('\nSample white cards:')
for i in range(5):
    print(f"{i+1}. {data['white'][i]}")

# Check for blanks in black cards
print('\nBlack cards with blanks:')
for i in range(20):
    if '_' in data['black'][i]['text']:
        print(f"{i+1}. {data['black'][i]}") 