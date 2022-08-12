from blog import create_app

# we can pass another config file, our set as default
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
