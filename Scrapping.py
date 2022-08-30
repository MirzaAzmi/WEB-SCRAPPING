import requests

import pandas as pd

from bs4 import BeautifulSoup



base_url='https://www.themoviedb.org/movie?page='

links=[]

for num in range(1,251):

    links.append(base_url+str(num))



my_movie_list=[]

for url in links:

    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.51 Safari/537.36'}

    r=requests.get(url,headers=header)

    html_code=r.text

    soup=BeautifulSoup(html_code,'lxml')

    all_divs=soup.find_all('div',class_='card style_1')

    for item in all_divs:

        url=item.find('div',class_='wrapper').a['href']

        r1=requests.get('https://www.themoviedb.org'+url,headers=header)

        html_code1=r1.text

        soup1=BeautifulSoup(html_code1,'lxml')

        all_divs1=soup1.find_all('div',"header_poster_wrapper false")

        for item in all_divs1:

            Name=item.find('h2').a.text

            Ratings=item.find('div',class_='user_score_chart')['data-percent']

            Genere=item.find('span',class_='genres').text.replace('\n','').replace('\xa0','')

            Rel_date=item.find('span',class_='release').text.split()[0]

            if not item.find('span',class_='runtime'):continue

            Runtime=item.find('span',class_='runtime').text.strip()            

            url1=url

            movie_url=('https://www.themoviedb.org'+url1)

            if not item.find('li',class_='profile'):continue

            Movie_Director=item.find('li',class_='profile').a.text

            all_movie_list={

                'Name':Name,

                'Rating':Ratings,

                'Genre':Genere,

                'Release date':Rel_date,

                'Runtime':Runtime,

                'Director':Movie_Director,

                'Url':movie_url

            }

            my_movie_list.append(all_movie_list)



print(my_movie_list)



job_df=pd.DataFrame(my_movie_list)

job_df.to_csv('MOVIE DATA')