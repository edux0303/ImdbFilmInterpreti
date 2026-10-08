from dataclasses import dataclass, field


@dataclass
class Movie:
    id: str                                         # es. "tt4975722": è una stringa, non un numero
    title: str
    year: int
    avg_rating: float                               # voto medio, da ratings
    total_votes: int                                # numero di voti, da ratings
    interpreti: set = field(default_factory=set)    # id degli attori e attrici del film

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return isinstance(other, Movie) and self.id == other.id

    def __str__(self):
        return f"{self.title} ({self.year})"