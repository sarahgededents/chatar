import datetime
import scrap

infos_chev = scrap.infos_cheval

score_cheval = {}

for c in range(len(infos_chev)):
    cheval_info = infos_chev[c+1]
    s1 = (cheval_info['nwin'] + 0.7 * cheval_info['npodium']) / cheval_info['total']
    s2_etap = 0
    n_course = len(cheval_info['past_run'])
    for r in range(n_course):
        run_info = cheval_info['past_run'][f'course{r+1}']
        s2_etap += (1 - (datetime.datetime.today().date() - run_info['date']).days / 365) * (1 - (run_info['arrivee'] - 1) / run_info['partants']) if run_info['arrivee'] != 0 else 0
    s2 = s2_etap / n_course
    score_cheval[c+1] = (s1 + s2) / 2
print(score_cheval)
print(list(dict(sorted(score_cheval.items(), key=lambda item: item[1], reverse=True)).keys())[:3])
