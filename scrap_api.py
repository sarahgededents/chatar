import datetime
import requests
import re

quinte_info = requests.get("https://turfinfo.api.pmu.fr/rest/client/61/evenements/quinte?specialisation=INTERNET").json()

date = input("Please enter a date (by default next quinte): (format ddmmyyyy) ")
def check_date(d):
    pattern = re.compile("^[0-3][0-9][0-1][0-9][0-9][0-9][0-9][0-9]$")
    if not d:
        return datetime.datetime.fromtimestamp(quinte_info['quinte']['heureDepart']/1000).strftime("%d%m%Y")
    while not pattern.match(d):
        d = input("Please enter a date: (format ddmmyyyy) ")
    return f'{d}'


date = check_date(date)

prono = False
data = True
if datetime.datetime.strptime(date, "%d%m%Y") > datetime.datetime.fromtimestamp(quinte_info['quintePasse']['heureDepart']/1000):
    if datetime.datetime.strptime(date, "%d%m%Y").date() != datetime.datetime.fromtimestamp(quinte_info['quinte']['heureDepart']/1000).date():
        numReu = input("Numéro de réunion: ")
        numCourse = input("Numéro de course: ")
        quinte = False
    else:
        quinte = True
        numCourse = quinte_info['quinte']['numeroCourse']
        numReu = quinte_info['quinte']['numeroExterneReunion']
    print(f"https://www.pmu.fr/turf/{date}/R{numReu}/C{numCourse}")
    print("=============================================")

    try:
        run_info = requests.get(f"https://turfinfo.api.pmu.fr/rest/client/61/programme/{date}/R{numReu}/C{numCourse}/participants?specialisation=INTERNET").json()
        past_run_info = requests.get(f"https://online.turfinfo.api.pmu.fr/rest/client/61/programme/{date}/R{numReu}/C{numCourse}/performances-detaillees/pretty").json()

        h_score = {}
        # print(f"https://turfinfo.api.pmu.fr/rest/client/61/programme/{date}/R{numReu}/C{numCourse}/participants?specialisation=INTERNET")
        for c in range(len(run_info['participants'])):
            h_info = run_info['participants'][c]
            nomCheval = h_info['nom']
            try:
                s1 = (h_info['nombreVictoires'] + 0.8 * h_info['nombrePlacesSecond'] + 0.6 * h_info['nombrePlacesTroisieme']) / h_info['nombreCourses']
            except:
                s1 = 0
            s2_step = 0
            pr_info = past_run_info['participants'][c]['coursesCourues']
            for course in pr_info:
                course_date = datetime.datetime.fromtimestamp(course['date']/1000).date()
                ratio = 1 - (datetime.datetime.today().date() - course_date).days / 365
                if ratio < 0:  # if run was before a year ago
                    ratio = 0
                rank_h = 0  # by default if no rank
                for p in course['participants']:  # get rank of participant
                    if p['nomCheval'] == nomCheval:
                        if p['place']['statusArrivee'] == 'PLACE':
                            rank_h = p['place']['place']
                        else:
                            rank_h = 0
                s2_step += ratio * (1 - (rank_h - 1) / course['nbParticipants']) if rank_h != 0 else 0
            try:
                s2 = s2_step / len(pr_info)
            except:
                s2 = 0
            h_score[c+1] = (s1 + s2) / 2
        #print(h_score)
        prono = list(dict(sorted(h_score.items(), key=lambda item: item[1], reverse=True)).keys())
        if quinte:
            print(f'Pronostic Quinté: {prono}')
        else:
            print(f'Pronostic Réunion {numReu}, Course {numCourse}: {prono}')
    except:
        data = False
        print("No available data at the moment.")

else:
    numCourse = quinte_info['quintePasse']['numeroCourse']
    numReu = quinte_info['quintePasse']['numeroExterneReunion']
    date = datetime.datetime.fromtimestamp(quinte_info['quintePasse']['heureDepart'] / 1000).strftime("%d%m%Y")

    print(f"https://www.pmu.fr/turf/{date}/R{numReu}/C{numCourse}")
    print("=============================================")

    r = quinte_info['quintePasse']['ordreArrivee']
    res = [r[i][0] for i in range(len(r))]
    print(f'Résultat Quinté: {res}')
