from flask import Flask, render_template_string, request, redirect, session, send_from_directory
import os

app = Flask(__name__)
app.secret_key = "censs_secret"

BASE = "uploads"
os.makedirs(BASE, exist_ok=True)

# Single user
users = {"censs": "censs@1234"}

# Folders and Subfolders
folders = {
    "Power BI":["Chandana","Eswari","Narendra","Sandhya","Saathvik"],
    "Tableau":["Chandana","Eswari","Narendra","Sandhya","Saathvik"],
    "MySQL":["Chandana","Eswari","Narendra","Sandhya","Saathvik"],
    "Python":["Chandana","Eswari","Narendra","Sandhya","Saathvik"],
    "MS Excel":["Chandana","Eswari","Narendra","Sandhya","Saathvik"],
    "Data Sets":["Raw Dataset","Cleaned Dataset"]
}

HTML = """
<!DOCTYPE html>
<html>
<head>
<title>CENSS Dashboard</title>
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<style>
body {margin:0;font-family:Segoe UI;background:#0f172a;color:white;}
.login {height:100vh;display:flex;justify-content:center;align-items:center;}
.box {background:#1e293b;padding:30px;border-radius:15px;text-align:center;}
.sidebar {width:230px;height:100vh;position:fixed;background:#020617;padding:20px;}
.main {margin-left:250px;padding:20px;}
.folder {padding:10px;background:#1e293b;margin:5px;border-radius:10px;cursor:pointer;transition:0.3s;}
.folder:hover {background:#334155;transform:scale(1.05);}
.subfolder {padding:8px;margin:5px;background:#334155;border-radius:8px;}
.file {background:#334155;margin:5px;padding:8px;border-radius:8px;display:flex;justify-content:space-between;align-items:center;}
button {margin:2px;padding:5px 10px;border:none;border-radius:5px;cursor:pointer;}
.upload {background:#22c55e;color:white;}
.logout {background:#ef4444;color:white;position:absolute;top:10px;right:20px;}
input,select {padding:5px;border-radius:5px;border:none;margin-right:5px;}
.card {background:#1e293b;padding:15px;margin:10px 0;border-radius:15px;transition:0.3s;}
.card:hover {transform:scale(1.02);}
canvas {background:white;border-radius:10px;margin-top:10px;}
.topbar {display:flex;justify-content:flex-start;align-items:center;margin-bottom:10px;gap:10px;}
</style>
</head>

<body>

{% if not session.get("user") %}
<div class="login">
<div class="box">
<h2>🚀 CENSS Dashboard</h2>
<form method="post">
<input name="username" placeholder="Username"><br><br>
<input name="password" type="password" placeholder="Password"><br><br>
<button>Login</button>
</form>
<p>{{error}}</p>
</div>
</div>

{% else %}
<a href="/logout"><button class="logout">Logout</button></a>

<div class="sidebar">
<h3>📊 CENSS</h3>
{% for f in folders %}
<div class="folder" onclick="window.location='/?folder={{f}}'">{{f}}</div>
{% endfor %}
</div>

<div class="main">

<div class="topbar">
<form method="get" style="display:flex;align-items:center;gap:5px;">
<input name="search" placeholder="🔍 Search" value="{{search}}">
<select name="sort">
<option value="">Sort</option>
<option value="az" {% if sort=="az" %}selected{% endif %}>A-Z</option>
<option value="za" {% if sort=="za" %}selected{% endif %}>Z-A</option>
</select>
<input type="hidden" name="folder" value="{{current_folder}}">
<button>Apply</button>
</form>

<form method="post" action="/upload" enctype="multipart/form-data" style="display:flex;align-items:center;gap:5px;">
<input type="hidden" name="folder" value="{{current_folder}}">
<input type="file" name="file" required>
<button class="upload">Upload</button>
</form>

</div>

{% if current_folder %}
<h2>{{current_folder}}</h2>

<div class="card">
<h3>Files Count</h3>
<canvas id="chart-folder"></canvas>
</div>

{% for s in folders[current_folder] %}
<div class="card">
<div class="subfolder">
<h4>{{s}} ({{counts[current_folder][s]}})</h4>

{% for file in data[current_folder][s] %}
<div class="file">
<a href="/file/{{current_folder}}/{{s}}/{{file}}" target="_blank">{{file}}</a>
<div>
<a href="/download/{{current_folder}}/{{s}}/{{file}}"><button>⬇️</button></a>
<form method="post" action="/delete/{{current_folder}}/{{s}}/{{file}}" style="display:inline;">
<button>❌</button>
</form>
</div>
</div>
{% endfor %}

</div>
</div>
{% endfor %}

<script>
const ctx = document.getElementById('chart-folder').getContext('2d');
new Chart(ctx, {
    type:'bar',
    data:{
        labels: {{folders[current_folder]|tojson}},
        datasets:[{
            label:'Files Count',
            data: {{counts[current_folder].values()|list}},
            backgroundColor:['#22c55e','#3b82f6','#f59e0b','#ef4444','#8b5cf6']
        }]
    },
    options:{
        responsive:true,
        plugins:{legend:{display:false}, title:{display:true,text:'Files Count'}},
        scales:{y:{beginAtZero:true,precision:0}}
    }
});
</script>

{% endif %}
</div>
{% endif %}
</body>
</html>
"""

# ROUTES
@app.route("/", methods=["GET","POST"])
def home():
    error=""
    if request.method=="POST":
        if users.get(request.form["username"]) == request.form["password"]:
            session["user"] = request.form["username"]
            return redirect("/")
        else:
            error="Invalid Credentials"

    if not session.get("user"):
        return render_template_string(HTML, error=error)

    current_folder=request.args.get("folder")
    search=request.args.get("search","").lower()
    sort=request.args.get("sort")

    data={}
    counts={}

    for f, subs in folders.items():
        data[f]={}
        counts[f]={}
        for s in subs:
            path=os.path.join(BASE,f,s)
            os.makedirs(path, exist_ok=True)
            files=os.listdir(path)

            if search:
                files=[x for x in files if search in x.lower()]
            if sort=="az": files.sort()
            if sort=="za": files.sort(reverse=True)

            data[f][s]=files
            counts[f][s]=len(files)

    return render_template_string(HTML, folders=folders, data=data, counts=counts,
                                  current_folder=current_folder, search=search, sort=sort, error=error)

@app.route("/upload", methods=["POST"])
def upload():
    f=request.form["folder"]
    if not f:
        return redirect("/")
    file=request.files["file"]
    # upload to first subfolder automatically
    s=folders[f][0]
    path=os.path.join(BASE,f,s)
    os.makedirs(path, exist_ok=True)
    file.save(os.path.join(path,file.filename))
    return redirect(f"/?folder={f}")

@app.route("/file/<f>/<s>/<name>")
def file(f,s,name):
    return send_from_directory(os.path.join(BASE,f,s), name, as_attachment=False)

@app.route("/download/<f>/<s>/<name>")
def download(f,s,name):
    return send_from_directory(os.path.join(BASE,f,s), name, as_attachment=True)

@app.route("/delete/<f>/<s>/<name>", methods=["POST"])
def delete(f,s,name):
    os.remove(os.path.join(BASE,f,s,name))
    return redirect(f"/?folder={f}")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

if __name__=="__main__":
    app.run(debug=True, host="0.0.0.0", port=10000)