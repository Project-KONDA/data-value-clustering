lido_titles_1000_expectation = [

    # normal title (may contain numbers, dot and minus)
    ["Die vier Evangelisten",
     # "Die beiden Seifenbläser",
     # "Lob des Herings",
     "Die Fußoperation",
     "Via San Giovanni in Laterano mit Blick auf das Kolosseum",
     # "Familienbildnis bei der silbernen Hochzeit der Familie Neuß",
     "Bildnis eines Mannes von 35-40 Jahren",
     "Bildnis des Landgrafen Wilhelm 6.",
     # "Bildnis Papst Clemens 9.",
     "König Friedrich Wilhelm 3. als Kind",
     "Wilhelm 1. von Oranien-Nassau",
     # "Kurfürst Wilhelm 2. von Hessen-Kassel als Kurprinz",
     "Bildnis einer Frau mit Panther-Katze",
     # "Landgraf Karl von Hessen-Kassel und seine Familie",
     "Bildnis des Schreib- und Rechenmeisters Lieven Willemsz van Coppenol",
     "Linné als Knabe"],

    # comma -> extra information
    ["Bildnis Cosimos 1., Großherzog von Toskana",
     "Diana mit Nymphen, im Schlafe von Satyrn belauscht",
     "Italienische Landschaft mit Jägern, Landleuten und Herde",
     "Allegorie der Malerei und der Bildhauerei mit dem Bildnis ihres Beschützers, des Landgrafen Friedrich 2. von Hessen",
     # "Selbstbildnis, der Künstler mit seiner Familie",
     "Bildnis eines Jünglings, angeblich des Landgrafen Wilhelms 6. von Hessen",
     "Philibert, Prince de Savoye-Carignan",
     "Gustav 3., König von Schweden",
     # "Arkadische Landschaft, im Vordergrund Jüngling mit rotem Mantel",
     # "Bildnis der Saskia van Uylenburgh im Profil, in reichem Kostüm",
     # "Südliche Landschaft mit Herde, Hirtin und Knabe",
     "Venus, Amor, Bacchus und Ceres",
     "Fünfzehn Ansichten aus München, in der Mitte der Marienplatz",
     # "Gräfin Ernst Harrach, geborene Dittrichstein",
     "Florenz, Blick von San Miniato auf die Stadt"],  # -

    # space minus space -> part
    ["Flügelaltärchen — Mittelbild",
     # "Flügelaltärchen — Altarflügel",
     "Altartafel mit der Kreuzigung und Szenen der Marienlegende — Christus am Kreuz",
     "Diptychon — Verkündigung",
     "Zwei Landschaften — Landschaft mit Aufrichtung eines antiken Grabmals",
     # "Zwei Musiker — Geigenspieler mit Glas",
     "Kasseler Auferstehungsaltärchen — Wappen Mecklenburgs",
     "Rembrandts Eltern — Rembrandts Vater"],

    # space minus space ... space minus space -> part of part?
    ["Doppelbildnis eines Ehepaares von Weinsberg — Gottschalk von Weinsberg — originaler Rahmen",
     "Doppelbildnis eines Ehepaares von Weinsberg — Elisabeth von Weinsberg, geb. Horns — originaler Rahmen"],

    # # dot
    # # TODO
    # ["Doppelbildnis eines Ehepaares von Weinsberg — Elisabeth von Weinsberg, geb. Horns"],

    # # dot
    # # TODO
    # ["Allegorie. Der Bettel sitzt der Hoffahrt auf der Schleppe"],

    # semi-colon -> extra info
    ["Triptychon mit der Darstellung des Schmerzensmannes zwischen Maria und Johannes; auf den Flügeltafeln der heilige Andreas und die heilige Katharina — Schmerzensmann"],

    # space minus space ... brackets -> extra information for part
    ["Die fünf Sinne — Der Geruch (Selbstporträt)",
     "Die Verkündigung an Maria — Schauseite (erste)",
     "Kasseler Auferstehungsaltärchen — Schauseite (zweite)"],

    # space minus -> whole
    ["Die Verkündigung an Maria —",
     "Vor dem Tore einer befestigten Stadt —",
     "Das Innere der Kathedrale von Antwerpen —"],

    # brackets -> uncertainty, extra info or language variant
    # TODO: maybe split
    ["Bildnis einer Dame (Luise Henriette von Oranien?)",
     "Die Kartenspieler (oder: Lagerszene; Rast der Soldaten)",
     "Bildnis eines Architekten (Apostel Thomas?)",
     "Landleute bei der Mahlzeit auf dem Feld (Kopie)",
     "Das Mädchen mit dem Spiegel (Allegorie der Vanitas)",
     "Die Predigt Johannes des Täufers (\"Ecce Agnus Dei\")",
     "Christus erscheint Maria Magdalena als Gärtner (Noli me tangere)"],

    # brackets in text -> normal
    # TODO
    ["Das Innere der (abgebrochenen) Sankt Marienkirche zu Utrecht"],

    # space minus space ... brackets in text ->
    # TODO
    ["Die niederländischen Sprichwörter — Läßt man den Hund herein, so kriecht er in den (Topf) Schrank",
     "Die niederländischen Sprichwörter — Zwei Hunde an einem Bein (Knochen) kommen selten überein"],

    # question mark at end -> uncertain
    ["Pendants?",
     "Eine Räuberhöhle?",
     "Partie an der Mosel?",
     "Allegorie des Herbstes?"],

    # space minus space ... question mark at end -> part uncertain
    ["Die niederländischen Sprichwörter — Er hat es faustdick hinter den Ohren?"],

    # brackets with numbers at end -> birth and death dates
    ["Porträt des Joseph Rinald (1735-1811)",
     "Der Kosmograph Sebastian Münster (1489-1552)",
     "Kaiser Karl V. (1500-1558)",
     "Giuliano de'Medici (1453-1478)"],

    # numbers -> dating info
    ["Komposition 1923 V",
     "Dorfszene im Winter 1828",
     "Doppelporträt zweier Ärzte als Heilige Cosmas und Damian. Um 1623/26"],

    # number at end
    # TODO
    ["Hirte 2"],

    # space slash space -> alternatives or language variants
    ["Die Versucherin / Allegorie der Vanitas",
     # "Antiochos und Stratonike / Der kranke Königssohn",
     "Der lustige Zecher / Herr Peeckelhaering",
     # "Das Kartenspielchen / Soldat und Dirne",
     # "Das lustige Paar / Satyr mit Nymphe",
     "Angebliches Bildnis des Don Carlos / Bildnis eines Hofzwerges",
     "Die Briefsieglerin / Une femme occupée à cacheter une lettre"],

    # space slash space ... space slash space -> alternatives or language variants
    ["Rückkehr vom Markt / Die Köchin / La pourvoyeuse"],

] # n = 17

lido_titles_1000_expectation_v2 = [

    # normal title (may contain numbers, dot and minus)
    ["Die vier Evangelisten",
     # "Die beiden Seifenbläser",
     # "Lob des Herings",
     "Die Fußoperation",
     "Via San Giovanni in Laterano mit Blick auf das Kolosseum",
     # "Familienbildnis bei der silbernen Hochzeit der Familie Neuß",
     # "Bildnis Papst Clemens 9.",
     # "Kurfürst Wilhelm 2. von Hessen-Kassel als Kurprinz",
     "Bildnis einer Frau mit Panther-Katze",
     # "Landgraf Karl von Hessen-Kassel und seine Familie",
     "Bildnis des Schreib- und Rechenmeisters Lieven Willemsz van Coppenol",
     "Linné als Knabe",
     "Pendants?",
     "Eine Räuberhöhle?",
     "Partie an der Mosel?",
     "Allegorie des Herbstes?",
     "Hirte 2"],

    ["Bildnis des Landgrafen Wilhelm 6.",
     "König Friedrich Wilhelm 3. als Kind",
     "Wilhelm 1. von Oranien-Nassau",
     "Bildnis Cosimos 1., Großherzog von Toskana",
     "Gustav 3., König von Schweden"],

    # comma -> extra information
    ["Diana mit Nymphen, im Schlafe von Satyrn belauscht",
     "Italienische Landschaft mit Jägern, Landleuten und Herde",
     # "Selbstbildnis, der Künstler mit seiner Familie",
     "Philibert, Prince de Savoye-Carignan",
     # "Arkadische Landschaft, im Vordergrund Jüngling mit rotem Mantel",
     # "Bildnis der Saskia van Uylenburgh im Profil, in reichem Kostüm",
     # "Südliche Landschaft mit Herde, Hirtin und Knabe",
     "Venus, Amor, Bacchus und Ceres",
     "Fünfzehn Ansichten aus München, in der Mitte der Marienplatz",
     # "Gräfin Ernst Harrach, geborene Dittrichstein",
     "Florenz, Blick von San Miniato auf die Stadt"],  # -

    ["Bildnis eines Jünglings, angeblich des Landgrafen Wilhelms 6. von Hessen",
     "Allegorie der Malerei und der Bildhauerei mit dem Bildnis ihres Beschützers, des Landgrafen Friedrich 2. von Hessen"],

    # space minus space -> part
    ["Flügelaltärchen — Mittelbild",
     # "Flügelaltärchen — Altarflügel",
     "Altartafel mit der Kreuzigung und Szenen der Marienlegende — Christus am Kreuz",
     "Diptychon — Verkündigung",
     "Zwei Landschaften — Landschaft mit Aufrichtung eines antiken Grabmals",
     # "Zwei Musiker — Geigenspieler mit Glas",
     "Kasseler Auferstehungsaltärchen — Wappen Mecklenburgs",
     "Rembrandts Eltern — Rembrandts Vater",
     "Die Verkündigung an Maria —",
     "Vor dem Tore einer befestigten Stadt —",
     "Das Innere der Kathedrale von Antwerpen —",
     "Die niederländischen Sprichwörter — Er hat es faustdick hinter den Ohren?"],

    # space minus space ... space minus space -> part of part?
    ["Triptychon mit der Darstellung des Schmerzensmannes zwischen Maria und Johannes; auf den Flügeltafeln der heilige Andreas und die heilige Katharina — Schmerzensmann"],

    ["Doppelbildnis eines Ehepaares von Weinsberg — Gottschalk von Weinsberg — originaler Rahmen",],

    ["Doppelbildnis eines Ehepaares von Weinsberg — Elisabeth von Weinsberg, geb. Horns — originaler Rahmen"],

    # # dot
    # # TODO
    # ["Doppelbildnis eines Ehepaares von Weinsberg — Elisabeth von Weinsberg, geb. Horns"],

    # # dot
    # # TODO
    # ["Allegorie. Der Bettel sitzt der Hoffahrt auf der Schleppe"],



    # space minus space ... brackets -> extra information for part
    # space minus space ... brackets in text ->
    ["Die fünf Sinne — Der Geruch (Selbstporträt)",
     "Die Verkündigung an Maria — Schauseite (erste)",
     "Kasseler Auferstehungsaltärchen — Schauseite (zweite)",
     "Die niederländischen Sprichwörter — Läßt man den Hund herein, so kriecht er in den (Topf) Schrank",
     "Die niederländischen Sprichwörter — Zwei Hunde an einem Bein (Knochen) kommen selten überein"],

    # space minus -> whole


    # brackets -> uncertainty, extra info or language variant
    # TODO: maybe split
    ["Bildnis einer Dame (Luise Henriette von Oranien?)",
     "Bildnis eines Architekten (Apostel Thomas?)",
     "Landleute bei der Mahlzeit auf dem Feld (Kopie)",
     "Das Mädchen mit dem Spiegel (Allegorie der Vanitas)",
     "Christus erscheint Maria Magdalena als Gärtner (Noli me tangere)",
     "Das Innere der (abgebrochenen) Sankt Marienkirche zu Utrecht"],

    ["Die Predigt Johannes des Täufers (\"Ecce Agnus Dei\")"],

    ["Die Kartenspieler (oder: Lagerszene; Rast der Soldaten)"],



    # question mark at end -> uncertain
    # space minus space ... question mark at end -> part uncertain

    # brackets with numbers at end -> birth and death dates
    ["Porträt des Joseph Rinald (1735-1811)",
     "Der Kosmograph Sebastian Münster (1489-1552)",
     "Kaiser Karl V. (1500-1558)",
     "Giuliano de'Medici (1453-1478)"],

    # numbers -> dating info
    ["Komposition 1923 V",
     "Bildnis eines Mannes von 35-40 Jahren",
     "Dorfszene im Winter 1828"],

    ["Doppelporträt zweier Ärzte als Heilige Cosmas und Damian. Um 1623/26"],


    # space slash space -> alternatives or language variants
    ["Die Versucherin / Allegorie der Vanitas",
     # "Antiochos und Stratonike / Der kranke Königssohn",
     "Der lustige Zecher / Herr Peeckelhaering",
     # "Das Kartenspielchen / Soldat und Dirne",
     # "Das lustige Paar / Satyr mit Nymphe",
     "Angebliches Bildnis des Don Carlos / Bildnis eines Hofzwerges",
     "Die Briefsieglerin / Une femme occupée à cacheter une lettre"],

    ["Rückkehr vom Markt / Die Köchin / La pourvoyeuse"],
    # space slash space ... space slash space -> alternatives or language variants


] # n = 17