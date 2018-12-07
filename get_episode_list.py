import requests
from bs4 import BeautifulSoup

site_url = 'http://www.lostfilm.tv'


class GetEpisode(object):

    def xstr(self, s):
        if s is None:
            return """PlayEpisode('0')"""
        return str(s)

    def get_html(self, url):
        r = requests.get(url)
        return r.text

    def get_ep_beta(self, html):
        soup = BeautifulSoup(html, 'lxml')
        series = soup.find('div', class_='series-block')
        ep_beta = []
        for i in (range(len(series.find_all('td', class_='beta')))):
            ep_b = series.find_all('td', class_='beta')[i].get('onclick')
            ep_beta.append(ep_b[6:-8])
        return list(ep_beta)

    def get_ep_zeta(self, html):
        soup = BeautifulSoup(html, 'lxml')
        series = soup.find('div', class_='series-block')
        ep_zeta = []
        for i in (range(len(series.find_all('td', class_='zeta')))):
            ep_z = series.find_all('td', class_='zeta')[i].find('div', class_='external-btn').get('onclick')
            ep_zeta.append(self.xstr(ep_z))
        return list(ep_zeta)

    def get_final_list(self, list1, list2):
        ep_final = []
        for i in range(len(list1)):
            if list2[i] != "PlayEpisode('0')":
                ep_final.append(list1[i])
        return list(ep_final)

    def get_links(self, list_of_series):
        links = []
        for i in range(len(list_of_series)):
            episode_link = site_url + list_of_series[i]
            links.append(episode_link)
        return list(links)

    def get_eps(self, show):
        series_part = '/series/'
        query_part = show
        seasons_part = '/seasons/'

        url_gen = site_url + series_part + query_part + seasons_part
        res_beta = self.get_ep_beta(self.get_html(url_gen))
        res_zeta = self.get_ep_zeta(self.get_html(url_gen))
        list_final = self.get_final_list(res_beta, res_zeta)
        eps_links = self.get_links(list_final)


        return eps_links

    def __init__(self, show):
        self.episodes = self.get_eps(show)
