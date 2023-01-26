from concurrent.futures import ThreadPoolExecutor


class ThreadPoolService:

    def __init__(self, amount_workers):
        self.amount_workers = amount_workers
        self.pool = ThreadPoolExecutor(self.amount_workers)

    def get_worker(self):
        return self.pool
