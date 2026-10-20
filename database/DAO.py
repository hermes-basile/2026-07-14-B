from database.DB_connect import DBConnect
from model.film import Film


class DAO:
    @staticmethod
    def getAllNodes():
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct m.id ,m.title , m.year, r.avg_rating 
                    from movie m 
                    join genre g on m.id  = g.movie_id 
                    left join ratings r on m.id =r.movie_id 

                """

        cursor.execute(query)

        for row in cursor:
            results.append(
                Film(
                    id=row["id"],
                    title =row["title"],
                    year=row["year"],
                    avg_rating=row["avg_rating"]
                )
            )

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getNodi(genere):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct g.movie_id  
                    from genre g
                    left join ratings r  on g.movie_id = r.movie_id 
                    join role_mapping rm on g.movie_id = rm.movie_id 
                    where  g.genre = %s
                    and (rm.category = 'actor' or rm.category = 'actress' )
                   """

        cursor.execute(query, (genere,))

        for row in cursor:
            results.append(
                row["movie_id"]
            )

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def fillAttori(film_oggetto):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct rm.name_id as id
                    from role_mapping rm 
                    where rm.movie_id = %s
                    and (rm.category = 'actor' or rm.category = 'actress' )
                       """

        cursor.execute(query,(film_oggetto.id,))

        for row in cursor:
            results.append(
                row["id"]
            )

        cursor.close()
        conn.close()
        film_oggetto.lista_attori = results

    @staticmethod
    def getAllGeneri():
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct g.genre 
                    from genre g 

                   """

        cursor.execute(query)

        for row in cursor:
            results.append(row["genre"]

            )

        cursor.close()
        conn.close()
        return results
