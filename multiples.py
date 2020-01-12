n = int(input('Please enter the value of N: '))

if n <= 0:
    raise Exception('Value of N ({}) should be greater than 0'.format(n))

m = int(input('Please enter the value of M: '))

if m <= 0:
    raise Exception('Value of M ({}) should be greater than 0'.format(m))

magic_num_dict = {}  # store the {magic_number: substitute} pair

for _ in range(m):
    num = int(input('Please enter the magic number: '))
    magic_num_dict[num] = raw_input('Please enter the substitute for {}: '.format(num))

for i in range(1, n+1):
    stmnt = ''  # the statement to print
    multiple_found = False  # whether multiple is found or not
    for num in magic_num_dict.keys():
        if i%num == 0:
            multiple_found = True
            stmnt += magic_num_dict[num]  # multiple is found, append the substitute
    if not multiple_found:
        stmnt = i  # if no multiple found,
    print(stmnt)