import sqlite3
from datetime import datetime

# Conecta ao banco de dados (cria se não existir)
conn = sqlite3.connect('projeto_fisico.db')
cursor = conn.cursor()

# Criação das tabelas
cursor.executescript("""
CREATE TABLE IF NOT EXISTS CLIENTE( 
    ID INT, 
    NOME VARCHAR(100) NOT NULL, 
    FONE VARCHAR(11), 
    ENDERECO VARCHAR(150), 
    CONSTRAINT PK_CLIENTE PRIMARY KEY(ID) 
);

CREATE TABLE IF NOT EXISTS MOTORISTA( 
    CPF VARCHAR(11), 
    NOME VARCHAR(100) NOT NULL, 
    CNH VARCHAR(9) UNIQUE NOT NULL, 
    DATA_CONTR DATE,
    SUPERVISOR VARCHAR(11), 
    CONSTRAINT PK_MOTORISTA PRIMARY KEY (CPF), 
    CONSTRAINT FK_MOTORISTA_SUPERVISOR FOREIGN KEY (SUPERVISOR) REFERENCES MOTORISTA(CPF) 
);

CREATE TABLE IF NOT EXISTS TRANSPORTE( 
    COD INT,  
    TIPO VARCHAR(100), 
    CAPACIDADE INT, 
    COR VARCHAR(100), 
    PLACA VARCHAR(100), 
    CONSTRAINT PK_TRANS PRIMARY KEY(COD) 
);

CREATE TABLE IF NOT EXISTS CARACTERISTICA( 
    ID INT, 
    ACIDEZ VARCHAR(100), 
    TORRA VARCHAR(100), 
    CORPO VARCHAR(100), 
    MOAGEM VARCHAR(100), 
    CONSTRAINT PK_CARAC PRIMARY KEY(ID) 
);

CREATE TABLE IF NOT EXISTS CAFE( 
    COD INT,  
    NOME VARCHAR(100) NOT NULL, 
    FAZENDA VARCHAR(100), 
    PRECO REAL,  -- SQLite usa REAL para números decimais
    ID INT UNIQUE, 
    CONSTRAINT FK_CAFE_CARAC FOREIGN KEY (ID) REFERENCES CARACTERISTICA(ID) ON DELETE CASCADE,
    CONSTRAINT PK_CAFE PRIMARY KEY(COD) 
);

CREATE TABLE IF NOT EXISTS PROMOCAO( 
    ID INT, 
    VALOR REAL NOT NULL, 
    CONSTRAINT PK_PROMO PRIMARY KEY(ID) 
);

CREATE TABLE IF NOT EXISTS PEDIDO( 
    ID INT, 
    NUM INT, 
    DAT DATE,  
    PRECO_FINAL REAL, 
    QUANT INT,
    DESCONTO REAL,
    CONSTRAINT FK_PEDIDO_CLIENTE FOREIGN KEY (ID) REFERENCES CLIENTE(ID) ON DELETE CASCADE, 
    CONSTRAINT PK_PEDIDO PRIMARY KEY (ID, NUM) 
);

CREATE TABLE IF NOT EXISTS PF( 
    ID INT, 
    CPF CHAR(11) NOT NULL, 
    DATA_NASC DATE, 
    CONSTRAINT FK_PF_CLIENTE FOREIGN KEY (ID) REFERENCES CLIENTE(ID) ON DELETE CASCADE, 
    CONSTRAINT PK_PF PRIMARY KEY (ID) 
);

CREATE TABLE IF NOT EXISTS PJ( 
    ID INT, 
    RAZAO_SOCIAL VARCHAR(100), 
    CNPJ CHAR(14) NOT NULL, 
    CONSTRAINT FK_PJ_CLIENTE FOREIGN KEY (ID) REFERENCES CLIENTE(ID) ON DELETE CASCADE, 
    CONSTRAINT PK_PJ PRIMARY KEY (ID) 
);

CREATE TABLE IF NOT EXISTS RA( 
    ID INT, 
    COD_REV VARCHAR(100), 
    AREA_COB VARCHAR(100), 
    CONSTRAINT FK_RA_PJ FOREIGN KEY (ID) REFERENCES PJ(ID) ON DELETE CASCADE, 
    CONSTRAINT PK_RA PRIMARY KEY (ID) 
);

CREATE TABLE IF NOT EXISTS TEM( 
    ID INT, 
    NUM INT, 
    COD INT,
    ID_PROMO INT,                  
    CONSTRAINT FK_PEDIDO_CAFE FOREIGN KEY (ID, NUM) REFERENCES PEDIDO(ID, NUM) ON DELETE CASCADE, 
    CONSTRAINT FK_TEM_CAFE FOREIGN KEY (COD) REFERENCES CAFE(COD) ON DELETE CASCADE,
    CONSTRAINT FK_TEM_PROMO FOREIGN KEY (ID_PROMO) REFERENCES PROMOCAO(ID) ON DELETE SET NULL,
    CONSTRAINT PK_TEM PRIMARY KEY (ID, NUM, COD) 
);

CREATE TABLE IF NOT EXISTS Entrega ( 
    Id_pedido INT, 
    Num INT, 
    CPF VARCHAR(11), 
    Codigo INT, 
    Status VARCHAR(20), 
    Data DATE,  -- SQLite não tem tipo DATE nativo
    CONSTRAINT pk_entrega PRIMARY KEY (Id_pedido, Num, CPF, Codigo), 
    CONSTRAINT fk_entrega_pedido FOREIGN KEY (Id_pedido, Num) REFERENCES Pedido(ID, NUM), 
    CONSTRAINT fk_entrega_motorista FOREIGN KEY (CPF) REFERENCES Motorista(CPF), 
    CONSTRAINT fk_entrega_transporte FOREIGN KEY (Codigo) REFERENCES Transporte(COD) 
);
""")

def is_revendedor_autorizado(id_cliente):
    """Verifica se o cliente é um revendedor autorizado (está na tabela RA)"""
    cursor.execute("SELECT 1 FROM RA WHERE ID = ?", (id_cliente,))
    return cursor.fetchone() is not None

# Função para inserir múltiplos registros (simulando INSERT ALL do Oracle)
def insert_all(table, columns, values_list):
    placeholders = ', '.join(['?'] * len(columns))
    query = f"INSERT INTO {table} ({', '.join(columns)}) VALUES ({placeholders})"
    cursor.executemany(query, values_list)

# Inserindo dados na tabela CLIENTE
clientes = [
    (1, 'João Silva', '11987654321', 'Rua das Flores, 123, São Paulo, SP'),
    (2, 'Maria Oliveira', '21988776655', 'Avenida Copacabana, 456, Rio de Janeiro, RJ'),
    (3, 'Carlos Pereira', '31999887766', 'Rua da Bahia, 789, Belo Horizonte, MG'),
    (4, 'Ana Costa', '51981234567', 'Avenida Ipiranga, 101, Porto Alegre, RS'),
    (5, 'Beatriz Souza', '71996543210', 'Rua do Carmo, 212, Salvador, BA'),
    (6, 'Cafeteria Sabor & Arte Ltda', '1145678901', 'Alameda Santos, 1500, São Paulo, SP'),
    (7, 'Empório Grão Nobre', '4133445566', 'Rua XV de Novembro, 300, Curitiba, PR'),
    (8, 'Mercado Central Comércio de Alimentos', '6132145678', 'Setor Comercial Sul, Quadra 2, Brasília, DF'),
    (9, 'Distribuidora Aroma do Campo', '8134567890', 'Avenida Boa Viagem, 550, Recife, PE'),
    (10, 'Padaria Doce Manhã Eireli', '2733221100', 'Rua Sete de Setembro, 80, Vitória, ES')
]
insert_all('CLIENTE', ['ID', 'NOME', 'FONE', 'ENDERECO'], clientes)

# Inserindo dados na tabela PF (Pessoa Física)
pf_data = [
    (1, '11122233344', '1985-05-20'),
    (2, '22233344455', '1990-11-15'),
    (3, '33344455566', '1978-02-10'),
    (4, '44455566677', '1995-07-30'),
    (5, '55566677788', '2000-01-05')
]
insert_all('PF', ['ID', 'CPF', 'DATA_NASC'], pf_data)

# Inserindo dados na tabela PJ (Pessoa Jurídica)
pj_data = [
    (6, 'Cafeteria Sabor & Arte Ltda', '11222333000144'),
    (7, 'Empório Grão Nobre e Cia', '22333444000155'),
    (8, 'Mercado Central Comércio de Alimentos S.A.', '33444555000166'),
    (9, 'Distribuidora Aroma do Campo Ltda', '44555666000177'),
    (10, 'Padaria Doce Manhã Eireli', '55666777000188')
]
insert_all('PJ', ['ID', 'RAZAO_SOCIAL', 'CNPJ'], pj_data)

# Inserindo dados na tabela RA (Representante Autônomo)
ra_data = [
    (3, 'REV-MG-001', 'Belo Horizonte e Região Metropolitana'),
    (4, 'REV-RS-001', 'Porto Alegre e Vale dos Sinos')
]
insert_all('RA', ['ID', 'COD_REV', 'AREA_COB'], ra_data)

# Inserindo dados na tabela MOTORISTA
motoristas = [
    ('12345678901', 'Roberto Dias', '123456789', '2020-03-15', None),
    ('23456789012', 'Fernanda Lima', '234567890', '2019-07-20', None),
    ('34567890123', 'Marcos Andrade', '345678901', '2021-01-10', '12345678901'),
    ('45678901234', 'Juliana Santos', '456789012', '2022-05-22', '23456789012'),
    ('56789012345', 'Ricardo Martins', '567890123', '2022-11-01', '12345678901'),
    ('67890123456', 'Laura Azevedo', '678901234', '2023-02-18', '23456789012'),
    ('78901234567', 'Bruno Carvalho', '789012345', '2023-06-30', '12345678901'),
    ('89012345678', 'Vanessa Rocha', '890123456', '2023-08-14', '23456789012'),
    ('90123456789', 'Felipe Barros', '901234567', '2024-01-20', '12345678901'),
    ('01234567890', 'Camila Neves', '012345678', '2024-03-05', '23456789012')
]
insert_all('MOTORISTA', ['CPF', 'NOME', 'CNH', 'DATA_CONTR', 'SUPERVISOR'], motoristas)

# Inserindo dados na tabela TRANSPORTE
transportes = [
    (10, 'Van de Carga', 1500, 'Branca', 'BRA1A23'),
    (20, 'Caminhão Leve', 4000, 'Prata', 'MER2B34'),
    (30, 'Fiorino', 650, 'Branca', 'SUL3C45'),
    (40, 'Caminhão Toco', 8000, 'Vermelho', 'BRA4D56'),
    (50, 'Van de Carga', 1500, 'Azul', 'MER5E67'),
    (60, 'Kombi Carga', 1000, 'Branca', 'SUL6F78'),
    (70, 'Caminhão Truck', 14000, 'Verde', 'BRA7G89'),
    (80, 'Fiorino', 650, 'Prata', 'MER8H90'),
    (90, 'Van de Carga', 1500, 'Preta', 'SUL9I01'),
    (100, 'Caminhão Leve', 4000, 'Amarelo', 'BRA0J12')
]
insert_all('TRANSPORTE', ['COD', 'TIPO', 'CAPACIDADE', 'COR', 'PLACA'], transportes)

# Inserindo dados na tabela CARACTERISTICA
caracteristicas = [
    (101, 'Cítrica Média', 'Média Clara', 'Leve', 'Média'),
    (102, 'Frutada Baixa', 'Escura', 'Encorpado', 'Grossa'),
    (103, 'Brilhante Alta', 'Média', 'Delicado', 'Fina'),
    (104, 'Equilibrada', 'Média', 'Cremoso', 'Média'),
    (105, 'Baixa', 'Clara', 'Suave', 'Média'),
    (106, 'Cítrica Alta', 'Média', 'Viloso', 'Fina'),
    (107, 'Achocolatada', 'Escura', 'Pesado', 'Grossa'),
    (108, 'Floral', 'Clara', 'Leve', 'Média'),
    (109, 'Caramelizada', 'Média Escura', 'Encorpado', 'Média'),
    (110, 'Suave', 'Média Clara', 'Aveludado', 'Fina')
]
insert_all('CARACTERISTICA', ['ID', 'ACIDEZ', 'TORRA', 'CORPO', 'MOAGEM'], caracteristicas)

# Inserindo dados na tabela CAFE
cafes = [
    (1001, 'Bourbon Amarelo', 'Fazenda Mantiqueira', 55.00, 101),
    (1002, 'Catuaí Vermelho', 'Sítio Caparaó', 75.50, 102),
    (1003, 'Geisha', 'Fazenda Esmeralda', 120.00, 103),
    (1004, 'Mundo Novo', 'Fazenda Cerrado Mineiro', 48.90, 104),
    (1005, 'Arábica Orgânico', 'Sítio Boa Esperança', 62.00, 105),
    (1006, 'Kona', 'Kona Coffee Farms', 150.75, 106),
    (1007, 'Robusta Especial', 'Plantação do Congo', 40.00, 107),
    (1008, 'Yirgacheffe', 'Cooperativa Etíope', 95.20, 108),
    (1009, 'Sul de Minas', 'Fazenda Santa Inês', 59.99, 109),
    (1100, 'Microlote Premiado', 'Sítio da Torre', 180.00, 110)
]
insert_all('CAFE', ['COD', 'NOME', 'FAZENDA', 'PRECO', 'ID'], cafes)

# Inserindo dados na tabela PROMOCAO
promocoes = [
    (1, 5.00),
    (2, 10.00),
    (3, 15.50),
    (4, 20.00),
    (5, 25.00),
    (6, 0.50),
    (7, 1.00),
    (8, 2.00),
    (9, 3.00),
    (10, 4.00)
]
insert_all('PROMOCAO', ['ID', 'VALOR'], promocoes)

# Inserindo dados na tabela PEDIDO
pedidos = [
    (1, 101, '2024-05-10', 110.00, 2, 0.00),
    (2, 102, '2024-05-12', 48.90, 1, 0.00),
    (6, 103, '2024-05-15', 370.00, 5, 25.00),
    (3, 104, '2024-06-01', 124.00, 2, 0.00),
    (7, 105, '2024-06-05', 489.00, 10, 0.00),
    (4, 106, '2024-06-20', 150.75, 1, 0.00),
    (8, 107, '2024-07-02', 119.98, 2, 0.00),
    (1, 108, '2024-07-11', 75.50, 1, 0.00),
    (9, 109, '2024-07-15', 200.00, 5, 0.00),
    (10, 110, '2024-07-22', 180.00, 1, 0.00)
]
for pedido in pedidos:
    id_cliente, num_pedido, data, preco_final, quant, desconto = pedido
    
    # Verifica se o desconto é válido (aprovado apenas para revendedores)
    if desconto > 0 and not is_revendedor_autorizado(id_cliente):
        print(f"AVISO: Cliente ID {id_cliente} não é revendedor autorizado. Desconto não aplicado.")
        desconto = 0.00  # Remove o desconto
    
    cursor.execute(
        "INSERT INTO PEDIDO (ID, NUM, DAT, PRECO_FINAL, QUANT, DESCONTO) VALUES (?, ?, ?, ?, ?, ?)",
        (id_cliente, num_pedido, data, preco_final, quant, desconto)
    )

# Inserindo dados na tabela TEM (itens do pedido)
tem_data = [
    (1, 101, 1001, 1),  # João comprou 2x Bourbon Amarelo
    (2, 102, 1004, 1),  # Maria comprou 1x Mundo Novo
    (6, 103, 1002, 9),  # Cafeteria Sabor & Arte comprou 5x Catuaí Vermelho
    (3, 104, 1005, None),  # Carlos comprou 2x Arábica Orgânico
    (7, 105, 1004, None),  # Empório Grão Nobre comprou 10x Mundo Novo
    (4, 106, 1006, None),  # Ana comprou 1x Kona
    (8, 107, 1009, None),  # Mercado Central comprou 2x Sul de Minas
    (1, 108, 1002, None),  # João fez outro pedido, 1x Catuaí Vermelho
    (9, 109, 1007, None),  # Distribuidora comprou 5x Robusta Especial
    (10, 110, 1100, None)  # Padaria comprou 1x Microlote Premiado
]
insert_all('TEM', ['ID', 'NUM', 'COD', 'ID_PROMO'], tem_data)

# Inserindo dados na tabela Entrega
entregas = [
    (1, 101, '12345678901', 30, 'Entregue', '2024-05-12'),
    (2, 102, '34567890123', 30, 'Entregue', '2024-05-14'),
    (6, 103, '23456789012', 20, 'Entregue', '2024-05-18'),
    (3, 104, '45678901234', 10, 'Entregue', '2024-06-03'),
    (7, 105, '56789012345', 40, 'Entregue', '2024-06-08'),
    (4, 106, '67890123456', 80, 'Em trânsito', '2024-06-21'),
    (8, 107, '78901234567', 10, 'Aguardando envio', '2024-07-03'),
    (1, 108, '89012345678', 30, 'Processando', '2024-07-12'),
    (9, 109, '90123456789', 50, 'Em trânsito', '2024-07-17'),
    (10, 110, '01234567890', 60, 'Entregue', '2024-07-25')
]
insert_all('Entrega', ['Id_pedido', 'Num', 'CPF', 'Codigo', 'Status', 'Data'], entregas)

# Implementação dos triggers (SQLite não suporta PL/SQL como no Oracle, então usamos triggers básicos)
cursor.executescript("""
CREATE TRIGGER IF NOT EXISTS disjuncao_pf
BEFORE INSERT ON PF
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN EXISTS (SELECT 1 FROM PJ WHERE ID = NEW.ID)
        THEN RAISE(ABORT, 'cliente já está em PJ.')
    END;
END;

CREATE TRIGGER IF NOT EXISTS disjuncao_pj
BEFORE INSERT ON PJ
FOR EACH ROW
BEGIN
    SELECT CASE
        WHEN EXISTS (SELECT 1 FROM PF WHERE ID = NEW.ID)
        THEN RAISE(ABORT, 'cliente já está em PF.')
    END;
END;
""")

# Commit das alterações e fechamento da conexão
conn.commit()
conn.close()

print("Banco de dados 'projeto_fisico.db' criado com sucesso!")
