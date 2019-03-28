from flaskblog import create_app

app = create_app()


def main():
    if __name__ == '__main__':
        app.run(debug=True)


main()
