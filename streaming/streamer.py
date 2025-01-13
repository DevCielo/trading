import json
import threading
import time
from queue import Queue

from streaming.stream_prices import PriceStreamer
from streaming.stream_processor import PriceProcessor
from streaming.stream_worker import WorkProcesser


def load_settings():
        with open("./bot/settings.json", "r") as f:
            return json.loads(f.read())

def run_streamer():
    settings = load_settings()

    shared_prices = {}
    shared_prices_events = {}
    shared_prices_lock = threading.Lock()
    work_queue = Queue()

    for p in settings['pairs'].keys():
        shared_prices_events[p] = threading.Event()
        shared_prices[p] = {}

    threads = []

    price_stream_t = PriceStreamer(shared_prices, shared_prices_lock, shared_prices_events)
    price_stream_t.daemon = True
    threads.append(price_stream_t)
    price_stream_t.start()

    worker_t = WorkProcesser(work_queue)
    worker_t.daemon = True
    threads.append(worker_t)
    worker_t.start()

    for p in settings['pairs'].keys():
        processing_t = PriceProcessor(shared_prices, shared_prices_lock, shared_prices_events, f"PriceProcessor_{p}", p, work_queue)
        processing_t.daemon = True
        threads.append(processing_t)
        processing_t.start()

    try:
        for t in threads:
            t.join()
    except KeyboardInterrupt:
        print("Keyboard Interrupt")

    print("ALL DONE")