import sqlite3 as conector
import pandas

conexao = None
cursor = None

try:
    conexao = conector.connect("bancoDengue2.db")
    conexao.execute("PRAGMA foreing_keys = on")
    cursor = conexao.cursor()

    comando = ''' SELECT municipio.nome, dengue.casos, populacao.populacao
                    FROM municipio
                    JOIN dengue ON municipio.codigo = dengue.codigo
                    JOIN populacao ON municipio.codigo = populacao.codigo
                    WHERE dengue.ano=:ano AND populacao.ano=:ano'''

    ano = {"ano": 2019}

    cursor.execute(comando, ano)

    #recuperando os registros
    registros = cursor.fetchall()
 #   print(registros[0])
 #   print(f'{"município":30} - {"casos":6} - {"populacao":9} - {"incidencia"}')
 #   for registro in registros:
 #       incidencia = registro[1] / registro[2]
 #       print(f'{registro[0]:30} - {registro[1]:5} - {registro[2]:9} - {incidencia:.6f}')

    resultado = pandas.read_sql(sql=comando, con=conexao, params=ano)
    resultado['incidencia'] = 100 * (resultado['casos'] / resultado['populacao'])
    print(resultado)
    print(resultado['incidencia'].describe())

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
