import sqlite3

def criar_banco():
    # Conecta ao banco de dados (cria o arquivo automacao.db se não existir)
    conexao = sqlite3.connect('automacao.db')
    cursor = conexao.cursor()

    # Cria a tabela de Funcionários (Entidade principal)
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS funcionarios (
            id_cracha TEXT PRIMARY KEY,
            nome TEXT NOT NULL,
            setor TEXT NOT NULL,
            acesso_liberado BOOLEAN NOT NULL
        )
    ''')

    # Cria a tabela de Histórico (Entidade de registro) com Chave Estrangeira
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS historico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            id_cracha TEXT,
            data_hora DATETIME DEFAULT CURRENT_TIMESTAMP,
            status TEXT NOT NULL,
            FOREIGN KEY(id_cracha) REFERENCES funcionarios(id_cracha)
        )
    ''')

    # Limpa a tabela de funcionários para não dar erro de duplicação se rodar 2 vezes
    cursor.execute('DELETE FROM funcionarios')

    # Insere 3 funcionários de teste automaticamente para facilitar a apresentação
    funcionarios_teste = [
        ('111', 'João Silva', 'Produção', True),
        ('222', 'Maria Souza', 'Manutenção', True),
        ('333', 'Carlos Eduardo', 'Visitante', False) # Este usuário está bloqueado
    ]
    
    # Executa o INSERT no banco
    cursor.executemany('INSERT INTO funcionarios VALUES (?, ?, ?, ?)', funcionarios_teste)

    # Salva as alterações (commit) e fecha a conexão
    conexao.commit()
    conexao.close()
    print("Banco de dados criado e populado com sucesso!")

if __name__ == '__main__':
    criar_banco()