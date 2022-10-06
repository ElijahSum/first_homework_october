#!/usr/bin/env python
# coding: utf-8

# In[238]:


import csv

def primal_prints_answer():
    '''Выводит первичный вопрос при запуске программы, сохраняет результаты ответа'''
    print('Какую функцию вы хотите выполнить? Введите соответствующую цифру:')
    print('1. Вывести иерархию команд')
    print('2. Вывести сводный отчёт по департаментам')
    print('3. Сохранить сводный отчет по департаментам в csv файл')
    answer = 0
    while answer not in [1, 2, 3]:
        answer = int(input('Введите необходимую цифру: '))
    print()
    return answer


def hierarchy_create(department, part, dict_department):
    '''Добавляет ключи и модифицирует словарь, в котором записана иерархия отделов в департаментах'''
    if department not in dict_department.keys():
        dict_department[department] = [part]
    elif part not in dict_department[department]:
        dict_department[department].append(part)
    return dict_department


def statistics_create(dict_statistics, department, salary):
    '''Создает и модифицирует словарь со статистиками по департаментам'''
    salary = int(salary)
    if department not in dict_statistics['dep_name']:
        dict_statistics['dep_name'].append(department)
        dict_statistics['population'].append(0)
        dict_statistics['min'].append(salary)
        dict_statistics['max'].append(salary)
        dict_statistics['mean'].append(salary)
    else:
        i = 0
        while dict_statistics['dep_name'][i] != department:
            i += 1
        dict_statistics['population'][i] += 1
        if salary < dict_statistics['min'][i]:
            dict_statistics['min'][i] = salary
        elif salary > dict_statistics['max'][i]:
            dict_statistics['max'][i] = salary
        dict_statistics['mean'][i] += salary
    return dict_statistics


def print_departments(dict_hierarchy):
    '''В случае, если пользователь вводит 1, то начинает работу эта функция, которая выводит
    состав всех департаментов фирмы, поясняет из каких отделов состоят департаменты'''
    for key, value in dict_hierarchy.items():
        print(f'Департамент "{key}" состоит из следующих отделов: ', end = '')
        print(*value, sep = ', ')
   

def print_statistics(dict_statistics, answer):
    '''Выводит статистику по департаментам в окно функции, если введена цифра 2.
    Сохраняет полученные результаты в файл result_department.csv, если введена цифра 3.'''
    true_means = []
    for k, value in enumerate(dict_statistics['mean']):
            true_means.append(round(value / dict_statistics['population'][k]))
    dict_statistics['mean'] = true_means
    if answer == 2:
        for i in range(0, len(dict_statistics.keys())):
            print(f"В отделе {dict_statistics['dep_name'][i]}: {dict_statistics['population'][i]} человек. Минимальная зарплата: {dict_statistics['min'][i]}, Максимальная: {dict_statistics['max'][i]}, Средняя: {dict_statistics['mean'][i]}")
    if answer == 3:
        with open('result_department.csv', 'w', newline='') as csvfile:
            spamwriter = csv.writer(csvfile, delimiter=';')
            result_dict = []
            for i in range(0, len(dict_statistics.keys())):
                result_dict.append([])
            for i, val in enumerate(dict_statistics.values()):
                for j, res in enumerate(val):
                    result_dict[j].append(res)
            spamwriter.writerow(dict_statistics.keys())
            spamwriter.writerows(result_dict)
        print('Удачно! Данные сохранены в файл result_department.csv!')



def main():
    '''Основная функция - создает словари, открывает файл, разграничивает действия в зависимости от полученного
    ответа'''
    answer = primal_prints_answer()
    dict_hierarchy = dict()
    dict_statistics = {'dep_name': [], 'population': [], 'min': [], 'max': [], 'mean': []}
    with open('Corp_Summary.csv', 'r') as infile:
        i = 0
        for i, string in enumerate(infile):
            lst_strings = string.splitlines()[0].split(';')
            if i != 0 and answer == 1:
                dict_hierarchy = hierarchy_create(lst_strings[1], lst_strings[2], dict_hierarchy)
            elif i != 0 and answer in [2, 3]:
                dict_statistics = statistics_create(dict_statistics, lst_strings[1], lst_strings[5])
    if answer == 1:
        print_departments(dict_hierarchy)
    elif answer in [2, 3]:
        print_statistics(dict_statistics, answer)
    
if __name__ == '__main__':
    main()


# In[ ]:




