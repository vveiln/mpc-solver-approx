import random

if __name__ == "__main__":
    
    # Pasta p parameter
    field_size = 2 ** 254 + 45560315531419706090280762371685220353
    fake_ptx = [random.randint(0, field_size) for _ in range(28)]
    with open('Input-P0-0', 'w') as f:
        f.write('1 1 2 2 ' + ' '.join([str(i) for i in fake_ptx]))
    
    with open('Input-P1-0', 'w') as f:
        f.write('2 2 1 1 ' + ' '.join([str(random.randint(0, field_size)) for _ in range(28)]))
