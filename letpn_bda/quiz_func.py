import time
import random as rnd
import os
import typer as t


def show_result(attempted_qus: int, total_marks: int, no_qus: int) -> None:
    print("--------------------------------------------------------------")
    t.echo(
        "| Your Result : " +
        t.style(f"{total_marks}/{no_qus}", fg=t.colors.BRIGHT_BLUE, bold=True) +
        "\n| Attempted Qus :" +
        t.style(f" {attempted_qus} / out of {no_qus}", fg=t.colors.BRIGHT_RED) +
        "\n| Percentage :" +
        t.style(f" {total_marks/no_qus:.1%}", fg=t.colors.CYAN) +
        "\n| Accuracy :" +
        t.style(f" {total_marks/attempted_qus:.2%}",
                fg=t.colors.BRIGHT_YELLOW)
    )
    print("---------------------------------------------------------------")


def generate_combo() -> list[int, int]:
    """
        this generates combination like [1,3],[2,3]
    """
    rnd.seed(time.time())
    week = rnd.randint(1, 11)  # TODO: Change 11 -> 12
    qus_num = rnd.randint(1, 10)
    combo = [week, qus_num]
    return combo


def clearConsole():
    command = 'clear'
    if os.name in ('nt', 'dos'):  # If Machine is running on Windows, use cls
        command = 'cls'
    os.system(command)


def show_qus_and_get_ans(combo: list[int], data: list[dict]) -> int:
    # clearConsole()
    t.echo()
    week, qus_no = combo
    qus: dict = data[week-1].get("qustions")[qus_no-1]
    options_list: list[dict] = qus.get("options")
    rnd.shuffle(options_list)
    t.echo(f"{qus.get('qno')} ) {qus.get('statement')}\n")
    for option, index in zip(options_list, range(1, 5)):
        t.echo(f"{index}) {option.get('value')}")
    ans = t.prompt("Choose option [1-4] ", type=int)
    if not (ans >= 1 and ans <= 4):
        t.secho("Bokachoda thik kore input de", fg="red")
        ans = t.prompt("Select Option no ", type=int)
        if not (ans >= 1 and ans <= 4):
            t.secho(
                "Bokachoda Gandu,  thik kore input dite jane na \n Vag Laora", fg="red")
            raise t.Abort()

    ans -= 1
    clearConsole()
    marks = 0
    t.echo(f"{qus.get('qno')} ) {qus.get('statement')}\n")
    for option, index in zip(options_list, range(1, 5)):
        time.sleep(.15)
        if index-1 == ans:
            color = t.colors.GREEN if options_list[ans].get(
                "is_correct") else t.colors.RED
            marks = 1 if options_list[ans].get("is_correct") else 0
            t.secho(f"{index}) {option.get('value')}", fg=color)
        else:
            color = t.colors.GREEN if option.get(
                'is_correct') else t.colors.BRIGHT_WHITE
            t.secho(f"{index}) {option.get('value')}", fg=color)

    return marks
