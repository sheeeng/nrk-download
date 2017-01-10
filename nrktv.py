#!/usr/bin/env python

import requests
import os.path
import re
import sys

NRK_TV_API = 'https://tv.nrk.no'
NRK_TV_MOBIL_API = 'https://tvapi.nrk.no/v1'
NRK_PS_API = 'http://v8.psapi.nrk.no'
# image_url = 'http://m.nrk.no/m/img?kaleidoId={}&width={}'.format(json['imageId'], 640)

# Initialize requests session
session = requests.Session()
session.headers['app-version-android'] = '999'


class Program:
    def __init__(self, json):
        self.programId = json['programId']
        self.title = json['title']
        self.description = json['description']
        self.seriesTitle = ''
        self.seasonNumber = ''
        self.episodeNumberOrDate = ''
        self.s0xe0y = ''
        self.fileName = ''
        # self.get_details()

    def get_details(self):
        r = session.get(NRK_PS_API + '/mediaelement/' + self.programId)
        r.raise_for_status()
        json = r.json()

        self.seriesTitle = json['seriesTitle'] if json['seriesTitle'] != 'None' else ''
        self.seasonNumber = json['seasonNumber'] if json['seasonNumber'] != 'None' else ''
        self.episodeNumberOrDate = json['episodeNumberOrDate'] if json['seriesTitle'] != 'None' else ''

        if self.episodeNumberOrDate and self.episodeNumberOrDate.find(':') > 0:
            self.s0xe0y = 'S' + self.seasonNumber.zfill(2) + 'E' + self.episodeNumberOrDate.split(':')[0].zfill(2)
        else:
            self.s0xe0y = ''

        if self.seriesTitle and self.s0xe0y:
            self.fileName = os.path.join(self.seriesTitle, 'Season ' + self.seasonNumber.zfill(2),
                                         self.seriesTitle + ' - ' + self.s0xe0y + ' - ' + self.title)
        elif self.seriesTitle:
            self.fileName = os.path.join(self.seriesTitle, 'Season ' + self.seasonNumber.zfill(2),
                                         self.seriesTitle + ' - ' + json['episodeTitle'])
        else:
            self.fileName = os.path.join(self.title)

    def __str__(self):
        string = 'ID: {}\n'.format(self.programId)
        string += '    Title: {}\n'.format(self.title)
        string += '    Episode: {}\n'.format(self.episodeNumberOrDate)
        string += '    Filename: {}\n'.format(self.fileName)
        return string


class Season:
    def __init__(self, idx, json):
        self.id = json['id']
        self.name = json['name']
        self.number = idx + 1
        self.episodes = []

    def __str__(self):
        string = '{}: {} ({} ep)'.format(self.number, self.name, len(self.episodes))
        return string


class Series:
    def __init__(self, json):
        self.seriesId = json['seriesId']
        self.title = json['title']
        self.description = json['description']
        self.imageID = json['imageId']
        self.seasons = []
        self.seasonId2Idx = {}

        r = session.get(NRK_TV_MOBIL_API + '/series/' + self.seriesId)
        r.raise_for_status()
        self.json = r.json()
        for idx, season in enumerate(reversed(self.json['seasonIds'])):
            self.seasons.append(Season(idx, season))
            self.seasonId2Idx[season['id']] = idx
        self.get_episodes()

    def get_episodes(self):
        for item in reversed(self.json['programs']):
            program = Program(item)
            season_index = self.seasonId2Idx[item['seasonId']]
            self.seasons[season_index].episodes.append(program)

    def __str__(self):
        string = 'SeriesID: {}\n'.format(self.seriesId)
        string += '    Title: {}\n'.format(self.title)
        string += '    Seasons: '
        string += '{}'.format([str(season) for season in self.seasons])
        return string

    def episodes(self):
        r = session.get(NRK_TV_MOBIL_API + '/series/' + self.seriesId)
        r.raise_for_status()

        episodes = []
        for item in r.json()['programs']:
            episodes.append(Program(item))
        return episodes


def search(string):
    r = session.get(NRK_TV_MOBIL_API + '/search/' + string)
    r.raise_for_status()

    series = []
    programs = []
    for item in r.json()['hits']:
        if item['type'] == 'serie':
            series.append(Series(item['hit']))
        elif item['type'] in ['program', 'episode']:
            programs.append(Program(item['hit']))
    series.reverse()
    programs.reverse()
    return series, programs


def get_input(num_elements):
    while True:
        try:
            string = input('Enter a number or interval (e.g. 8 or 5-10). (q to quit): ')
            slice_match = re.match(r'^(\d*)[:-](\d*)$', string)
            index_match = re.match(r'^(\d+)$', string)
            quit_match = re.match(r'^q$', string.lower())
            if slice_match:
                slice_min = int(slice_match.group(1) or 0)
                slice_max = int(slice_match.group(2) or num_elements - 1)
            elif index_match:
                slice_min = int(index_match.group(1))
                slice_max = slice_min
            elif quit_match:
                print('OK, quitting program\n')
                sys.exit(0)
            else:
                raise SyntaxError('Syntax not allowed')

            # Check the values of the ints
            if slice_min > slice_max:
                raise ValueError('Max is not larger than min')
            if slice_max >= num_elements or slice_min > num_elements - 1:
                raise ValueError('Value is too high')

        except Exception as e:
            # An exception was generated above
            print('Sorry, not a valid input: {}\n'.format(e))
            continue
        else:
            # No exception generated above
            break

    return slice(slice_min, slice_max + 1)


if __name__ == '__main__':

    import argparse

    parser = argparse.ArgumentParser(description='This script can be used to search tv.nrk.no and download programs.')
    parser.add_argument('search_string', help='The string to search for on tv.nrk.no')
    args = parser.parse_args()

    series, programs = search(args.search_string)
    for p in programs:
        print(p)
    for i, s in enumerate(series):
        print(i, s)

