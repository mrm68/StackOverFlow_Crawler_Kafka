# main.py

from Crawler.watcher import QuestionWatcher as QuestionWatcher
import logging
import traceback

logging.basicConfig(level=logging.ERROR)


def main():
    """Main application workflow"""
    try:
        language = 'python'
        # language = input(
        #     "Enter programming language to monitor (e.g., python): "
        # ).strip().lower()
        check_interval = 3
        # check_interval = int(
        #     input("Enter check interval in seconds (default 60): ") or 60)

        if check_interval <= 0:
            print("Error: Check interval must be positive")
            return

        watcher = QuestionWatcher(
            language=language, check_interval=check_interval)
        watcher.start_watching()

    except ValueError:
        print("Error: Please enter valid numbers")
    except Exception as e:
        logging.exception("An error occurred")
        print(f"An error occurred: {e}")
        traceback.print_exc()


if __name__ == "__main__":
    main()
