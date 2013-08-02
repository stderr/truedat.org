from flask import Flask
app = Flask(__name__)

@app.route("/")
def root():
  return "truedat.org"

if __name__ == "__main__":
  app.run()
