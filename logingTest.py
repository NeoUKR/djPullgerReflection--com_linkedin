import logging
import time

logging.basicConfig(filename="log11DEBUG.txt", level=logging.DEBUG, format="%(asctime)s %(message)s")
logging.warning('Watch out!')

# logging.debug("Debug logging test...")


for count in range(10):
    print(f'Count: {count}')
    logging.warning('Watch out!')
    time.sleep(1)
