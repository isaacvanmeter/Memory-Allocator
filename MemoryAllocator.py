block_five = ['-', '-', '-', '-', '-', '-', '-', '-', '-', '-']
block_ten = ['-', '-', '-', '-', '-']
block_twenty = ['-', '-', '-', '-', '-']
catch_all = '-' * 300
catch_all_record = ""

def readFile(file_path):
    arr = []
    with open(file_path, 'r') as file:
        arr = [line.strip() for line in file.readlines()]
    
    arr2 = [line.split(' ') for line in arr]
        
    return arr2

def allocate(arr):
    global block_five, block_ten, block_twenty, catch_all, catch_all_record
    
    for item in arr:
        print(' '.join(map(str, item)))
        if item[1] == 'allocate':
            size = int(item[2])
            if size == 5 and '-' in block_five:
                index = block_five.index('-')
                block_five[index] = item[0]
            elif size == 10 and '-' in block_ten:
                index = block_ten.index('-')
                block_ten[index] = item[0]
            elif size == 20 and '-' in block_twenty:
                index = block_twenty.index('-')
                block_twenty[index] = item[0]
            else:
                if '-' * size in catch_all:
                    index = catch_all.find('-' * size)
                    catch_all_record += f" {item[0]}({index}:{index + size})"
                    catch_all = catch_all[:index] + "*" * size + catch_all[index + size:]
                elif size < 5 and '-' in block_five:
                    index = block_five.index('-')
                    block_five[index] = item[0] + f"({size})"
                elif size < 10 and '-' in block_ten:
                    index = block_ten.index('-')
                    block_ten[index] = item[0] + f"({size})"
                elif size < 20 and '-' in block_twenty:
                    index = block_twenty.index('-')
                    block_twenty[index] = item[0] + f"({size})"
                else:
                    print("Allocation failed. No room.")
        elif item[1] == 'free':
            freed = False
            if item[0] in block_five:
                block_five = ['-' if x == item[0] else x for x in block_five]
            elif item[0] in block_ten:
                block_ten = ['-' if x == item[0] else x for x in block_ten]
            elif item[0] in block_twenty:
                block_twenty = ['-' if x == item[0] else x for x in block_twenty]
            else:
                allocations = catch_all_record.split()
                for alloc in allocations:
                    if alloc.startswith(item[0]):
                        start, end = map(int, alloc[alloc.index('(')+1:alloc.index(')')].split(':'))
                        catch_all = catch_all[:start] + '-' * (end - start) + catch_all[end:]
                        catch_all_record = catch_all_record.replace(alloc, '')
                        freed = True
                        break
                if not freed:
                    print(f"Freeing failed: {item[0]} not found.")
        else:
            print("Invalid input")
        print("5: " + ' '.join(map(str, block_five)))
        print("10: " + ' '.join(map(str, block_ten)))
        print("20: " + ' '.join(map(str, block_twenty)))
        print(f"Catch All: {catch_all_record}")
        print("Visual Memory:")
        print_catch = fix(block_five, 5) + fix(block_ten, 10) + fix(block_twenty, 20) + catch_all
        for i in range(0, len(print_catch), 50):
            print(print_catch[i:i+50])
    
def fix(arr, num):
    val = ""
    for item in arr:
        if any(char.isalpha() for char in item) and '(' in item:
            start = item.find('(') + 1
            end = item.find(')')
            space = int(item[start:end])
            val += '*' * space + '-' * (num - space)
        elif item != '-':
            val += '*'*num
        else:
            val += '-'*num
    return val

file_name = readFile('alloc_data3.txt')
allocate(file_name)

