lido_titles_1000_expectation_v3_complete = [

    # normal title and uncertain title
    ["Die vier Evangelisten",
     "Die Fußoperation",
     "Via San Giovanni in Laterano mit Blick auf das Kolosseum",
     "Bildnis einer Frau mit Panther-Katze",
     "Bildnis des Schreib- und Rechenmeisters Lieven Willemsz van Coppenol",
     "Linné als Knabe",
     "Pendants?",
     "Eine Räuberhöhle?",
     "Partie an der Mosel?",
     "Allegorie des Herbstes?",
     "Hirte 2",
     "Der Canal Grande mit der Ca'Foscari und dem Palazzo Balbi"],

    ["Bildnis des Landgrafen Wilhelm 6.",
     "König Friedrich Wilhelm 3. als Kind",
     "Wilhelm 1. von Oranien-Nassau",
     "Bildnis Cosimos 1., Großherzog von Toskana",
     "Gustav 3., König von Schweden",
     "Allegorie. Der Bettel sitzt der Hoffahrt auf der Schleppe"],

    # comma -> extra information
    ["Diana mit Nymphen, im Schlafe von Satyrn belauscht",
     "Italienische Landschaft mit Jägern, Landleuten und Herde",
     "Philibert, Prince de Savoye-Carignan",
     "Venus, Amor, Bacchus und Ceres",
     "Fünfzehn Ansichten aus München, in der Mitte der Marienplatz",
     "Florenz, Blick von San Miniato auf die Stadt",
     "Bildnis eines Jünglings, angeblich des Landgrafen Wilhelms 6. von Hessen",
     "Allegorie der Malerei und der Bildhauerei mit dem Bildnis ihres Beschützers, des Landgrafen Friedrich 2. von Hessen"],

    # semi-colon -> extra information
    ["Triptychon mit der Darstellung des Schmerzensmannes zwischen Maria und Johannes; auf den Flügeltafeln der heilige Andreas und die heilige Katharina",
     "Hafen mit ankernden Schiffen &amp; Stille See"],

    # minus -> part
    ["Flügelaltärchen — Mittelbild",
     "Altartafel mit der Kreuzigung und Szenen der Marienlegende — Christus am Kreuz",
     "Diptychon — Verkündigung",
     "Zwei Landschaften — Landschaft mit Aufrichtung eines antiken Grabmals",
     "Kasseler Auferstehungsaltärchen — Wappen Mecklenburgs",
     "Rembrandts Eltern — Rembrandts Vater",
     "Die Verkündigung an Maria —",
     "Vor dem Tore einer befestigten Stadt —",
     "Das Innere der Kathedrale von Antwerpen —",
     "Die niederländischen Sprichwörter — Er hat es faustdick hinter den Ohren?",
     "Triptychon mit der Darstellung des Schmerzensmannes zwischen Maria und Johannes; auf den Flügeltafeln der heilige Andreas und die heilige Katharina — Schmerzensmann",
     "Flügelaltärchen mit der Darstellung der Kreuztragung, Kreuzigung und Kreuzabnahme — Kreuzabnahme",
     "Doppelbildnis eines Ehepaares von Weinsberg — Gottschalk von Weinsberg — originaler Rahmen"],

    # minus and comma -> part
    ["Die niederländischen Sprichwörter — Es ist nichts so fein gesponnen, es kommt doch an die Sonnen",
     "Die niederländischen Sprichwörter — Die Reise ist noch nicht zu End', wenn man Kirch' und Turm erkennt",
     "Die niederländischen Sprichwörter — Wer weiß, warum die Gänse barfuß gehen und Bin ich zum Gänsehüten nicht berufen, so laß ich Gänse Gänse sein",
     "Die niederländischen Sprichwörter — Die eine rocknet, was die andere spinnt und Paß' auf, daß kein schwarzer Hund dazwischen kommt",
     "Die niederländischen Sprichwörter — Scher' sie, aber schinde sie nicht",
     "Die niederländischen Sprichwörter — Laß' ein Ei im Nest",
     "Doppelbildnis eines Ehepaares von Weinsberg — Elisabeth von Weinsberg, geb. Horns"],

    ["Doppelbildnis eines Ehepaares von Weinsberg — Elisabeth von Weinsberg, geb. Horns — originaler Rahmen"],

    # space and minus -> extra information for part
    ["Die fünf Sinne — Der Geruch (Selbstporträt)",
     "Die Verkündigung an Maria — Schauseite (erste)",
     "Kasseler Auferstehungsaltärchen — Schauseite (zweite)",
     "Die niederländischen Sprichwörter — Läßt man den Hund herein, so kriecht er in den (Topf) Schrank",
     "Die niederländischen Sprichwörter — Zwei Hunde an einem Bein (Knochen) kommen selten überein"],

    # brackets -> uncertainty, extra info or language variant
    ["Bildnis einer Dame (Luise Henriette von Oranien?)",
     "Bildnis eines Architekten (Apostel Thomas?)",
     "Landleute bei der Mahlzeit auf dem Feld (Kopie)",
     "Das Mädchen mit dem Spiegel (Allegorie der Vanitas)",
     "Christus erscheint Maria Magdalena als Gärtner (Noli me tangere)",
     "Das Innere der (abgebrochenen) Sankt Marienkirche zu Utrecht",
     "Die Predigt Johannes des Täufers (\"Ecce Agnus Dei\")"],

    # special characters in brackets -> uncertainty, extra info
    ["Die Kartenspieler (oder: Lagerszene; Rast der Soldaten)"],

    # brackets with numbers at end -> birth and death dates
    ["Porträt des Joseph Rinald (1735-1811)",
     "Der Kosmograph Sebastian Münster (1489-1552)",
     "Kaiser Karl V. (1500-1558)",
     "Giuliano de'Medici (1453-1478)"],

    # numbers -> dating info
    ["Komposition 1923 V",
     "Bildnis eines Mannes von 35-40 Jahren",
     "Dorfszene im Winter 1828"],

    # dot and numbers -> dating info
    ["Doppelporträt zweier Ärzte als Heilige Cosmas und Damian. Um 1623/26"],

    # slash -> alternatives or language variants
    ["Die Versucherin / Allegorie der Vanitas",
     "Der lustige Zecher / Herr Peeckelhaering",
     "Angebliches Bildnis des Don Carlos / Bildnis eines Hofzwerges",
     "Die Briefsieglerin / Une femme occupée à cacheter une lettre",
     "Rückkehr vom Markt / Die Köchin / La pourvoyeuse"],

]  # n = 14

if __name__ == "__main__":
    print(len(lido_titles_1000_expectation_v3_complete))
