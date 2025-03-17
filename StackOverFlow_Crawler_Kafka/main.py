# main.py

from Crawler.watcher import QuestionWatcher


def main():
    """Main application workflow"""
    try:
        language = input(
            "Enter programming language to monitor (e.g., python): "
        ).strip().lower()
        check_interval = int(
            input("Enter check interval in seconds (default 60): ") or 60)

        if check_interval <= 0:
            print("Error: Check interval must be positive")
            return

        watcher = QuestionWatcher(
            language=language, check_interval=check_interval)
        watcher.start_watching()

    except ValueError:
        print("Error: Please enter valid numbers")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    main()
