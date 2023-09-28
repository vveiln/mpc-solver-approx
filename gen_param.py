import random

if __name__ == "__main__":
    
    # Pasta p parameter
    field_size = 2 ** 254 + 45560315531419706090280762371685220353
    fake_ptx = [random.randint(0, field_size) for _ in range(28)]
    with open('Player-Data/Input-P0-0', 'w') as f:
        f.write('4 5 2 2 1 ' + ' '.join([str(i) for i in fake_ptx]))
    
    with open('Player-Data/Input-P1-0', 'w') as f:
        f.write('5 4 4 2 2 ' + ' '.join([str(random.randint(0, field_size)) for _ in range(28)]))
