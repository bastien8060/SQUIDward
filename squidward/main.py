import json
import time
import random
import asyncio
from tqdm import tqdm
from squidward import Client

def worker(tag, cli, progress_bar):
    try:
        time1 = time.time()
        res = cli.checkTag(tag)
        time2 = time.time()

        if res.get('statusCode') == 404 and res.get('errorCode') == 'ERR_TAG_NOT_FOUND':
            pass
        elif res.get('statusCode') != 200:
            print("Unknown error: " + res.get('errorCode') + " " + res.get('message'))
        else:
            print("Found tag: " + tag)

        # Update the progress bar
        if progress_bar:
            progress_bar.update(1)

    except KeyboardInterrupt:
        pass

def bruteforce_tags():
    tag_generator = gen_all_tags(7 * 2)
    total_tags = 16 ** (7 * 2)

    master_bar = tqdm(total=total_tags, desc="Bruteforcing Tags", unit="tag", miniters=10, maxinterval=20, mininterval=2)

    cli = Client()
    if not cli.authPresent:
        cli.login("saidi.ireland@gmail.com", "bastienRES13")

    loop = asyncio.get_event_loop()

    for tag in tag_generator:
        loop.run_in_executor(None, worker, tag, cli, master_bar)

    loop.run_until_complete(asyncio.sleep(0))  # Ensure all tasks are completed
    master_bar.close()

def gen_all_tags(length):
    modulus = 16 ** length
    a = 5  # Choose an appropriate multiplier
    c = 3  # Choose an appropriate increment
    seed = random.randint(0, modulus - 1)

    print("Generated seed: " + str(seed))

    for _ in range(modulus):
        tag = "{:0{}X}".format(seed, length)
        yield tag

        seed = (a * seed + c) % modulus

if __name__ == "__main__":
    bruteforce_tags()
