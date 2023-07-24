from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.firefox.options import Options

print('Загружаем драйвер...')
options = Options()
options.add_argument('-headless')
driver = webdriver.Firefox(options=options)
print('Драйвер загружен')

while True:
    print('Открываем IMDB...')
    driver.get('https://www.imdb.com/')
    search = driver.find_element(By.ID, 'suggestion-search')
    print('Готовы искать фильм')
    film = input('Введите название фильма:\n')
    search.send_keys(film)
    search.submit()
    print('Запрос отправлен, ищем...')
    time.sleep(2)
    suggest = driver.find_elements(By.CLASS_NAME, 'ipc-metadata-list-summary-item')

    print('Вот что мы нашли:')
    sugres = []
    for s in suggest:
        title = s.find_element(By.CLASS_NAME, 'ipc-metadata-list-summary-item__t')
        info = s.find_element(By.CLASS_NAME, 'ipc-metadata-list-summary-item__tl').find_elements(By.TAG_NAME, 'li')
        info = ' '.join(list(map(lambda x: x.text, info)))
        sugres.append(s)
        print(f'{len(sugres)}. {title.text} ({info})')

    num = int(input('Введите номер фильма или 0 для нового запроса:\n'))
    if num != 0:
        break


print('Парсим информацию о фильме...')
sugres[num - 1].find_element(By.TAG_NAME, 'a').click()

title = driver.find_element(By.TAG_NAME, 'h1').text
origtitle = driver.find_element(By.XPATH,
        '/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/div').text
info = driver.find_elements(By.XPATH,
        '/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li')
info = list(map(lambda x: x.text, info))
if len(info) > 3:
    info = info[1] + ' ' + info[0]
else:
    info = info[0]
rating = driver.find_element(By.XPATH,
        '/html/body/div[2]/main/div/section[1]/section/div[3]/section/section/div[2]/div[2]/div/div[1]/'
        'a/span/div/div[2]/div[1]/span[1]').text

trivia = ''
tags = driver.find_elements(By.TAG_NAME, 'li')
for t in tags:
    try:
        a = t.find_element(By.TAG_NAME, 'a')
        if a.text == 'Trivia':
            trivia = t.find_element(By.CLASS_NAME, 'ipc-metadata-list-item__content-container').text
            break
    except:
        pass

cast = driver.find_element(By.CLASS_NAME, 'title-cast__grid').find_elements(By.TAG_NAME, 'a')
names = list(map(lambda x: x.text, filter(lambda x: x.get_attribute('data-testid') == 'title-cast-item__actor', cast)))
roles = list(map(lambda x: x.text, filter(lambda x: x.get_attribute('data-testid') == 'cast-item-characters-link', cast)))
actors = zip(names, roles)


print(f'{title} ({info})\n{origtitle}\nРейтинг IMDB: {rating}/10')
print('\nВ ролях:')
print('Актёр'.ljust(39), 'Роль')
for a in actors:
    print(a[0].ljust(39), a[1])
print('\nСлучайный факт:')
print(trivia)

driver.close()
