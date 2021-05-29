"""Main program script."""

import logging

from flask import Flask

app = Flask(__name__)

logging.basicConfig(
    filename="log.log",
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s")

if __name__ == "__main__":
    app.run()
