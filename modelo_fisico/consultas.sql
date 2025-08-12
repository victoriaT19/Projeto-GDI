--  Clientes (PJ) com valor total de pedidos maior que R$ 300
SELECT c.NOME AS NomeCliente,SUM(p.PRECO_FINAL) AS TotalPedidos
FROM CLIENTE c
JOIN PEDIDO p ON c.ID = p.ID
WHERE c.ID IN (SELECT ID FROM PJ)
GROUP BY c.NOME
HAVING SUM(p.PRECO_FINAL) > 300;

-- Pergunta: Listar cafés e suas características (torra, corpo, acidez).
SELECT ca.nome, ca.fazenda, car.torra, car.corpo, car.acidez
FROM cafe ca
INNER JOIN caracteristica car ON ca.id = car.id;

-- Pergunta: Listar todas as entregas e o transporte utilizado (se houver)
SELECT e.Id_pedido, e.Num, e.Status AS StatusEntrega, t.TIPO AS TipoTransporte, t.PLACA AS PlacaTransporte
FROM
   Entrega e
LEFT JOIN
   TRANSPORTE t ON e.Codigo = t.COD;

-- Pergunta: Listar os clientes que já fizeram pedidos.
SELECT DISTINCT c.nome
FROM cliente c
WHERE c.id IN (
    SELECT p.id
    FROM pedido p 
);

-- Pergunta: Listar os clientes que nunca fizeram pedidos.
SELECT c.nome
FROM cliente c
WHERE NOT EXISTS (
    SELECT 1
    FROM pedido p
    WHERE p.id = c.id
);

-- Café mais caro
SELECT Nome, Preco_Kg
FROM Cafe
WHERE Preco_Kg = (
    SELECT Preco_Kg
    FROM Cafe
    where nome = 'banana'
);


-- Café mais barato (linha completa)
SELECT *
FROM Cafe c
WHERE (c.Preco_Kg, c.Cod) in (
    SELECT Preco_Kg, Cod
    FROM Cafe
    ORDER BY Preco_Kg ASC
    LIMIT 1
);



-- Lista de cafés acima da média de preço
SELECT *
FROM (
    SELECT Cod, Nome, Preco_Kg
    FROM Cafe
) AS tabela_cafe
WHERE Preco_Kg > (
    SELECT AVG(Preco_Kg) FROM Cafe
);

-- Lista de clientes (PF e PJ) com seus nomes
SELECT nome
FROM cliente c
JOIN pf ON c.id = pf.id
UNION ALL
SELECT razao_social
FROM cliente c
JOIN pj ON c.id = pj.id;
