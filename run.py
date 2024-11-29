from welcomehome import create_app

wh = create_app()

if __name__ == "__main__":
    wh.run(debug=True)

