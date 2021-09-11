import datetime
import scrap

horses_info = scrap.horse_info

h_score = {}

for c in range(len(horses_info)):
    h_info = horses_info[c+1]
    s1 = (h_info['n_victory'] + 0.7 * h_info['n_podium']) / h_info['n_runs']
    s2_step = 0
    nrun = len(h_info['past_runs'])
    for r in range(nrun):
        run_info = h_info['past_runs'][f'r{r+1}']
        ratio = 1 - (datetime.datetime.today().date() - run_info['date']).days / 365
        if ratio < 0:  # if run was before a year ago
            ratio = 0
        s2_step += ratio * (1 - (run_info['rank'] - 1) / run_info['n_starters']) if run_info['rank'] != 0 else 0
    s2 = s2_step / nrun
    h_score[c+1] = (s1 + s2) / 2
#print(h_score)
for np in scrap.nstart:  # if the horse is a non-starter, horse_score = 0 to ignore him
    h_score[np] = 0
print("=============================================")
print(f'Pronostic Quinté: {list(dict(sorted(h_score.items(), key=lambda item: item[1], reverse=True)).keys())}')
