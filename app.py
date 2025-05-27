from flask import Flask, render_template, jsonify, request
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
                'memoria': round(info['memory_info'].rss / (1024 * 1024), 2) 
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    return render_template('index.html', processos=processos)

@app.route('/api/processos')
def api_processos():
    processos = []
    for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info']):
        try:
            info = proc.info
            processos.append({
                'pid': info['pid'],
                'nome': info['name'],
                'cpu': info['cpu_percent'],
                'memoria': round(info['memory_info'].rss / (1024 * 1024), 2)
            })
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    return jsonify(processos)

@app.route('/api/uso_total')
def uso_total():
    cpu = psutil.cpu_percent(interval=0.5)
    memoria = psutil.virtual_memory()
    return jsonify({
        'cpu_percent': cpu,
        'memoria_usada': round(memoria.used / (1024*1024), 2),
        'memoria_total': round(memoria.total/ (1024*1024), 2),
        'alerta_cpu': cpu > 80,
        'alerta_memoria': memoria.percent > 90
    })

@app.route('/api/encerrar', methods=['POST'])
def encerrar_processo():
    dados = request.get_json()
    pid = dados.get('pid')

    try:
        proc = psutil.Process(pid)
        proc.terminate()
        return jsonify({'mensagem': f'Processo {pid} encerrado com sucesso.'}), 200
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
        return jsonify({'erro': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
