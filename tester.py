from model.model import Model
modello_prova = Model()

print(f"La lista che contiene tutti i nodi (non filtrati) è lunga: {len(modello_prova.lista_nodi_totale)}")
#creo il grafo:
modello_prova.crea_grafo("Drama")
print(f"Il grafo ha {modello_prova.num_nodi()} nodi, e {modello_prova.num_archi()} archi")
lista_nodi = modello_prova.return_lista_nodi()
for film in lista_nodi:
    if film.year != 2017 and film.year != 2018 and film.year != 2019  and film.year != 2020:

        print(film)
#for film in lista_nodi:
 #   print(film.lista_attori)

#print(modello_prova.film_maggiore_archi_uscenti())
#print(modello_prova.componente_connessa_maggiore_numero())
#print(modello_prova.info_componente_connessa_maggiore())
film1 = lista_nodi[0]

print(modello_prova.crea_ricorsione(film1, 2))
