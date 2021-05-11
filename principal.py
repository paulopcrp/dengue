import sqlite3 as conector
from modelos import Municipio, Dengue

conexao = None
cursor = None

try:
    conexao = conector.connect("bancoDengue2.db")
    conexao.execute("PRAGMA foreing_keys = on")
    cursor = conexao.cursor()

    with open("dengue_MG.csv", encoding="utf8") as arquivo:
        arquivo.readline()
        for linha in arquivo:
            codigo, nome, casos_2018, casos_2019 = linha.strip().split(';')
            print(codigo, nome, casos_2018, casos_2019)

            municipio = Municipio(codigo, nome)
            comando = '''INSERT INTO municipio VALUES (:codigo, :nome);'''
            cursor.execute(comando, vars(municipio))

            dengue_2018 = Dengue(codigo, 2018, int(casos_2018))
            dengue_2019 = Dengue(codigo, 2019, int(casos_2019))
            comando = '''INSERT INTO dengue VALUES (:codigo, :ano, :casos);'''
            cursor.execute(comando, vars(dengue_2018))
            cursor.execute(comando, vars(dengue_2019))

    with open("populacao.csv", encoding="utf8") as arquivo:
        arquivo.readline()
        for linha in arquivo:
            codigo, nome, pop_2018, pop_2019 = linha.strip().split(';')
            print(codigo, nome, pop_2018, pop_2019)
            comando = '''INSERT INTO populacao VALUES (?, ?, ?);'''
            cursor.execute(comando, (codigo, 2018, pop_2018))
            cursor.execute(comando, (codigo, 2019, pop_2019))

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
