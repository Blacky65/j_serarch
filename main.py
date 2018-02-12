# -*- coding:utf-8 -*-
import argparse
import pandas as pd


def createparser():
    parser = argparse.ArgumentParser(description='Process some value\'s')
    parser.add_argument('-j', '--j', help='Journal', dest='journal')
    parser.add_argument('-t', '--t', help='Search users that have made the greatest amount of data', dest='most_request')
    parser.add_argument('-b', '--b', help='Search users that have made the greatest amount of requests', dest='byte_out')
    parser.add_argument('-f', '--f', help='Search regular queries by user', dest='search')
    parser.add_argument('-p', '--p', help='Search regular queries by ip', dest='ip')
    return parser


def data_cvs(journal):
    fixed = pd.read_csv(journal,
                        sep=',', encoding='utf-8',
                        date_parser=[['src_user'], ['src_ip']])
    return fixed


def top_request_send(data, val):
    with open('result.txt', 'a', encoding='utf-8') as file:
        print('\n#Поиск {} пользователей, сгенерировавших наибольшее количество запросов:\n'.format(val), file=file)
        print(data['src_user'].value_counts()[:int(val)], file=file)


def top_data_send_summ(data, val):
    with open('result.txt', 'a', encoding='utf-8') as file:
        print('\n#Поиск {} пользователей, отправивших наибольшее количество данных\n'.format(val), file=file)
        res = pd.pivot_table(data, values=['output_byte'], index=['src_user'], aggfunc='sum')
        res1 = res.sort_values('output_byte', axis=0, ascending=False)
        print(res1[:int(val)], file=file)


def sames_request_by_user(data, val):
    with open('result.txt', 'a', encoding='utf-8') as file:
        print('\n#Поиск регулярных запросов (запросов выполняющихся периодически) по полю src_user = {}\n'.format(val),
              file=file)
        sort_data = data.groupby(['src_user', 'dest_ip', 'dest_port']).size().reset_index(name='Запросы')
        reqests_data_sorted = sort_data.sort_values('Запросы', ascending=False)
        print(
            reqests_data_sorted[['dest_ip', 'dest_port', 'Запросы']][reqests_data_sorted['src_user'].str.contains(val)],
            file=file)


def sames_request_by_ip(data, val):
    with open('result.txt', 'a', encoding='utf-8') as file:
        print('\n#Поиск регулярных запросов (запросов выполняющихся периодически) по полю src_ip = {}\n'.format(val),
              file=file)
        sort_data = data.groupby(['src_ip', 'dest_ip', 'dest_port']).size().reset_index(name='Запросы')
        reqests_data_sorted = sort_data.sort_values('Запросы', ascending=False)
        print(reqests_data_sorted[['dest_ip', 'dest_port', 'Запросы']][reqests_data_sorted['src_ip'].str.contains(val)],
              file=file)


if __name__ == "__main__":
    try:
        parser = createparser()
        data = parser.parse_args()
        opened_cvs = data_cvs(data.journal)

        if data.most_request != None:
            top_request_send(opened_cvs, data.most_request)
        if data.byte_out != None:
            top_data_send_summ(opened_cvs, data.byte_out)
        if data.search != None:
            sames_request_by_user(opened_cvs, data.search)
        if data.ip != None:
            sames_request_by_ip(opened_cvs, data.ip)
    except:
        print("""
#
#     ___      .__   __.      ___       __      ____    ____  ________   _______    ____    ____  ___      __
#    /   \     |  \ |  |     /   \     |  |     \   \  /   / |       /  |   ____|   \   \  /   / / _ \    /_ |
#   /  ^  \    |   \|  |    /  ^  \    |  |      \   \/   /  `---/  /   |  |__       \   \/   / | | | |    | |
#  /  /_\  \   |  . `  |   /  /_\  \   |  |       \_    _/      /  /    |   __|       \      /  | | | |    | |
# /  _____  \  |  |\   |  /  _____  \  |  `----.    |  |       /  /----.|  |____       \    / __| |_| |  __| |
#/__/     \__\ |__| \__| /__/     \__\ |_______|    |__|      /________||_______|       \__/ (__)\___/  (__)_|
#
#.______   ____    ____         _______..___  ___.   ______    __  ___  _______
#|   _  \  \   \  /   /        /       ||   \/   |  /  __  \  |  |/  / |   ____|
#|  |_)  |  \   \/   /        |   (----`|  \  /  | |  |  |  | |  '  /  |  |__
#|   _  <    \_    _/          \   \    |  |\/|  | |  |  |  | |    <   |   __|
#|  |_)  |     |  |        .----)   |   |  |  |  | |  `--'  | |  .  \  |  |____
#|______/      |__|        |_______/    |__|  |__|  \______/  |__|\__\ |_______|
#
#
#        Синтаксис программы следующий:
#
#        >python main.py -j shkib.csv -t 5 -b 5 -f f2b28434a4b03d943c94c9224b3e6a7c -p 9ec3b27794d1d302fa04a94836249f4a
#
#        Обязательные опции:
#        j - Журнал
#        t - Количество пользователей, сгенерировавших наибольшее количество запросов в отчет
#        b - Количество пользователей, отправивших наибольшее количество данных
#        f - Поиск регулярных запросов (запросов выполняющихся периодически) по полю src_user
#        p - Поиск регулярных запросов (запросов выполняющихся периодически) по полю src_ip    
#        
#        Помощь:
#        h - Помощь
#        
#        Связь: email:sergmadox@yandex.com       
""")
