from flask import Flask, render_template
import psutil

app = Flask(__name__)

@app.route('/')
def index():
    processos = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
        try:
            info = proc.info
            processos.append({
                'pid': info['pid'],
                'nome': info['name'],
                'cpu': info['cpu_percent'],
                'memoria': round(info['memory_info'].rss / (1024 * 1024), 2)  # em MB
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    return render_template('index.html', processos=processos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
