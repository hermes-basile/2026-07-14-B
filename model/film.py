from dataclasses import dataclass, field


@dataclass
class Film:
    id : str
    title : str
    year : int
    avg_rating : float

    lista_attori: list = field(default_factory=list)


    def __hash__(self):
        return hash(self.id)

    def __str__(self):
        return f"{self.title} dell'anno '{self.year}'"

    def __eq__(self, other):
        return self.id == other.id

    def numero_attori_recitanti(self):
        return len(self.lista_attori)