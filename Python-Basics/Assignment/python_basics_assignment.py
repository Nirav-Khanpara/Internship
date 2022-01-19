import random
import string
import asyncio

async def generate_random(length=6):
    s=''
    for _ in range(length):
        s+=random.choice(string.ascii_letters)
    return s

async def write_count(c):
    with open('counts.log', 'w') as f:
        f.write(f"No. of time keyword 'MARUTI' occured in file1: {c[0]}" + '\n')
        f.write(f"No. of time keyword 'MARUTI' occured in file2: {c[1]}")

async def read_files():
    counts=[0,0]
    with open('File1.txt','r') as f:
        data = f.read()
        counts[0] = data.count('MARUTI')
    with open('File2.txt','r') as f:
        data = f.read()
        counts[1] = data.count('MARUTI')
    await write_count(counts)

async def write_to_file(file_name):
    generated_string = random.choice([await generate_random(), 'MARUTI'])
    with open(file_name,'a') as f:
        f.write(generated_string+'\n')

async def main():
    print('Code execution started ...')
    print('Press Ctrl + Z to stop')
    while True:
        t1 = asyncio.create_task(write_to_file('File1.txt'))
        t2 = asyncio.create_task(write_to_file('File2.txt'))
        t3 = asyncio.create_task(read_files())

        await asyncio.gather(t1, t2, t3)

asyncio.run(main())
