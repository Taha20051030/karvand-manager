import json
import os

path = r"data\karvands.json"

os.makedirs("data", exist_ok=True)

if not os.path.exists(path):
    initial_data = {
        "bootcamp": {
            "title": "Karvand Python",
            "year": 2026
        },
        "karvands": []
    }
    with open(path, "w", encoding="utf-8") as file:
        json.dump(initial_data, file, indent=4)

with open(path, "r", encoding="utf-8") as f:
    data = json.load(f)

karvands = data["karvands"]

start = """Please select one of the numbers below.
1)Add
2)Show Karvands
3)Search(id)
4)Search(skill)
5)Edit profile
6)Delete Karvand
7)General Report
8)Exit"""

if karvands:
    Id = max(k["id"] for k in karvands) + 1
else:
    Id = 1

while True:
    print(start)
    inp = int(input())
    if inp == 1:
        name = input("Please enter your name:\n")
        email = input("Please enter your email:\n")
        city = input("Please enter your city:\n")

        degree = input("Please enter your education degree:\n")
        field = input("Please enter your education field:\n")
        try:
            count_skills = int(input("How many skills do you have?\n"))
        except Exception:
            print("please enter valid number")
            continue
        ls_skills = []
        for _ in range(count_skills):
            skill_name = input("Please enter name of skill:\n")
            skill_level = input("Please enter level of skill:\n")
            while True:
                score_inp = input("Please enter score of skill:\n")
                try:
                    skill_score = int(score_inp)
                    if 0 <= skill_score <= 100:
                        break
                    else:
                        print("skill_score has to be between 0 to 100")
                except ValueError:
                    print("please enter valid integer number")

            ls_skills.append({
                "name": skill_name,
                "level": skill_level,
                "score": skill_score
            })

        new_karvand = {
            "id": Id,
            "full_name": name,
            "email": email,
            "city": city,
            "education": {
                "degree": degree,
                "field": field
            },
            "skills": ls_skills
        }

        Id += 1
        karvands.append(new_karvand)
        data["karvands"] = karvands

        with open(path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4, ensure_ascii=False)

    elif inp == 2:
        if karvands:
            for k in karvands:
                print(f"id : {k["id"]}\n"
                      f"full_name : {k['full_name']}\n"
                      f"email : {k["email"]}\n"
                      f"city : {k["city"]}\n"
                      f"education : {k["education"]}\n"
                      f"skills : {k["skills"]}\n")
        else:
            print("There is no person to display.")

    elif inp == 3:
        search_id = int(input("Please enter the id:\n"))
        flag = True
        for k in karvands:
            if k["id"] == search_id:
                flag = False
                print(k)
                break
        if flag:
            print("This ID does not exist.")

    elif inp == 4:
        search_skill = input("Which skill are you looking for?\n")
        ls = []
        for k in karvands:
            for s in k["skills"]:
                if search_skill == s['name']:
                    ls.append(k['full_name'])
        if ls:
            print(*ls)
        else:
            print("No user with this skill was found.")

    elif inp == 5:
        search_id = int(input("Please enter the id:\n"))
        flag = True
        for k in karvands:
            if k["id"] == search_id:
                flag = False
                print("""Which section's information do you want to change?
        1) email
        2) city
        3) degree
        4) field""")
                choice = int(input())
                if choice == 1:
                    k["email"] = input("Please enter your email:\n")
                elif choice == 2:
                    k["city"] = input("Please enter your city:\n")
                elif choice == 3:
                    k["education"]["degree"] = input("Please enter your education degree:\n")
                elif choice == 4:
                    k["education"]["field"] = input("Please enter your education field:\n")
                else:
                    print("Invalid choice!")
                    break
                with open(path, "w", encoding="utf-8") as file:
                    json.dump(data, file, indent=4, ensure_ascii=False)
                break
        if flag:
            print("This ID does not exist.")

    elif inp == 6:
        search_id = int(input("Please enter the id:\n"))
        flag = True
        for k in karvands:
            if k["id"] == search_id:
                flag = False
                karvands.remove(k)
                with open(path, "w", encoding="utf-8") as file:
                    json.dump(data, file, indent=4, ensure_ascii=False)
                break

        if flag:
            print("This ID does not exist.")
    elif inp == 7:
        if not karvands:
            print("There is no person to report.")
        else:
            unique_skills = set()
            cities = set()
            ls_score = []
            for k in karvands:
                if k['city'] not in cities:
                    cities.add(k['city'])
                for s in k["skills"]:
                    ls_score.append(s['score'])
                    if s['name'] not in unique_skills:
                        unique_skills.add(s['name'])
            report = {"total_karvands" : len(karvands),
                      "total_skills" : len(unique_skills),
                      "average_skill_score" : sum(ls_score) / len(ls_score) if ls_score else 0,
                      "cities" : list(cities),
                      "unique_skills" : list(unique_skills)
                      }
            with open(r"data\report.json", "w", encoding="utf-8") as rf:
                json.dump(report, rf, indent=4, ensure_ascii=False)
            print(json.dumps(report, indent=4, ensure_ascii=False))
            print("Report saved to data/report.json")
    elif inp == 8:
        break
