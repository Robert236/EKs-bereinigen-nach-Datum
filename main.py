import csv
from datetime import datetime

basic_data = []
basic_data_only_one_article = []
data_to_print = []

with open('Einspieldatei EKs Beispieldatei.csv', 'r') as inputFile:
    rv_csv = csv.DictReader(inputFile, delimiter=';')
    for line in rv_csv:
        basic_data.append(line)


def kalk_wirksam_right_place(articles):
    count_articles = len(articles)
    if count_articles > 1:
        for e, article in enumerate(articles):
            if e == 1:
                article['Kalk_wirksam'] = 'X'
            else:
                article['Kalk_wirksam'] = ''
    else:
        for article in articles:
            if article['Staffelmenge'] != '':
                article['Kalk_wirksam'] = 'X'
            else:
                article['Kalk_wirksam'] = ''
    return articles


def build_date(date):
    hashlist = list(date)
    hashlist.insert(4, '-')
    hashlist.insert(7, '-')
    format_date = ''.join(hashlist)
    return format_date


def check_date_between(periods2):
    date_of_today = datetime.today().strftime('%Y-%m-%d')
    for period_of_time in periods2:
        if period_of_time['Startdatum'] < date_of_today < period_of_time['Enddatum'] \
                or period_of_time['Startdatum'] == date_of_today or period_of_time['Enddatum'] == date_of_today:
            return period_of_time


def check_current_date(articles):  # takes list of all same article as dictionary.
    all_periods = []
    for article in articles:
        period = {}
        dd1 = build_date(article['Startdatum'])
        dd2 = build_date(article['Enddatum'])
        period['Startdatum'] = dd1
        period['Enddatum'] = dd2
        if period not in all_periods:
            all_periods.append(period)
    rv_current_time_periode = check_date_between(all_periods)
    if rv_current_time_periode is None:
        last_date = [ee['Startdatum'] for ee in all_periods]
        last_date.sort(key=lambda date22: datetime.strptime(date22, "%Y-%m-%d"))
        last_date = last_date[-1].replace('-', '')
        dates_return = []
        for article2 in articles:
            if article2['Startdatum'] == str(last_date):
                dates_return.append(article2)
        return dates_return
    else:
        rv_current_time_periode = rv_current_time_periode['Startdatum'].replace('-', '')
        dates_return = []
        for article2 in articles:
            if article2['Startdatum'] == str(rv_current_time_periode):
                dates_return.append(article2)
        return dates_return


for dataset in basic_data:
    if dataset['Artikel_nr'] not in [line['Artikel_nr'] for line in basic_data_only_one_article]:
        basic_data_only_one_article.append(dataset)

# main

for dataset in basic_data_only_one_article:
    sum_of_one_article = []
    current_number = dataset['Artikel_nr']
    for dataset2 in basic_data:
        if dataset2['Artikel_nr'] == current_number:
            sum_of_one_article.append(dataset2)
    rv_current_date = check_current_date(sum_of_one_article)
    rv_current_date = kalk_wirksam_right_place(rv_current_date)
    for print_out in rv_current_date:
        data_to_print.append(print_out)

# for i in data_to_print:
    # del i['']

count = 0
with open('output_EKs_bereinigt.csv', 'w') as csvfile:
    fieldnames = ['Lieferanten_nr', 'Lieferanten_matnr', 'Artikel_nr', 'Preisenheit', 'Mengeneinheit',
                  'Staffelmenge', 'Preis', 'Waehrung', 'Code', 'Startdatum', 'Enddatum', 'Kalk_wirksam']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames, delimiter=';')
    writer.writeheader()
    for see in data_to_print:
        count += 1
        writer.writerow(see)
print(count)
