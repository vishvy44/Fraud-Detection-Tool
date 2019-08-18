from api.fraudapp import app


if __name__ == '__main__':
    app.debug='true'
    app.run(host='0.0.0.0')
