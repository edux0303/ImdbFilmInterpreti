from database.DB_connect import DBConnect
from model.movie import Movie


"""
IMDB: FILM E INTERPRETI

Si consideri il database "imdb", contenente informazioni su film (movie),
valutazioni (ratings), generi (genre), anagrafica di interpreti e registi
(names) e le relative associazioni ai film tramite ruolo (role_mapping).
Si intende costruire un'applicazione che permetta di analizzare le relazioni
tra film di uno stesso genere in base agli interpreti che hanno in comune.

PUNTO 1
a. L'utente seleziona da un menu a tendina un genere tra quelli presenti nella
   tabella genre, in ordine alfabetico, e inserisce in un campo di testo un
   numero minimo di voti V. Il campo deve mostrare come valore di default 10000.

b. Premendo "Crea grafo", l'applicazione costruisce un grafo semplice, non
   orientato e pesato. I vertici sono i film del genere selezionato che hanno
   ricevuto almeno V voti (campo total_votes della tabella ratings).
   SUGGERIMENTO. Per ogni film puo' risultare conveniente aggiungere alla
   relativa classe il titolo, l'anno, il voto medio (avg_rating), il numero di
   voti e l'insieme dei suoi interpreti (attori e attrici, cioe' role_mapping
   con category uguale a 'actor' oppure 'actress').

c. Esiste un arco tra due film distinti F1 e F2 se hanno almeno un interprete
   in comune. Il peso dell'arco e' il numero di interpreti in comune.
   Costruito il grafo, l'applicazione visualizza il numero di vertici e di
   archi.

d. Alla pressione del tasto "Stampa dettagli", il programma dovra':
   - stampare i tre archi di peso maggiore; a parita' di peso, in ordine
     alfabetico sul primo film e poi sul secondo;
   - stampare il numero di componenti connesse;
   - identificare la componente connessa di dimensione maggiore e stamparne
     tutti i film, ordinati in senso decrescente secondo il grado; a parita'
     di grado, in ordine alfabetico.
   NOTA. I film vanno visualizzati come "Titolo (anno)", perche' nel database
   esistono titoli uguali per film diversi.

PUNTO 2
a. L'utente seleziona da un menu a tendina un film di partenza tra quelli
   presenti nel grafo.

b. Premendo "Cerca percorso", l'applicazione determina, mediante un algoritmo
   ricorsivo, un cammino semplice che:
   - parta dal film selezionato;
   - attraversi gli archi del grafo;
   - non passi piu' volte dallo stesso film;
   - sia tale che ogni film successivo abbia un voto medio STRETTAMENTE
     MAGGIORE del precedente;
   - contenga il MASSIMO NUMERO DI FILM possibile; a parita' di numero di
     film, si scelga il cammino con la SOMMA DEI VOTI ricevuti (total_votes)
     massima.

c. L'applicazione stampa i film del cammino nell'ordine in cui sono
   attraversati, ciascuno con il suo voto medio, poi il numero di film e la
   somma dei voti ricevuti. Se dal film di partenza non si puo' raggiungere
   nessun film con voto medio maggiore, va mostrato un messaggio.

"""
class DAO:
    @staticmethod
    def getAllGeneri():
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
            SELECT DISTINCT genre AS genere
            FROM genre
            ORDER BY genre"""

        cursor.execute(query)

        for row in cursor:
            results.append(row["genere"])

        cursor.close()
        conn.close()
        return results

    @staticmethod
    def getNodes(genere,minimo):
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT m.id AS id, m.title AS titolo, m.year AS anno, r.avg_rating AS media, r.total_votes AS voti
                FROM movie m, ratings r, genre g
                WHERE m.id = r.movie_id AND g.movie_id = m.id AND  g.genre = %s AND r.total_votes >= %s 
                ORDER BY m.id"""

        cursor.execute(query,(genere,minimo))
        for row in cursor:
            results.append(Movie(row["id"],row["titolo"],int(row["anno"]),float(row["media"]),row["voti"]))
        cursor.close()
        conn.close()
        return results
    @staticmethod
    def getInterpreti():
        conn = DBConnect.get_connection()
        results = []

        cursor = conn.cursor(dictionary=True)
        query = """
                SELECT r.movie_id AS idFilm, r.name_id AS idRuolo
                FROM role_mapping r
                WHERE r.category= "actor" or r.category = "actress"
                """

        cursor.execute(query)
        for row in cursor:
            results.append((row["idFilm"],row["idRuolo"]))
        cursor.close()
        conn.close()
        return results


