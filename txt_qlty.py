import requests
from bs4 import BeautifulSoup
import re
import nltk
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import syllables

nltk.download('punkt')
nltk.download('stopwords')
def get_scores(url1=None, para=None):
    rw = dict()
    if url1 != None:
      req = requests.get(url1)
      sup = BeautifulSoup(req.content, 'html.parser')
      req = requests.get(url1)
      sup = BeautifulSoup(req.content, 'html.parser')
      tit_dv = sup.find('header', class_='mw-body-header vector-page-titlebar', recursive=True)
      if tit_dv:
            tit = tit_dv.find('h1')
            tit_text = tit.text
      else:
            tit_text = ' '

      cont_dv = sup.find(id='bodyContent', recursive=True)
      if cont_dv:
            cont = cont_dv.find_all('p', recursive=True)
            cont = " ".join([pr.text for pr in cont])
      else:
            cont = ' '
      cont = cont + tit_text
    else:
        cont = para
    sntns = cont.split(".");
    num_sntns = len(sntns)
    cont_pnc = re.sub(r'[^\w\s]', ' ', cont)
    cont_pnc = cont_pnc.replace('\n', ' ')
    cont_pnc = re.sub(' +', ' ', cont_pnc)
    cont_pnc = cont_pnc.lower()
    wrds = cont_pnc.split(" ");
    num_wrds = len(wrds)
    wrd_pr_sntns = num_wrds / (num_sntns + 0.000001)
    prnoun_cnt = Counter(wrds)
    num_prnoun = prnoun_cnt['i'] + prnoun_cnt['we'] + prnoun_cnt['ours'] + prnoun_cnt['us'] + prnoun_cnt['my']
    num_char = len(list(cont_pnc.replace(' ', '')));
    char_per_wrd = num_char / (num_wrds + 0.000001)

    wrds_tok = word_tokenize(cont_pnc)
    wrds_tok_stp = [wrd for wrd in wrds_tok if wrd not in stopwords.words('english')]
    num_wrds_stp = len(wrds_tok_stp)
    ps = PorterStemmer()
    wrds_tok_stp_stm = [ps.stem(wrd) for wrd in wrds_tok_stp]
    st = nltk.tokenize.sonority_sequencing.SyllableTokenizer()
    num_syllb = len(st.tokenize(wrds_tok_stp_stm))
    syllb_pr_wrd = num_syllb / (num_wrds_stp + 0.000001)
    syllb_in_wrd = [syllables.estimate(wrd) for wrd in wrds_tok_stp_stm]
    syllb_grtr_2 = len([x for x in syllb_in_wrd if x > 2])
    avg_cmplx_wrds = syllb_grtr_2 / (num_wrds_stp + 0.000001)
    wrd_pr_sntns_stp = num_wrds_stp / (num_sntns + 0.000001)
    fog_indx = 0.4 * (avg_cmplx_wrds + wrd_pr_sntns_stp)

    rw['WORD COUNT'] = num_wrds_stp
    rw['PERSONAL PRONOUNS'] = num_prnoun
    rw['SYLLABLE PER WORD'] = syllb_pr_wrd
    rw['COMPLEX WORD COUNT'] = syllb_grtr_2
    rw['AVG NUMBER OF WORDS PER SENTENCE'] = wrd_pr_sntns
    rw['FOG INDEX'] = fog_indx
    rw['PERCENTAGE OF COMPLEX WORDS'] = avg_cmplx_wrds
    rw['AVG SENTENCE LENGTH'] = wrd_pr_sntns_stp
    rw['AVG WORD LENGTH'] = char_per_wrd

    pos = 0;
    neg = 0
    with open('positive-words.txt', 'r') as fl:
        pos_wrds = fl.read().replace('\n', ' ')
    with open('negative-words.txt', 'r', encoding="ISO-8859-1") as fl:
        neg_wrds = fl.read().replace('\n', ' ')

    pos_wrds = pos_wrds.split(' ');
    neg_wrds = neg_wrds.split(' ');
    for wrd in wrds_tok_stp:
        if wrd in pos_wrds:
            pos = pos + 1
        if wrd in neg_wrds:
            neg = neg + 1

    pol_scr = (pos - neg) / (pos + neg + 0.000001)
    sub_scr = (pos + neg) / (num_wrds_stp + 0.000001)

    rw['POSITIVE SCORE'] = pos
    rw['NEGATIVE SCORE'] = neg
    rw['POLARITY SCORE'] = pol_scr
    rw['SUBJECTIVITY SCORE'] = sub_scr

    return rw , cont