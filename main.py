import time
import schedule
from controller.news import News


def main():
    News()
    schedule.every(1).hours.do(News)
    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == '__main__':
    main()
