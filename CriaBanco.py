import sqlite3 as conector
from modelos import Municipio, Dengue

conexao = None
cursor = None

try:
    conexao = conector.connect("bancoDengue2.db")
    conexao.execute("PRAGMA foreing_keys = on")
    cursor = conexao.cursor()

    comando = ''' CREATE TABLE municipio(
                    codigo INTEGER NOT NULL,
                    nome VARCHAR(50) NOT NULL,
                    PRIMARY KEY(codigo)
                    );'''

    cursor.execute(comando)

    comando = '''CREATE TABLE populacao (
                    codigo	INTEGER NOT NULL,
                    ano	INTEGER NOT NULL,
                    populacao	INTEGER NOT NULL DEFAULT 0,
                    FOREIGN KEY(codigo) REFERENCES municipio(codigo),
                    PRIMARY KEY(codigo, ano)
                );'''

    cursor.execute(comando)

    comando = ''' CREATE TABLE dengue (
                    codigo INTEGER NOT NULL,
                    ano	INTEGER NOT NULL,
                    casos INTEGER NOT NULL,
                    FOREIGN KEY(codigo) REFERENCES municipio(codigo),
                    PRIMARY KEY(codigo,ano)
                );'''

    cursor.execute(comando)

    conexao.commit()


except conector.OperationalError as erro:
    print("Erro Operacional", erro)

except conector.DatabaseError as erro:
    print("Erro de Banco de Dados", erro)

finally:
    if cursor:
        cursor.close()
    if conexao:
        conexao.close()
