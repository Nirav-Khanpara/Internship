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

async def read_files(fname,c):
    with open(fname,'r') as f:
        for i in f.readlines():
            if i=='MARUTI\n':
                if fname=='File1.txt':
                    c[0]+=1
                else:
                    c[1]+=1

async def write_to_file(file_name,c):
    generated_string = random.choice([await generate_random(), 'MARUTI'])
    with open(file_name,'a') as f:
        f.write(generated_string+'\n')

async def main():
    while True:
        c = [0, 0]
        t1 = asyncio.create_task(write_to_file('File1.txt',c))
        t2 = asyncio.create_task(write_to_file('File2.txt',c))
        t3 = asyncio.create_task(read_files('File1.txt',c))
        t4 = asyncio.create_task(read_files('File2.txt',c))
        t5 = asyncio.create_task(write_count(c))

        await asyncio.gather(t1, t2, t3, t4, t5)

asyncio.run(main())
