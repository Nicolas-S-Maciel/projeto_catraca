from flask import Flask, render_template, request, jsonify, redirect
import sqlite3

app = Flask(__name__)

def conectar_banco():
    conexao = sqlite3.connect('automacao.db')
    conexao.row_factory = sqlite3.Row
    return conexao

# Rota principal: Carrega a página Web com os dados do banco
@app.route('/')
def index():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    # 1. Puxa os últimos 10 acessos da catraca
    cursor.execute('''
        SELECT h.data_hora, f.nome, h.id_cracha, h.status 
        FROM historico h
        JOIN funcionarios f ON h.id_cracha = f.id_cracha
        ORDER BY h.data_hora DESC LIMIT 10
    ''')
    acessos = cursor.fetchall()
    
    # 2. Puxa TODOS os funcionários cadastrados no sistema
    cursor.execute('SELECT * FROM funcionarios')
    funcionarios = cursor.fetchall()
    
    conexao.close()
    return render_template('index.html', acessos=acessos, funcionarios=funcionarios)

# Rota para CADASTRAR um funcionário (C do CRUD)
@app.route('/cadastrar', methods=['POST'])
def cadastrar_funcionario():
    id_cracha = request.form['id_cracha']
    nome = request.form['nome']
    setor = request.form['setor']
    acesso_liberado = True if request.form.get('acesso_liberado') else False
    
    conexao = conectar_banco()
    cursor = conexao.cursor()
    try:
        cursor.execute('''
            INSERT INTO funcionarios (id_cracha, nome, setor, acesso_liberado) 
            VALUES (?, ?, ?, ?)
        ''', (id_cracha, nome, setor, acesso_liberado))
        conexao.commit()
    except sqlite3.IntegrityError:
        pass # Ignora se tentar cadastrar um ID de crachá que já existe
    
    conexao.close()
    return redirect('/')

# Rota para APAGAR UM CRACHÁ (D do CRUD)
@app.route('/deletar_funcionario/<id_cracha>', methods=['POST'])
def deletar_funcionario(id_cracha):
    conexao = conectar_banco()
    cursor = conexao.cursor()
    
    # Primeiro limpamos o histórico desse crachá para o banco não dar erro de vínculo
    cursor.execute('DELETE FROM historico WHERE id_cracha = ?', (id_cracha,))
    # Depois apagamos o funcionário do sistema
    cursor.execute('DELETE FROM funcionarios WHERE id_cracha = ?', (id_cracha,))
    
    conexao.commit()
    conexao.close()
    return redirect('/')

# Rota para APAGAR TODO O HISTÓRICO da catraca
@app.route('/limpar_historico', methods=['POST'])
def limpar_historico():
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('DELETE FROM historico')
    conexao.commit()
    conexao.close()
    return redirect('/')

# Rota de Integração TA: Simula o sensor da catraca lendo o RFID
@app.route('/passar_cracha', methods=['POST'])
def pasar_cracha():
    dados = request.get_json()
    id_cracha = dados.get('id_cracha')
    
    conexao = conectar_banco()
    cursor = conexao.cursor()
    cursor.execute('SELECT nome, acesso_liberado FROM funcionarios WHERE id_cracha = ?', (id_cracha,))
    funcionario = cursor.fetchone()
    
    if funcionario:
        nome = funcionario['nome']
        status = "Entrada Permitida" if funcionario['acesso_liberado'] else "Acesso Negado"
        cursor.execute('INSERT INTO historico (id_cracha, status) VALUES (?, ?)', (id_cracha, status))
        conexao.commit()
        mensagem = f"Catraca acionada para {nome}: {status}!"
    else:
        mensagem = "Crachá não reconhecido no sistema!"
        
    conexao.close()
    return jsonify({"mensagem": mensagem})

if __name__ == '__main__':
    app.run(debug=True)