from src.engine import App

def main():
    try:
        app = App()

        app.run()
    except Exception as e:
        print(e)

if __name__ == '__main__':
    main()