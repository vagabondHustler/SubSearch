from dataclasses import dataclass


@dataclass
class Precentage:
    precentage: int


# compare two lists  with each other and return match in %
def check(from_pc: str or int, from_browser: str or int) -> Precentage:
    max_precentage = 100
    pc_list: list = mk_lst(from_pc)
    browser_list: list = mk_lst(from_browser)
    not_matching = list(set(pc_list) - set(browser_list))
    not_matching_value = len(not_matching)
    number_of_items = len(pc_list)
    precentage_to_remove = round(not_matching_value / number_of_items * max_precentage)
    precentage = round(max_precentage - precentage_to_remove)

    return Precentage(precentage)


# create list from string
def mk_lst(release: str or int) -> list:
    new: list = []
    qualities = ["720p", "1080p", "1440p", "2160p"]

    temp: list = release.split(".")

    for item in temp:
        if item not in qualities:
            new.append(item.lower())
    return new


# check if strings are equal length
def check_size_difference(x: list, y: list) -> int:
    if len(x) > len(y):
        answer = len(x) - len(y)
        return answer
    elif len(x) < len(y):
        answer = len(y) - len(x)
        return answer


def make_list_iterable(x: list, y: list, size_difference: int):
    if len(x) < len(y):
        for _isb_answer in range(size_difference):
            x.append("_None")
    elif len(x) > len(y):
        for _isb_answer in range(size_difference):
            y.append("_None")
    return x, y


# compare two items
def compare(x: str or int, y: str or int) -> bool:
    if x.lower() == y.lower():
        return True
    return False


def calculate_item_value(x: int, max_value=100) -> int:
    number_of_items = x
    value_of_item = max_value / number_of_items
    return value_of_item