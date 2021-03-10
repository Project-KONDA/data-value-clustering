from data_extraction import read_data_values_from_file

midas_artist_names_expecation_10000 = [
    [
        "---",
    ],
    [
        "Meister der Virgo inter virgines",
        "Meister der weiblichen Halbfiguren",
        "Meister des Kreuzigungsaltars in der Dortmunder Marienkirche",
        "Meister von Liesborn",
        "Meister H B mit dem Greifenkopf",
        "Long-nose-Maler",
        "Castellani-Maler",
        "Club-foot-Töpfer",
        "Kopenhagener Kopf-Maler",
        "Angeluccio",
        "Rembrandt",
        "Duris",
        "Euphronios",
        "Psiax",
        "Lydos",
        "Girolamo di Benvenuto di Giovanni del Guasta",
        "Monogrammist A R F",
        "Macrino d'Alba",
    # ],
    # [
        "Maler von London B 76",
        "Maler von London B 174",
        "Maler von Louvre F 161",
        "Maler von Istanbul 7314",
        "Maler von Berlin 1659",
    ],
    [
        "Daubigny, Charles-Franc^B8ois",
        "Troy, Jean Franc^B8ois de",
        "Née, Franc^B8ois Denis",
        "Diaz de la Pen^B5a, Narcisse Virgilio",
        "Achenbach, Andreas",
        "Bastiné, Jean-Baptiste Joseph",
        "Ravesteyn, Jan Anthonisz van",
        "Arthois, Jacques d'",
        "Eeckhout, Gerbrand van den",
        "Marseus van Schrieck, Evert",
        "Cornelisz van Haarlem, Cornelis",
        "Velázquez, Diego Rodríguez de Silva y",
        "Arthois, Jacques d'",
        "Dielmann, Jakob Fürchtegott",
        "Goya y Lucientes, Francisco José de",
        "Landi, Neroccio di Bartolomeo di Benedetto de'",
        "Wildungen, Ludwig Karl Eberhard Heinrich Friedrich von",
        "Pollaiuolo, Piero di Jacopo d'Antonio Benci del",
        "Toulouse-Lautrec, Henri de",
    # ],
    # [
        "Brekelenkam, Quiringh Gerritsz. van",
        "Heem, Jan Davidsz. de",
        "Droochsloot, Joost Cornelisz.",
        "Herdincg, Hermann A.",
        "Daunel, E.",
        "Codde, Pieter Jacobsz.",
        "Cuyp, Aelbert Jacobsz.",
    # ],
    # [
        "Müller, J. A.",
    ],
    [
        "Pourbus, ?",
        "Schumacher, ?",
    ],
    [
        "Meister von 1462 (Kupferstecher)",
    ],
    [
        "Angelico (Fra)",
    ],
    [
        "Nikosthenes (550ante)",
    ],
    [
        "Monogrammist A B (1731)",
        "Monogrammist A H (1546)",
        "Python (2)",
        "Gérard, Franc^B8ois (1770-1837)",
    ],
    [
        "Bouts, Dierick (1415)",
        "Hals, Frans (1582)",
        "Hondt, Lambert de (1620)",
        "Jordaens, Jacob (1)",
        "Santacroce, Francesco di Simone da (1)",
        "Claesz., Pieter (1597)",
        "Mo^BEller, Andreas (1684)",
        "Millet, Jean Franc^B8ois (1)",
    ],
    [
        "Cranach, Lucas (der Ältere)",
        "Balen, Hendrick van (der Ältere)",
        "Bassano, Francesco (der Jüngere)",
        "Lippi, Filippo (Fra)",
        "Pickenhahn, J. C. F. (Sohn)",
    ],
    [
        "Miller, ? (1868)",
    ],
    [
        "Brueghel, ? (?)",
    ],
    [
        "Friedrich (Preußen, König, 2, der Große)",
    ]
]


if __name__ == '__main__':
    path = "..\..\data\midas_artist_names.txt"
    file = read_data_values_from_file(path)
    for list in midas_artist_names_expecation_10000:
        for v in list:
            if not (v in file):
                print(v)
