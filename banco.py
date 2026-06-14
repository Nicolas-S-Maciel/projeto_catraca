import sqlite3

def criar_banco():
    # Conecta ao banco (se não existir, ele cria o arquivo automacao.db)
    conexao = sqlite3.connect('automacao.db')
    cursor = conexao.cursor()

    # Cria a tabela de Funcionários
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS funcionarios (
            id_cracha TEXT PRIMARY KEY,
            nome TEXT NOT NULL,
            setor TEXT NOT NULL,
            acesso_liberado BOOLEAN NOT NULL
        )
    ''')

    # Cria a tabela de Histórico de Acessos
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cracha TEXT,
            data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
            status TEXT NOT NULL,
            FOREIGN KEY(id_cracha) REFERENCES funcionarios(id_cracha)
        )
    ''')

    # Limpa a tabela de funcionários para não duplicar se rodar o script duas vezes
    cursor.execute('DELETE FROM funcionarios')

    # Insere funcionários de teste (TI e TA)
    funcionarios_teste = [
        ('111', 'João Silva', 'Produção', True),
        ('222', 'Maria Souza', 'Manutenção', True),
        ('333', 'Carlos Eduardo', 'Visitante', False) # Acesso bloqueado
    ]
    
    cursor.executemany('INSERT INTO funcionarios VALUES (?, ?, ?, ?)', funcionarios_teste)

    # Salva as alterações e fecha a conexão
    conexao.commit()
    conexao.close()
    print("Banco de dados criado e populado com sucesso!")

if __name__ == '__main__':
    criar_banco()