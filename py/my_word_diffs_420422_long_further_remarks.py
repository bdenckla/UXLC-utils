import my_html


def rmn(string):
    return my_html.span(string, {"class": "romanized"})


DECALOGUE_RAFE = [
    my_html.para(
        [
            "In WLC 4.22, all 12 ",
            rmn("rafeh"),
            " marks of 4.20 were removed. " "Seven of those ",
            rmn("rafeh"),
            " marks were in the Decalogues. " "This is one of those seven.",
        ]
    ),
    my_html.para(
        [
            "The utility of the other five ",
            rmn("rafeh"),
            " marks was debatable, " "since they merely marked letters where ",
            rmn("dagesh/mapiq"),
            " might have been expected. " "Those ",
            rmn("rafeh"),
            " marks expressed something like “this letter is intentionally left blank” "
            "if “blank” is taken to mean “free of ",
            rmn("dagesh/mapiq"),
            ".”",
        ]
    ),
    my_html.para(
        [
            "In contrast, the utility of these seven ",
            rmn("rafeh"),
            " marks "
            "was less debatable. "
            "These seven marks meant something quite different than those other five. "
            "We could say that these seven ",
            rmn("rafeh"),
            " marks modulated the meaning " "of the ",
            rmn("dagesh"),
            " present on the same letter. " "These ",
            rmn("rafeh"),
            " marks expressed something like " "“the ",
            rmn("dagesh"),
            " below applies to only one of the cantillations.”",
        ]
    ),
    my_html.para(
        [
            "In other words, whereas the five non-Decalogue ",
            rmn("rafeh"),
            " marks "
            "merely reassure the reader that "
            "“this letter is intentionally left blank,” "
            "these seven ",
            rmn("rafeh"),
            " marks tell the reader something like "
            "“this letter is contextually left blank.”",
        ]
    ),
    my_html.para(
        [
            "As documented on page xiv of its Foreword, Dotan’s BHL does not include any ",
            rmn("rafeh"),
            " marks. "
            "This does not, as the WLC 4.22 documentation suggests, support the removal "
            "of these seven Decalogue ",
            rmn("rafeh"),
            " marks. "
            "BHL presents the Decalogues in split rather than combined form, "
            "so these ",
            rmn("rafeh"),
            " marks would have the usual meaning, of debatable utility, "
            "in the lower cantillation. "
            "So, the lack of ",
            rmn("rafeh"),
            " marks in BHL’s (four) Decalogues says nothing "
            "one way or another about the utility of ",
            rmn("rafeh"),
            " marks " "in WLC’s (two) Decalogues.",
        ]
    ),
    my_html.para(
        [
            "The WLC 4.22 documentation cites not only BHL but also BHQ "
            "in support of its decision to remove all ",
            rmn("rafeh"),
            " marks. "
            "The comparison with BHQ is more relevant, since BHQ, like WLC, "
            "presents the Deuteronomy Decalogue in combined rather than split form. "
            "(The Exodus fascicle of BHQ has not yet been released.)",
        ]
    ),
    my_html.para(
        [
            "Yet, I don’t consider BHQ’s lack of Decalogue ",
            rmn("rafeh"),
            " marks "
            "to be a precedent to be cited for support. "
            "Rather, I see BHQ’s lack of Decalogue ",
            rmn("rafeh"),
            " marks as "
            "yet another piece of evidence pointing to BHQ’s rather casual "
            "(or at least inconsistently serious) "
            "attitude towards details of niqqud. "
            "Here we see BHQ not only failing to improve upon BHS "
            "but in fact taking a step backwards. "
            "I advise WLC to not follow BHQ in this regression, i.e. I advise WLC "
            "to restore these 7 Decalogue ",
            rmn("rafeh"),
            " marks in some future version.",
        ]
    ),
]
EZRA_4_12 = [
    my_html.para(
        [
            "I think I understand the impulse behind this WLC change, "
            "but nonetheless I find the change inadvisable. "
            "So I not only support UXLC’s rejection of this change "
            "but also advise WLC to revert this change in some future version.",
        ]
    ),
    my_html.para(
        [
            "My guess is that the impulse behind this change is "
            "that we are primarily dealing with a word boundary issue here. "
            "There is a ",
            rmn("ḥaser/malei"),
            " issue later in the second word, "
            "but the primary issue is where the word boundary falls within the letters "
            "ושוריאשכל[י]לו. "
            "Specifically, the ",
            rmn("qere"),
            " places the word boundary after the א, yielding",
        ]
    ),
    my_html.para(
        [
            "ושוריא שכלילו",
        ]
    ),
    my_html.para(
        [
            " whereas the ",
            rmn("ketiv"),
            " places the word boundary before the א, yielding",
        ]
    ),
    my_html.para(
        [
            "ושורי אשכללו",
        ]
    ),
    my_html.para(
        [
            "Because we are primarily dealing with a word boundary issue here, "
            "it is an understandable impulse to group these 4 words into a single k2q2 construct "
            "(which is what WLC 4.22 now has) "
            "rather than group them into two adjacent k1q1 constructs "
            "(which is what WLC 4.20 had). "
            "In Michigan-Clarement terms, a k2q2 construct looks something like this, schematically:",
        ]
    ),
    my_html.para(
        [
            "*ka *kb **qa **qb",
        ]
    ),
    my_html.para(
        [
            "whereas a k1q1×2 (two adjacent k1q1 constructs) looks something like this, schematically:",
        ]
    ),
    my_html.para(
        [
            "*ka **qa *kb **qb",
        ]
    ),
    my_html.para(
        [
            "Although the impulse is understandable, it is not consistent with the diplomatic spirit of "
            "WLC to allow such an impulse to override what we clearly see in the manuscript. "
            "What we clearly see in the manuscript is the choice to treat these words as k1q1×2: "
            "two adjacent k1q1 constructs. "
            "BHS and BHQ agree with the manuscript, though of course we’d be willing to reject their "
            "reading if it contradicted the manuscript."
        ]
    ),
]
