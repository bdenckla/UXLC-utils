""" Exports Latin-alphabet symbols for some template names. """

# SR: strongly related ketiv & qere
# WR: weakly related ketiv & qere
# UR: unrelated ketiv & qere

K1Q1_MCOM = 'מ:כו"ק בין שני מקפים'
K1Q2_SR_KQQ = 'מ:כו"ק כתיב מילה חדה וקרי תרתין מילין'
K1Q2_SR_QQK = 'מ:קו"כ כתיב מילה חדה וקרי תרתין מילין'
K1Q2_SR_BCOM = 'מ:כו"ק כתיב מילה חדה וקרי תרתין מילין בין שני מקפים'
K1Q2_WR_KQQ = 'מ:כו"ק קרי שונה מהכתיב בשתי מילים'
K1Q2_UR_QQK = 'מ:קו"כ קרי שונה מהכתיב בשתי מילים'
K2Q1 = 'מ:כו"ק כתיב תרתין מילין וקרי מילה חדה'
K2Q2 = 'מ:כו"ק של שתי מילים בהערה אחת'
TWO_ACCENTS_OF_QUPO = 'שני טעמים באות אחת קמץ-תחתון-פתח-עליון'
NO_PAR_AT_STA_OF_PRQ = 'מ:אין פרשה בתחילת פרק'
NO_PAR_AT_STA_OF_PRQ_EMT = 'מ:אין פרשה בתחילת פרק בספרי אמ"ת'
GENESIS_WEIRD_START = 'מ:אין רווח של פרשה בתחילת פרשת השבוע'
SLH_WORD = 'מ:אות-מיוחדת-במילה'
SCRDFFTAR = 'מ:הערה-2'

LATIN_SHORTS = {
    K1Q1_MCOM: 'k1q1-mcom',
    K1Q2_SR_KQQ: 'k1q2-sr-kqq',
    K1Q2_SR_QQK: 'k1q2-sr-qqk',
    K1Q2_SR_BCOM: 'k1q2-sr-bcom',
    K1Q2_WR_KQQ: 'k1q2-wr-kqq',
    K1Q2_UR_QQK: 'k1q2-ur-qqk',
    K2Q1: 'k2q1',
    K2Q2: 'k2q2',
    'כו"ק': 'k1q1-kq',
    'קו"כ': 'k1q1-qk',
    'קו"כ-אם': 'kq-trivial',
    'קרי ולא כתיב': 'kq-q-velo-k',
    'כתיב ולא קרי': 'kq-k-velo-q',
}