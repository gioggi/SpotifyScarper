# -*- coding: utf-8 -*-
import csv


class Writer(object):
    artist_header = ['Id', 'Name', 'Popularity', 'Followers', 'Generes']
    track_header = ['Id',
                    'artist_id',
                    'album_id',
                    'album_release_date',
                    'name',
                    'disc_number',
                    'duration_ms',
                    'explicit',
                    'popularity',
                    'track_number',
                    'danceability',
                    'energy',
                    'key',
                    'loudness',
                    'mode',
                    'speechiness',
                    'acousticness',
                    'instrumentalness',
                    'liveness',
                    'valence',
                    'tempo',
                    'time_signature',
                    ]
    delimiter = ','
    quotechar = '"'
    quoting = csv.QUOTE_MINIMAL

    def __init__(self, file_name='test.csv', writer_type='artist'):
        self.writer_type = writer_type
        self.file_name = file_name
        self.write_header()

    def write_header(self) -> object:
        """

        :rtype: object
        """
        header = self.artist_header if (self.writer_type == 'artist') else self.track_header
        with open(self.file_name, mode='w') as employee_file:
            employee_writer = csv.writer(employee_file,
                                         delimiter=self.delimiter,
                                         quotechar=self.quotechar,
                                         quoting=self.quoting)
            employee_writer.writerow(header)

    def write_row(self, row):
        with open(self.file_name, mode='a') as employee_file:
            employee_writer = csv.writer(employee_file,
                                         delimiter=self.delimiter,
                                         quotechar=self.quotechar,
                                         quoting=self.quoting)
            employee_writer.writerow(row)

