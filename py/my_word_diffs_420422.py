import my_word_diffs_420422_long_further_remarks as furrem


def _part_n_of_2(partn, from_str, to_str):
  return f'This is part {partn} of 2 of a change from {from_str} to {to_str}.'


_UXLC_RAFEH = 'UXLC rejected all rafeh-removing WLC changes.'
RECORDS = [
    {
      'wlc_bcv_str': "gn1:11",
      'word_diff_type': "word changed and notes changed",
      'ab-word': "D.E80$E)\nD.E81$E)",
      'ab-uword': "דֶּ֔שֶׁא\nדֶּ֗שֶׁא",
      'ab-notes': "\n]Q]c",
      'UXLC-change-proposals': ('2021.04.01', '2021.02.22-1'),
    },
    {
      'wlc_bcv_str': "gn2:8",
      'word_diff_type': "word changed but notes did not",
      'ab-word': "B:/(\"73DEN\nB.:/(\"73DEN",
      'ab-uword': "בְעֵ֖דֶן\nבְּעֵ֖דֶן",
      'ab-notes': "\n",
      'UXLC-change-proposals': ("2021.04.01", "2021.02.22-2"),
      'initial-remark': 'UXLC qualifies this WLC change with a t-note.',
      'UXLC-note': "https://tanach.us/Notes/Genesis/Genesis.2.8.5-t.html",
    },
    {
      'wlc_bcv_str': "gn2:10",
      'word_diff_type': "word changed and notes changed",
      'ab-word': "W:/NFHFR.03\nW:/NFHFR03",
      'ab-uword': "וְנָהָרּ֙\nוְנָהָר֙",
      'ab-notes': "]p\n",
      'UXLC-change-proposals': ("2021.04.01", "2020.12.29-1"),
    },
    {
      'wlc_bcv_str': "gn14:17",
      'word_diff_type': "word changed and notes changed",
      'ab-word': ")AX:AR\"74Y\n)AXAR\"74Y",
      'ab-uword': "אַחֲרֵ֣י\nאַחַרֵ֣י",
      'ab-notes': "\n]Q]n]v",
      'UXLC-change-proposals': ('2022.07.04', '2022.03.29-2'),
      # Kind of weird that this was a Holman change not a Salisbury change.
    },
    {
      'wlc_bcv_str': "gn14:17",
      'word_diff_type': "word changed but notes did not",
      'ab-word': "K.:DFR→\nK.:DFR-",
      'ab-uword': "כְּדָר→\nכְּדָר־",
      'ab-notes': "\n",
      'initial-remark': _part_n_of_2(1, 'אב', 'א־ב'),
      'UXLC-change-proposals': [
          ('2021.04.01', '2021.02.22-3'),
          ('2022.10.19', '2022.07.02-6')
      ],
    },
    {
      'wlc_bcv_str': "gn14:17",
      'word_diff_type': "word changed and notes changed",
      'ab-word': "←LF(O80MER\nLF(O80MER",
      'ab-uword': "←לָעֹ֔מֶר\nלָעֹ֔מֶר",
      'ab-notes': "]n]p\n",
      'initial-remark': _part_n_of_2(2, 'אב', 'א־ב'),
      'UXLC-change-proposals': [
          ('2021.04.01', '2021.02.22-3'),
          ('2022.10.19', '2022.07.02-6')
      ],
    },
    {
      'wlc_bcv_str': "gn18:25",
      'word_diff_type': "word changed and notes changed",
      'ab-word': "KA/C.AD.I73YQ\nKA/CAD.I73YQ",
      'ab-uword': "כַצַּדִּ֖יק\nכַצַדִּ֖יק",
      'ab-notes': "\n]Q]n]p",
      'UXLC-change-proposals': ("2021.04.01", "2021.02.22-4"),
    },
    {
      'wlc_bcv_str': "gn24:53",
      'word_diff_type': "word changed and notes changed",
      'ab-word': "WA/Y.IT.\"73N\nWA/YIT.\"73N",
      'ab-uword': "וַיִּתֵּ֖ן\nוַיִתֵּ֖ן",
      'ab-notes': "\n]Q]n]p",
      'UXLC-change-proposals': ("2021.04.01", "2021.02.22-5"),
    },
    {
      'wlc_bcv_str': "gn25:6",
      'word_diff_type': "word changed and notes changed",
      'ab-word': "B.:N/OW03\nB.N/OW03",
      'ab-uword': "בְּנוֹ֙\nבּנוֹ֙",
      'ab-notes': "\n]Q]n]v",
      'UXLC-change-proposals': ('2021.04.01', '2021.02.22-6'),
    },
    {
      'wlc_bcv_str': "gn26:1",
      'word_diff_type': "word changed and notes changed",
      'ab-word': "):ABIYM.E71LEK:\n):ABIYME71LEK:",
      'ab-uword': "אֲבִימֶּ֥לֶךְ\nאֲבִימֶ֥לֶךְ",
      'ab-notes': "]1\n]Q]p",
      'UXLC-change-proposals': ("2021.04.01", "2021.02.22-7"),
    },
    {
      'wlc_bcv_str': "gn34:28",
      'word_diff_type': "word changed and notes changed",
      'ab-word': "X:AMOR\"Y/H.E92M\nX:AMOR\"Y/HE92M",
      'ab-uword': "חֲמֹרֵיהֶּ֑ם\nחֲמֹרֵיהֶ֑ם",
      'ab-notes': "]1\n]Q]p",
      'UXLC-change-proposals': ("2021.04.01", "2021.01.04-1"),
    },
    {
      'wlc_bcv_str': "gn35:22",
      'word_diff_type': "word changed and notes changed",
      'ab-word': "R:)W.B\"80N\nR:)W.B\"8081N",
      'ab-uword': "רְאוּבֵ֔ן\nרְאוּבֵ֔֗ן",
      'ab-notes': "\n]C]c",
      'UXLC-change-proposals': ("2021.04.01", "2021.02.22-8"),
    },
    {
      'wlc_bcv_str': "gn38:11",
      'word_diff_type': "word changed and notes changed",
      'ab-word': "B:N/I80Y\nB:N/:80Y",
      'ab-uword': "בְנִ֔י\nבְנְ֔י",
      'ab-notes': "\n]Q]n]v",
      'UXLC-change-proposals': ('2021.04.01', '2021.02.22-9'),
    },
    {
      'wlc_bcv_str': "gn39:2",
      'word_diff_type': "word changed and notes changed",
      'ab-word': "B.:/B\"71YT\nB.:/B\"73YT",
      'ab-uword': "בְּבֵ֥ית\nבְּבֵ֖ית",
      'ab-notes': "\n]C]c",
      'UXLC-change-proposals': ('2020.02.19', '2018.11.27-1'),
    },
    {
      'wlc_bcv_str': "gn39:2",
      'word_diff_type': "word changed and notes changed",
      'ab-word': "):ADONF73Y/W\n):ADONF71Y/W",
      'ab-uword': "אֲדֹנָ֖יו\nאֲדֹנָ֥יו",
      'ab-notes': "\n]C]c",
      'UXLC-change-proposals': ('2020.02.19', '2018.11.27-2'),
    },
    {
      'wlc_bcv_str': "gn39:23",
      'word_diff_type': "word changed and notes changed",
      'ab-word': "HA/S.O81HAR\nHA/S.OHA81R",
      'ab-uword': "הַסֹּ֗הַר\nהַסֹּהַ֗ר",
      'ab-notes': "\n]Q]c]n",
      'UXLC-change-proposals': ('2021.04.01', '2021.02.22-10'),
    },
    {
      'wlc_bcv_str': "gn41:7",
      'word_diff_type': "word changed and notes changed",
      'ab-word': "HA75/$.IB.:FLI80YM\nHA75/$IB.:FLI80YM",
      'ab-uword': "הַֽשִּׁבֳּלִ֔ים\nהַֽשִׁבֳּלִ֔ים",
      'ab-notes': "\n]Q]n]p",
      'UXLC-change-proposals': ("2021.04.01", "2021.02.22-11"),
    },
    {
      'wlc_bcv_str': "gn41:24",
      'word_diff_type': "word changed and notes changed",
      'ab-word': "HF/$IB.:FLI74YM\nHA/$IB.:FLI74YM",
      'ab-uword': "הָשִׁבֳּלִ֣ים\nהַשִׁבֳּלִ֣ים",
      'ab-notes': "]1\n]Q]U]v",
      'UXLC-change-proposals': ('2021.04.01', '2021.02.22-12'),
    },
    {
      'wlc_bcv_str': "gn50:1",
      'word_diff_type': "word changed and notes changed",
      'ab-word': "WA/Y.IP.O71L\nWA/YIP.O71L",
      'ab-uword': "וַיִּפֹּ֥ל\nוַיִפֹּ֥ל",
      'ab-notes': "\n]Q]n]p",
      'UXLC-change-proposals': ("2021.04.01", "2021.02.22-13"),
    },
    {
      'wlc_bcv_str': "ex10:13",
      'word_diff_type': "word changed but notes did not",
      'ab-word': "R71W.XA\nR71W.XA-",
      'ab-uword': "ר֥וּחַ\nר֥וּחַ־",
      'ab-notes': "\n",
      'UXLC-change-proposals': [
          ("2021.04.01", "2021.02.22-14"),
          ("2023.07.04", "2023.03.27-1")
      ],
      'further-remarks': [
          "Although UXLC agrees with WLC 4.22 with respect to the maqaf at issue, "
          "UXLC differs from WLC 4.22 by having “demoted” this word’s merkha to a meteg."
      ]
    },
    {
      'wlc_bcv_str': "ex20:3",
      'word_diff_type': "word changed but notes did not",
      'ab-word': "P.FN/F8175YA\nP.FN/F75A81Y",
      'ab-uword': "פָּנָ+נ֗+נֽיַ\nפָּנָ+נֽ+נַ+נ֗י",
      'ab-notes': "]1\n]1",
      'UXLC-change-proposals': [
          ('2020.10.19', '2020.06.07-1'),
          ('2021.10.19', '2021.05.19-8'),
          ('2022.04.01', '2021.10.26-1')
      ],
      'initial-remark': 'UXLC somehow already had part of this change.',
      'further-remarks': [
          'Both WLC & UXLC needed to move the pataḥ back from the yod to the nun. '
          'WLC also needed to change the relative order of the accents (silluq and revia). '
          'UXLC somehow already had the relative order of the accents correct: UO, '
          'under-accent and then over-accent, which in this cases means '
          'silluq and then revia.',
          #
          'All UXLC was doing in its 2021.05.19-8 change was making its mark order robust. '
          'By “robust” I mean robust to Unicode normalization.',
          #
          'All UXLC was doing in its 2021.10.26-1 change was removing a ZWJ hack no longer relevant once CGJ was added.'
      ]
    },
    {
      'wlc_bcv_str': "ex20:4",
      'word_diff_type': "word changed but notes did not",
      'ab-word': "MI/T.F9261AXAT\nMI/T.F92A61XAT",
      'ab-uword': "מִתָּ֑+תּ֜+תַּחַת\nמִתָּ֑+תַּ+תּ֜חַת",
      'ab-notes': "]1\n]1",
      'UXLC-change-proposals': ('2021.10.19', '2021.05.19-7'),
      'initial-remark': 'UXLC somehow already had the correct mark order.',
      'further-remarks': [
          'I.e., UXLC somehow already had QUPO mark order. '
          'In terms of Michigan-Claremont encoding, we might call this FUAO mark order, '
          'since in M-C, F is qamats and A is pataḥ. '
          'So FUAO here is F92A61: '
          'U (under-accent) is 92 (atnaḥ) and '
          'O (over-accent) is 61 (geresh).',
          #
          'All UXLC was doing in its 2021.05.19-7 change was making its already-correct mark order robust. '
          'By “robust” I mean robust to Unicode normalization.'
      ]
    },
    {
      'wlc_bcv_str': "ex20:10",
      'word_diff_type': "word changed but notes did not",
      'ab-word': "W:/YO33WM03\nW:/YO63WM03",
      'ab-uword': "וְי֙וֹם֙\nוְי֨וֹם֙",
      'ab-notes': "\n",
      'UXLC-change-proposals': ('2020.10.19', '2020.06.07-2'),
    },
    {
      'wlc_bcv_str': "ex20:13",
      'word_diff_type': "word changed but notes did not",
      'ab-word': "T.,IR:CF7375X00\nT.IR:CF7375X00",
      'ab-uword': "תִּֿרְצָ֖+צֽח׃\nתִּרְצָ֖+צֽח׃",
      'ab-notes': "\n",
      # 'UXLC-change-proposals': ('2020.10.19', '2020.09.29-4'),
      # The proposal above is just adding a CGJ so it is not relevant to the WLC change,
      # which is to remove a rafeh.
      'initial-remark': _UXLC_RAFEH,
      'Decalogue-rafeh': True,
      'further-remarks': furrem.DECALOGUE_RAFE
    },
    {
      'wlc_bcv_str': "ex20:14",
      'word_diff_type': "word changed but notes did not",
      'ab-word': "T.,IN:)F9275P00\nT.IN:)F9275P00",
      'ab-uword': "תִּֿנְאָ֑+אֽף׃\nתִּנְאָ֑+אֽף׃",
      'ab-notes': "\n",
      # 'UXLC-change-proposals': [
      #     ('2020.02.19', '2020.01.30-10'),
      #     ('2021.04.01', '2020.09.29-1')
      # ],
      # The proposals above have the net effect of just adding a CGJ so they are not relevant to the WLC change,
      # which is to remove a rafeh.
      'initial-remark': _UXLC_RAFEH,
      'Decalogue-rafeh': True,
      'further-remarks': furrem.DECALOGUE_RAFE
    },
    {
      'wlc_bcv_str': "ex20:15",
      'word_diff_type': "word changed but notes did not",
      'ab-word': "T.,IG:NO8075B00\nT.IG:NO8075B00",
      'ab-uword': "תִּֿגְנֹ֔+נֽב׃\nתִּגְנֹ֔+נֽב׃",
      'ab-notes': "\n",
      'initial-remark': _UXLC_RAFEH,
      'Decalogue-rafeh': True,
      'further-remarks': furrem.DECALOGUE_RAFE
    },
    {
      'wlc_bcv_str': "lv13:3",
      'word_diff_type': "word changed and notes changed",
      'ab-word': "HA/N.E33GA(03\nHA/N.E33GE(03",
      'ab-uword': "הַנֶּ֙גַע֙\nהַנֶּ֙גֶע֙",
      'ab-notes': "\n]v",
      'UXLC-change-proposals': ('2021.04.01', '2021.02.22-15'),
    },
    {
      'wlc_bcv_str': "lv23:38",
      'word_diff_type': "word changed but notes did not",
      'ab-word': "Y.:HWF92H\nY:HWF92H",
      'ab-uword': "יְּהוָ֑ה\nיְהוָ֑ה",
      'ab-notes': "\n",
      'UXLC-change-proposals': ("2021.04.01", "2021.02.22-16"),
    },
    {
      'wlc_bcv_str': "lv26:35",
      'word_diff_type': "word changed and notes changed",
      'ab-word': "HF$.AM./F73H\nHF$AM./F73H",
      'ab-uword': "הָשַּׁמָּ֖ה\nהָשַׁמָּ֖ה",
      'ab-notes': "\n]p",
      'UXLC-change-proposals': [
          ("2021.04.01", "2021.02.22-17"),
          ("2022.04.01", "2021.12.28-2")
      ]
    },
    {
      'wlc_bcv_str': "nu11:24",
      'word_diff_type': "word changed and notes changed",
      'ab-word': "MO$E81H\nMO$E80H",
      'ab-uword': "מֹשֶׁ֗ה\nמֹשֶׁ֔ה",
      'ab-notes': "\n]c",
      'UXLC-change-proposals': ("2021.04.01", "2021.02.22-18"),
    },
    {
      'wlc_bcv_str': "nu16:7",
      'word_diff_type': "word changed and notes changed",
      'ab-word': "(:AL\"Y/HE63N\n(:AL\"Y/HE63N05",
      'ab-uword': "עֲלֵיהֶ֨ן\nעֲלֵיהֶ֨ן׀",
      'ab-notes': "\n]c",
      'UXLC-change-proposals': ("2021.04.01", "2021.02.22-19"),
    },
    {
      'wlc_bcv_str': "nu24:13",
      'word_diff_type': "word changed and notes changed",
      'ab-word': "MI/L.IB./I92Y\nMI/LIB./I92Y",
      'ab-uword': "מִלִּבִּ֑י\nמִלִבִּ֑י",
      'ab-notes': "\n]p",
      'UXLC-change-proposals': ("2021.04.01", "2021.02.22-20"),
    },
    {
      'wlc_bcv_str': "dt5:13",
      'word_diff_type': "word changed but notes did not",
      'ab-word': "K.,FL-\nK.FL-",
      'ab-uword': "כָּֿל־\nכָּל־",
      'ab-notes': "\n",
      'initial-remark': _UXLC_RAFEH,
      'Decalogue-rafeh': True,
      'further-remarks': furrem.DECALOGUE_RAFE
    },
    {
      'wlc_bcv_str': "dt5:14",
      'word_diff_type': "word changed but notes did not",
      'ab-word': "W:/YO33WM03\nW:/YO63WM03",
      'ab-uword': "וְי֙וֹם֙\nוְי֨וֹם֙",
      'ab-notes': "\n",
      'UXLC-change-proposals': ("2020.10.19", "2020.06.07-4"),
    },
    {
      'wlc_bcv_str': "dt5:17",
      'word_diff_type': "word changed but notes did not",
      'ab-word': "T.,IR:CF75X00\nT.IR:CF75X00",
      'ab-uword': "תִּֿרְצָֽח׃\nתִּרְצָֽח׃",
      'ab-notes': "\n",
      'initial-remark': _UXLC_RAFEH,
      'Decalogue-rafeh': True,
      'further-remarks': furrem.DECALOGUE_RAFE
    },
    {
      'wlc_bcv_str': "dt5:18",
      'word_diff_type': "word changed but notes did not",
      'ab-word': "T.,IN:)F7592P00\nT.IN:)F7592P00",
      'ab-uword': "תִּֿנְאָֽ֑ף׃\nתִּנְאָֽ֑ף׃",
      'ab-notes': "\n",
      'initial-remark': _UXLC_RAFEH,
      'Decalogue-rafeh': True,
      'further-remarks': furrem.DECALOGUE_RAFE
    },
    {
      'wlc_bcv_str': "dt5:19",
      'word_diff_type': "word changed but notes did not",
      'ab-word': "T.,IG:NO7580B00\nT.IG:NO7580B00",
      'ab-uword': "תִּֿגְנֹֽ֔ב׃\nתִּגְנֹֽ֔ב׃",
      'ab-notes': "\n",
      'initial-remark': _UXLC_RAFEH,
      'Decalogue-rafeh': True,
      'further-remarks': furrem.DECALOGUE_RAFE
    },
    {
      'wlc_bcv_str': "dt7:8",
      'word_diff_type': "word changed and notes changed",
      'ab-word': "W./MI/$.FM:R/70W.\nW./MI/$.FM:R/70W",
      'ab-uword': "וּמִשָּׁמְר֤וּ\nוּמִשָּׁמְר֤ו",
      'ab-notes': "]P]p]v\n]Q]n]v",
      'UXLC-change-proposals': ("2021.04.01", "2021.02.22-21"),
    },
    {
      'wlc_bcv_str': "dt12:30",
      'word_diff_type': "word changed and notes changed",
      'ab-word': "L\"/)MO63R\nL\"/)MO81R",
      'ab-uword': "לֵאמֹ֨ר\nלֵאמֹ֗ר",
      'ab-notes': "\n]P]p",
      'UXLC-change-proposals': ("2020.02.19", "2019.09.01-1"),
    },
    {
      'wlc_bcv_str': "2s11:1",
      'word_diff_type': "word changed but notes did not",
      'ab-word': "HA/M.AL:),KI81YM\nHA/M.AL:)KI81YM",
      'ab-uword': "הַמַּלְאֿכִ֗ים\nהַמַּלְאכִ֗ים",
      'ab-notes': "]1\n]1",
      'initial-remark': _UXLC_RAFEH,
      'Decalogue-rafeh': True,
    },
    {
      'wlc_bcv_str': "1k9:9",
      'word_diff_type': "word changed and notes changed",
      'ab-word': "WA/Y.A(AB:DU92/M\nWA/Y.A(:AB:DU92/M",
      'ab-uword': "וַיַּעַבְדֻ֑ם\nוַיַּעֲבְדֻ֑ם",
      'ab-notes': "\n]v",
      'UXLC-change-proposals': ("2021.04.01", "2021.02.22-22"),
    },
    {
      'wlc_bcv_str': "is22:10",
      'word_diff_type': "word changed but notes did not",
      'ab-word': "WA/T.IT,:CW.03\nWA/T.IT:CW.03",
      'ab-uword': "וַתִּתְֿצוּ֙\nוַתִּתְצוּ֙",
      'ab-notes': "\n",
      'initial-remark': _UXLC_RAFEH,
      'Decalogue-rafeh': True,
    },
    {
      'wlc_bcv_str': "is45:6",
      'word_diff_type': "word changed and notes changed",
      'ab-word': "W./MI/M.A74(:ARFB/F80H.\nW./MI/M.A74(:ARFB/F80H",
      'ab-uword': "וּמִמַּ֣עֲרָבָ֔הּ\nוּמִמַּ֣עֲרָבָ֔ה",
      'ab-notes': "]p\n]1",
      'UXLC-change-proposals': ("2021.04.01", "2021.02.22-23"),
    },
    {
      'wlc_bcv_str': "je15:18",
      'word_diff_type': "word changed and notes changed",
      'ab-word': "):ANW.$F92H03\n):ANW.$F92H",
      'ab-uword': "אֲנוּשָׁ֑ה֙\nאֲנוּשָׁ֑ה",
      'ab-notes': "\n]c",
      'UXLC-change-proposals': ("2021.04.01", "2021.02.22-24"),
    },
    {
      'wlc_bcv_str': "je20:17",
      'word_diff_type': "word changed but notes did not",
      'ab-word': "W:/RAX:M/F73H,\nW:/RAX:M/F73H",
      'ab-uword': "וְרַחְמָ֖הֿ\nוְרַחְמָ֖ה",
      'ab-notes': "\n",
      'initial-remark': _UXLC_RAFEH,
      'Decalogue-rafeh': True,
    },
    {
      'wlc_bcv_str': "je27:13",
      'word_diff_type': "word changed and notes changed",
      'ab-word': "W./BA/D.F92BER03\nW./BA/D.F92BER",
      'ab-uword': "וּבַדָּ֑בֶר֙\nוּבַדָּ֑בֶר",
      'ab-notes': "\n]c",
      'UXLC-change-proposals': ("2021.04.01", "2021.02.22-25"),
    },
    {
      'wlc_bcv_str': "je44:19",
      'word_diff_type': "word changed and notes changed",
      'ab-word': "L:/HA74(:ACIB/F80H\nL:/HA74(:ACIB/F80H.",
      'ab-uword': "לְהַ֣עֲצִבָ֔ה\nלְהַ֣עֲצִבָ֔הּ",
      'ab-notes': "\n]p",
      'initial-remark': "UXLC rejected this WLC change, in the end.",
      'further-remarks': [
          "This seems like a bad change to WLC because the mapiq is likely an artifact. "
          "UXLC has a rafeh on the he in question. "
          "UXLC arrived at this with a bit of back-and-forth: 3 changes. "
          "Change 1 added the mapiq, change 2 added the rafeh, and change 3 removed the mapiq, "
          "with the net result that only a rafeh remains."],
      'UXLC-change-proposals': [
        ("2020.02.19", "2019.12.21-1"),
        ("2020.10.19", "2020.07.16-1"),
        ("2021.04.01", "2021.03.04-1")
      ]
    },
    {
      'wlc_bcv_str': "je48:27",
      'word_diff_type': "word changed and notes changed",
      'ab-word': "D:BFRE71Y/KF\nD:BFRE91Y/KF",
      'ab-uword': "דְבָרֶ֥יךָ\nדְבָרֶ֛יךָ",
      'ab-notes': "\n]c",
      'UXLC-change-proposals': ("2020.02.19", "2019.01.03-1"),
    },
    {
      'wlc_bcv_str': "zc5:11",
      'word_diff_type': "word changed and notes changed",
      'ab-word': "L/F71H,\nL/F71H",
      'ab-uword': "לָ֥הֿ\nלָ֥ה",
      'ab-notes': "\n]U",
      'initial-remark': _UXLC_RAFEH,
      'Decalogue-rafeh': True,
    },
    {
      'wlc_bcv_str': "1c10:1",
      'word_diff_type': "word changed but notes did not",
      'ab-word': "WA/Y.F92NFS\nWA/Y.F70NFS",
      'ab-uword': "וַיָּ֑נָס\nוַיָּ֤נָס",
      'ab-notes': "\n",
      'UXLC-change-proposals': ("2021.04.01", "2021.02.22-27"),
    },
    {
      'wlc_bcv_str': "ps119:99",
      'word_diff_type': "word changed but notes did not",
      'ab-word': "L,/I75Y00\nL/I75Y00",
      'ab-uword': "לִֽֿי׃\nלִֽי׃",
      'ab-notes': "\n",
      'initial-remark': _UXLC_RAFEH,
      'Decalogue-rafeh': True,
    },
    {
      'wlc_bcv_str': "es7:8",
      'word_diff_type': "word changed and notes changed",
      'ab-word': "NOP\"80L\nNOP\"81L",
      'ab-uword': "נֹפֵ֔ל\nנֹפֵ֗ל",
      'ab-notes': "\n]C]c",
      'UXLC-change-proposals': ('2021.04.01', '2021.02.22-26'),
    },
    {
      'wlc_bcv_str': "da2:39",
      'word_diff_type': "word changed and notes changed",
      'ab-word': "):ARA74()\n**):ARA74(",
      'ab-uword': "אֲרַ֣עא\n**אֲרַ֣ע",
      'ab-notes': "]1\n",
      'UXLC-change-proposals': [
          ('2021.04.01', '2021.02.22-28'),
          ('2023.04.01', '2023.03.06-1'),
          ('2023.04.01', '2023.03.06-2')
      ],
    },
    {
      'wlc_bcv_str': "er4:12",
      'word_diff_type': "word changed but notes did not",
      'ab-word': "**W:/$W.RAY./F74)\n*)#KLLW",
      'ab-uword': "**וְשׁוּרַיָּ֣א\n*אשכללו",
      'ab-notes': "\n",
      'initial-remark': _part_n_of_2(1, 'k1q1×2', 'k2q2') + ' UXLC rejected this change.',
      'further-remarks': furrem.EZRA_4_12,
      'img': 'Ezra4v12.png',
      'line': 25,
    },
    {
      'wlc_bcv_str': "er4:12",
      'word_diff_type': "word changed but notes did not",
      'ab-word': "*)#KLLW\n**W:/$W.RAY./F74)",
      'ab-uword': "*אשכללו\n**וְשׁוּרַיָּ֣א",
      'ab-notes': "\n",
      'initial-remark': _part_n_of_2(2, 'k1q1×2', 'k2q2') + ' UXLC rejected this change.',
      'further-remarks': furrem.EZRA_4_12,
      'img': 'Ezra4v12.png',
      'line': 25,
    }
  ]
WORD_POSITIONS = {
    'gn1:11!D.E80$E)': 5,
    'gn2:8!B:/(\"73DEN': 5,
    'gn2:10!W:/NFHFR.03': 1,
    'gn14:17!)AX:AR\"74Y': 5,
    'gn14:17!K.:DFR→': 9,
    'gn14:17!←LF(O80MER': 10,
    'gn18:25!KA/C.AD.I73YQ': 11,
    'gn24:53!WA/Y.IT.\"73N': 8,
    'gn25:6!B.:N/OW03': 11,
    'gn26:1!):ABIYM.E71LEK:': 14,
    'gn34:28!X:AMOR\"Y/H.E92M': 6,
    'gn35:22!R:)W.B\"80N': 7,
    'gn38:11!B:N/I80Y': 12,
    'gn39:2!B.:/B\"71YT': 9,
    'gn39:2!):ADONF73Y/W': 10,
    'gn39:23!HA/S.O81HAR': 4,
    'gn41:7!HA75/$.IB.:FLI80YM': 6,
    'gn41:24!HF/$IB.:FLI74YM': 2,
    'gn50:1!WA/Y.IP.O71L': 1,
    'ex10:13!R71W.XA': 10,
    'ex20:3!P.FN/F8175YA': 7,
    'ex20:4!MI/T.F9261AXAT': 12,
    'ex20:10!W:/YO33WM03': 1,
    'ex20:13!T.,IR:CF7375X00': 2,
    'ex20:14!T.,IN:)F9275P00': 2,
    'ex20:15!T.,IG:NO8075B00': 2,
    'lv13:3!HA/N.E33GA(03': 12,
    'lv23:38!Y.:HWF92H': 3,
    'lv26:35!HF$.AM./F73H': 3,
    'nu11:24!MO$E81H': 2,
    'nu16:7!(:AL\"Y/HE63N': 5,
    'nu24:13!MI/L.IB./I92Y': 19,
    'dt5:13!K.,FL-': 5,
    'dt5:14!W:/YO33WM03': 1,
    'dt5:17!T.,IR:CF75X00': 2,
    'dt5:18!T.,IN:)F7592P00': 2,
    'dt5:19!T.,IG:NO7580B00': 2,
    'dt7:8!W./MI/$.FM:R/70W.': 5,
    'dt12:30!L\"/)MO63R': 12,
    '2s11:1!HA/M.AL:),KI81YM': 6,
    '1k9:9!WA/Y.A(AB:DU92/M': 20,
    'is22:10!WA/T.IT,:CW.03': 5,
    'is45:6!W./MI/M.A74(:ARFB/F80H.': 5,
    'je15:18!):ANW.$F92H03': 6,
    'je20:17!W:/RAX:M/F73H,': 9,
    'je27:13!W./BA/D.F92BER03': 7,
    'je44:19!L:/HA74(:ACIB/F80H': 14,
    'je48:27!D:BFRE71Y/KF': 13,
    'zc5:11!L/F71H,': 4,
    '1c10:1!WA/Y.F92NFS': 4,
    'ps119:99!L,/I75Y00': 7,
    'es7:8!NOP\"80L': 10,
    'da2:39!):ARA74()': 6,
    'er4:12!**W:/$W.RAY./F74)': 19,
    'er4:12!*)#KLLW': 20
  }
