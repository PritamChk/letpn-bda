import json
import random as rnd
import pathlib
import time
import typer as t
import os
from letpn_bda.quiz_func import *

BASEDIR = pathlib.Path().absolute()

app = t.Typer()

@app.callback()
def callback():
    """
    Awesome NPTEL Quiz
    """

@app.command()
def join_weeks(
    # from_:int=t.Option(1,'-f',help="from which week: #"),
    # to_:int = t.Option(9,'-t',help="to which week: #")
):
    folder = "db"
    weeks_json = os.listdir(BASEDIR/folder)
    quiz = {"data": []}
    with t.progressbar(weeks_json, label="Merging : ", fill_char=t.style(" ", bg=t.colors.YELLOW)) as weeksjson:
        for each_week in weeksjson:
            time.sleep(.2)
            with open(BASEDIR/folder/each_week, "r") as file:
                wq = json.load(file)
                quiz["data"].append(wq)
    quiz_data = json.dumps(quiz, indent=4)
    saved_file = "quiz_data.json"
    with open(saved_file, "w") as file:
        file.write(quiz_data)
    t.echo(
        "---------------------------------------------------" +
        "\n|Your Combined quiz data saved at location ->\n|" +
        t.style(f"{BASEDIR/saved_file}", fg=t.colors.BLUE) +
        "\n---------------------------------------------------\n"
    )


@app.command()
def startquiz(
        name: str = t.Option("Hola", prompt="Write Your Name"),
        week_no: int = t.Option(rnd.randint(1, 9)  # TODO change 9 to 12
                                , "--week-no", "-n", min=1, max=12,
                                help="by default 1 and range  [ 1<=x<=12 ]"),
        weekly: bool = t.Option(
            True, "--weekly/--random", "-w/-r", help="If True then qus given weekly else taken randomly from any week"),
        no_qus: int = t.Option(10, '--no-qus', "-q", min=3,
                               max=90,  # TODO: change 90 -> 120
                               help="This is applicable for Random Quiz")
):
    """
        --week-no : the week no you want to practice

        -w : if you want to practice qustions by week or randomly from any where
            if -w true then weekly else randomly and then you have to provide how many questions you want to practice

        -q : no of qus you want to practice
    """
    clearConsole()
    name = t.style(name, bold=True, fg=t.colors.RED)
    t.echo("\nWelcome "+name +
           "\n----------------------\nYour Quiz Has been started: \n")
    if weekly:
        quiz_db_file = f"week{week_no}.json"
        # no_qus: int = 10
        quiz: dict = {}
        with open(BASEDIR/"db"/quiz_db_file, "r") as jsonfile:
            quiz = json.load(jsonfile)
        qweek: int = quiz["week"]
        t.secho(
            f"Week : {qweek}\n-----------------------\n", fg=t.colors.YELLOW
        )

        quiz_questions = quiz['qustions']
        rnd.shuffle(quiz_questions)
        total_marks = 0
        attempted_qus = 0

        with t.progressbar(quiz_questions, label="progress", fill_char=t.style(" ", bg=t.colors.BRIGHT_MAGENTA)) as qq:
            for qus in qq:
                attempted_qus += 1
                qus_options = qus.get("options")
                rnd.shuffle(qus_options)
                t.echo(f"\n{qus.get('qno')} ) {qus.get('statement')}")

                for i in range(1, 5):
                    t.echo(f"{i}) {qus_options[i-1].get('value')}")

                ans = t.prompt("Select Option no [1-4]", type=int)
                if not (ans >= 1 and ans <= 4):
                    t.secho("Bokachoda thik kore input de", fg="red")
                    ans = t.prompt("Select Option no [1-4]", type=int)
                    if not (ans >= 1 and ans <= 4):
                        t.secho(
                            "Bokachoda Gandu,  thik kore input dite jane na\n Vag Bara", fg="red")
                        show_result(attempted_qus, total_marks, 10)
                        raise t.Abort()

                ans_success = t.colors.RED

                if qus_options[ans-1].get("is_correct") == True:
                    ans_success = t.colors.GREEN
                    total_marks += 1

                clearConsole()
                # print qus ans by clearing the previous screen
                t.echo(f"{qus.get('qno')} ) {qus.get('statement')}")
                for i in range(1, 5):
                    time.sleep(.1)
                    if i == ans:
                        t.secho(
                            f"{i}) {qus_options[i-1].get('value')}", fg=ans_success)
                    elif qus_options[i-1].get("is_correct") == True:
                        t.secho(
                            f"{i}) {qus_options[i-1].get('value')}", fg=t.colors.GREEN)
                    else:
                        t.echo(f"{i}) {qus_options[i-1].get('value')}")
                cnf = t.confirm("Next Qus [press enter to continue] ", True)
                if not cnf:
                    clearConsole()
                    show_result(attempted_qus, total_marks, 10)
                    raise t.Abort()
                clearConsole()
        show_result(attempted_qus, total_marks, 10)
    else:
        json_db_file_path = BASEDIR/"quiz_data.json"
        # json_data = {}
        with open(json_db_file_path, "r") as file:
            json_data = json.load(file)
        quiz_list: list[dict] = json_data.get("data")
        random_qus_set = []
        combo = generate_combo()
        random_qus_set.append(combo)
        count = 1
        while count < no_qus:
            combo = generate_combo()
            if combo not in random_qus_set:
                random_qus_set.append(combo)
                count += 1
        # RESULT VARIABLES
        attempted_qus = 0
        total_marks = 0
        # -----------------
        clearConsole()
        with t.progressbar(random_qus_set, label="Progress ", fill_char=t.style(" ", bg=t.colors.MAGENTA)) as qus_set:
            for qus_combo in qus_set:
                total_marks += show_qus_and_get_ans(qus_combo, quiz_list)
                attempted_qus += 1
                cnf = t.confirm("Next qus [Press Enter]", True)
                if not cnf:
                    clearConsole()
                    show_result(attempted_qus, total_marks, no_qus)
                    raise t.Abort()
                clearConsole()
        clearConsole()
        show_result(attempted_qus, total_marks, no_qus)


@app.command()
def addqus(
    week: int = t.Option(..., "-w", min=1, max=12,
                         help="Provide the week no and week#.txt should exist in same directory"),
    noq: int = t.Option(10, "-n", min=1, max=10,
                        help="Enter No of Qus to be converted",)
):
    """
        Per week 10 qustions will be taken input via file: week#.txt

        & per qus 4 options will be added

        After that the ans options have to be added

        ## NB: Case sensitive comparisions

        example:

        ---------

        who are you?

        Human

        Yeti

        Dog

        Cat

        Human


        -w : week no for short notation

        -n : no of qus short notation
    """
    qbank_file = "week"+str(week)
    no_options = 4
    # noq = 10
    questions = []
    options = []
    readlines = []
    qbank_json = {
        "week": week
    }
    with open(BASEDIR/"raw_text"/(qbank_file+".txt"), "r") as file:
        readlines = file.readlines()

    import time
    label = t.style("Convertion", fg=t.colors.GREEN)
    fchar = t.style(" ", bg=t.colors.GREEN)
    t.echo("")
    with t.progressbar(range(noq), fill_char=fchar, label=label) as noqs:
        for index in noqs:
            time.sleep(.03)
            qstatement = readlines.pop(0).rstrip("\n")
            options = readlines[:4]
            ans = readlines[4]
            options = [
                {
                    "value": op.rstrip("\n").strip(),
                    "is_correct": op.rstrip("\n").strip() == ans.rstrip("\n").strip()
                } for op in options
            ]
            for _ in range(no_options+1):
                readlines.pop(0)

            questions.append(
                {
                    'qno': index+1,
                    "statement": qstatement,
                    "options": options
                }
            )
    qbank_json["qustions"] = questions
    json_object = json.dumps(qbank_json, indent=4)
    save_location = BASEDIR/"db"/(qbank_file+".json")
    with open(save_location, "w") as f:
        f.write(json_object)
    success_msg = f"| Your "+t.style(f"week{week}.txt", fg=t.colors.BRIGHT_RED)+" has been successfuly converted to "+t.style(
        f"week{week}.json", fg=t.colors.GREEN, bold=True)
    qbank_json_file = qbank_file+".json"
    t.echo(
        "\n-----------------------------------------------------------------\n" +
        success_msg +
        "\n| file saved in location ->  " +
        t.style(f"{BASEDIR/qbank_json_file}", fg=t.colors.BRIGHT_CYAN) +
        "\n-----------------------------------------------------------------\n"
    )

