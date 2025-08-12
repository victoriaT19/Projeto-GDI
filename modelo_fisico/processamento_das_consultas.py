import sqlite3

class DatabaseManager:
    def __init__(self, db_name='projeto_fisico.db'):
        self.db = sqlite3.connect(db_name)
        self.cursor = self.db.cursor()
    
    def ler_arquivo(self, file_name='consultas.sql'):
        try:
            with open(file_name, 'rt', encoding='utf-8') as f:
                dados = f.read()
                
                linhas = [linha.strip() for linha in dados.split('\n') 
                         if not linha.strip().startswith('--') and linha.strip()]
                script_sql = '\n'.join(linhas)
                
                sql_comandos = [cmd.strip() for cmd in script_sql.split(';') if cmd.strip()]
                
                print(f"Executando {len(sql_comandos)} comandos do arquivo {file_name}")
                
                for comando in sql_comandos:
                    try:
                        self.cursor.execute(comando)
                        
                        if comando.strip().upper().startswith('SELECT'):
                            print(f"\nResultados para: {comando[:50]}...")
                            for linha in self.cursor.fetchall():
                                print(linha)
                                
                    except sqlite3.Error as e:
                        print(f"Erro ao executar comando: {comando[:50]}...")
                        print(f"Erro: {e}")
                        
            self.db.commit()
            print("Comandos executados com sucesso!")
            
        except FileNotFoundError:
            print(f"Arquivo não encontrado: {file_name}")
        except Exception as e:
            print(f"Erro inesperado: {e}")
            self.db.rollback()
    
    def close(self):
        self.db.close()

if __name__ == "__main__":
    db_manager = DatabaseManager()
    
    db_manager.ler_arquivo('clientes_sp.sql')
    
    db_manager.close()
