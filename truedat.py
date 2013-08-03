from flask import Flask, render_template
from app.feeds import feeder

app = Flask(__name__)
app.debug = True

@app.route("/")
def index():
  activities = feeder.latest()

  return render_template("index.html", activities=activities)

if __name__ == "__main__":
  app.run()
