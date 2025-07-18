from flask import Flask, request, render_template_string
from kiteconnect import KiteConnect

app = Flask(__name__)

API_KEY = "84pgb53pnc39ph6p"
API_SECRET = "i76fjuhxye6qvqekvsct9a16lc1xslcg"

HTML_TEMPLATE = """
<!doctype html>
<title>Kite Access Token Generator</title>
<h2>🔑 Generate Access Token</h2>
<form method="post">
  <label>Request Token:</label><br>
  <input name="request_token" style="width: 300px;" required><br><br>
  <button type="submit">Generate Access Token</button>
</form>

{% if access_token %}
  <h3>✅ Access Token:</h3>
  <div style="background:#dff0d8;padding:10px;border-radius:5px;">
    {{ access_token }}
  </div>
{% elif error %}
  <h3 style="color:red;">❌ Error:</h3>
  <div style="background:#f2dede;padding:10px;border-radius:5px;">
    {{ error }}
  </div>
{% endif %}
"""

@app.route("/", methods=["GET", "POST"])
def index():
    access_token = None
    error = None

    if request.method == "POST":
        req_token = request.form.get("request_token", "").strip()
        try:
            kite = KiteConnect(api_key=API_KEY)
            session = kite.generate_session(req_token, api_secret=API_SECRET)
            access_token = session["access_token"]
            with open("access_token.txt", "w") as f:
                f.write(access_token)
        except Exception as e:
            error = str(e)

    return render_template_string(HTML_TEMPLATE, access_token=access_token, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
