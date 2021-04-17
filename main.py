from src.engine import App
from src.engine import Screen

def main():
    try:
        app = App(Screen())

        app.run()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()