import os
import configparser
from download_torrent import GetTorrent
from get_episode_list import GetEpisode


def get_shows():
    config = configparser.ConfigParser()
    config.read('config.ini')
    shows_list = config.sections()
    shows_list.pop(0)
#    print(shows_list)
    return shows_list


def get_logpass():
    config = configparser.ConfigParser()
    config.read('config.ini')
    loginpassword = [config['logpass']['login'], config['logpass']['password']]
    return loginpassword


def get_lastwatched(show):
    config = configparser.ConfigParser()
    config.read('config.ini')
    lastseason = config[show]['lastseason']
    lastepisode = config[show]['lastepisode']
    lastwatched = [lastseason, lastepisode]
    return lastwatched


def get_new(show, lastwatch, loginpassword):
    baseurl = 'http://www.lostfilm.tv/series/'
    last_episode = baseurl + show + '/season_' + lastwatch[0] + '/episode_' + lastwatch[1] + '/'
    episodes = GetEpisode(show).episodes
    index = episodes.index(last_episode)
    list_to_dl = episodes[:index]
    for dl in list_to_dl:
        GetTorrent(dl, loginpassword)
    return last_episode


def main():
    loginpassword = get_logpass()
    shows = get_shows()
    for show in shows:
        lastwatch = get_lastwatched(show)
        get_new(show, lastwatch, loginpassword)


if __name__ == '__main__':
    main()