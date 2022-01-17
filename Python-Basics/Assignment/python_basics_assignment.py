import random
import string
import asyncio

async def generate_random(s_minimum,s_maximum):
    x=random.choice([i for i in range(s_minimum,s_maximum+1)])
    s=''
    for _ in range(x):
        s+=random.choice(string.ascii_letters)
    return s

async def write_count(file_name,c):
    # await asyncio.sleep(0.1)
    with open('counts.log', 'w') as f:
        f.write(f"No. of time keyword 'MARUTI' occured in file1: {c[0]}" + '\n')
        f.write(f"No. of time keyword 'MARUTI' occured in file2: {c[1]}")

async def write_to_file(file_name,s_minimum,s_maximum,c):
    generated_string = random.choice([await generate_random(s_minimum,s_maximum), 'MARUTI'])
    with open(file_name,'a') as f:
        f.write(generated_string+'\n')
    if generated_string=='MARUTI':
        if file_name=='File1.txt':
            c[0]+=1
        else:
            c[1]+=1
    await write_count(file_name,c)

async def main():
    c = [0, 0]
    s_minimum = int(input('Enter minimum length for random string: '))
    s_maximum = int(input('Enter maximum length for random string: '))
    if s_maximum < s_minimum:
        print('maximum length should be greater than or equal to minimum length')
        print('Try runnig program again !')
    else:
        while True:
            t1 = asyncio.create_task(write_to_file('File1.txt',s_minimum,s_maximum,c))
            t2 = asyncio.create_task(write_to_file('File2.txt',s_minimum,s_maximum,c))
            await asyncio.gather(t1, t2)

asyncio.run(main())