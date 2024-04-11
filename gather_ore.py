import subprocess
import threading
from queue import Queue
import time

KEYS_DIR = "填入你的錢包路徑"
MAIN_ADDR = "填入你的主錢包地址"
THREAD_COUNT = 16

def transfer_ore(index):
    owner_key = f"{KEYS_DIR}/id{index}.json"
    balance_result = subprocess.run(["spl-token", "balance", "oreoN2tQbHXVaZsr3pf66A48miqcBXCDJozganhEJgz", "--owner", owner_key], capture_output=True, text=True)
    balance = balance_result.stdout.strip()
    
    if float(balance) > 0:
        print(f"id{index}.json 余额大于0，尝试转账...")
        while True:
            transfer_result = subprocess.run(["spl-token", "transfer", "--owner", owner_key, "--url", "https://api.mainnet-beta.solana.com", "oreoN2tQbHXVaZsr3pf66A48miqcBXCDJozganhEJgz", "ALL", MAIN_ADDR, "--fund-recipient"], capture_output=True, text=True)
            if transfer_result.returncode == 0:
                print(f"id{index}.json 转账成功.")
                break
            else:
                print(f"id{index}.json 转账失败，重试...")
    else:
        print(f"id{index}.json 余额为0，跳过...")

def worker(q):
    while not q.empty():
        index = q.get()
        try:
            transfer_ore(index)
        finally:
            q.task_done()

def main():
    while True:
        q = Queue()
        for i in range(100):
            q.put(i)
        
        threads = []
        for _ in range(THREAD_COUNT):
            t = threading.Thread(target=worker, args=(q,))
            t.start()
            threads.append(t)
        
        for t in threads:
            t.join()

        print("一次迭代完成，等待下一次迭代...")
        time.sleep(10)  # 可根据实际需要调整等待时间

if __name__ == "__main__":
    main()
