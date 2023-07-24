import logging
import threading
import time


def thread_OnOff(name):
    logging.info("Thread %s: starting", name)

    previous_reading = 1
    while True:

        time.sleep(0.01)
        current = GPIO.input(button_GPIO)  # Take reading of button at current moment
        # Print useful info to terminal (For Debugging)
        if current != previous_reading:
            switchLights()
        else:
            pass


def thread_Color(name):
    logging.info("Thread %s: starting", name)
    count = 0
    while count <= 100:
        input("Press enter to continue thread")
        print(name,count)
        count+=1
    logging.info("Thread %s: finishing", name)



if __name__ == "__main__":
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO,
                        datefmt="%H:%M:%S")

    threads = []
    on_off_Thread = threading.Thread(target=thread_function1, args=("on/off",))
    color_Thread = threading.Thread(target=thread_function2, args=("color",))
    threads.append(on_off_Thread)
    threads.append(color_Thread)

    on_off_Thread.start()
    color_Thread.start()

    for index, thread in enumerate(threads):
        logging.info("Main    : before joining thread %d.", index)
        thread.join()
        logging.info("Main    : thread %d done", index)