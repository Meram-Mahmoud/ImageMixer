import threading
import time

class DataProcessingThread(threading.Thread):
    def __init__(self, data_queue, stop_event):
        """
        Initialize the thread.
        :param data_queue: Queue to hold incoming data for processing.
        :param stop_event: Event to signal the thread to stop.
        """
        super().__init__()
        self.data_queue = data_queue
        self.stop_event = stop_event

    def process_data(self, data):
        """
        Simulate data processing (e.g., HRV/FHR analysis).
        :param data: The input data to process.
        """
        # Example: Simulate data filtering and analysis
        time.sleep(0.5)  # Simulate processing time
        result = f"Processed: {data}"
        return result

    def run(self):
        """Thread's activity: process data in the queue until stopped."""
        print("Thread started.")
        while not self.stop_event.is_set():
            if not self.data_queue.empty():
                data = self.data_queue.get()
                result = self.process_data(data)
                print(result)  # You can save or send the result elsewhere
            else:
                time.sleep(0.1)  # Avoid busy waiting
        print("Thread stopped.")

# Example usage
if __name__ == "__main__":
    from queue import Queue

    # Create a queue to hold data and an event to signal stopping
    data_queue = Queue()
    stop_event = threading.Event()

    # Create and start the thread
    thread = DataProcessingThread(data_queue, stop_event)
    thread.start()

    # Simulate adding data to the queue
    for i in range(10):
        data_queue.put(f"Data {i}")
        time.sleep(0.2)  # Simulate real-time data arrival

    # Signal the thread to stop and wait for it to finish
    stop_event.set()
    thread.join()

    print("Main program finished.")
