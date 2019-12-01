import os
import csv
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction


def readWriteCSV():
	lineCount = 0
	data = []
	directory = os.path.dirname(os.path.abspath(__file__))
	filename = os.path.join(directory, 'inst_summary_download_0.csv')
	with open(filename) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			rowData = []
			index = 0
			add = True
			if lineCount > 6:
				for col in row:
					if ',' in col:
						col = col.replace(',',';')
					if '"' in col:
						col = col.replace('"','')
					if index == 9:
						if '/' in col:
							add = False
					if index == 13 and col == '':
						rowData.append('N')
					else:
						rowData.append(col)
					if ((col == '' or col == ' ') and index != 13) or (col == '#N/A') or (col == 'NA') or (col == '(Blank)') or (col == 'Anupama'):
						add = False
						break
					index += 1
				if add == True:
					data.append(rowData)
			lineCount += 1
	filename = os.path.join(directory, 'clean_fcq.csv')
	with open(filename, mode='w', newline = '') as clean_fcq:
		writer = csv.writer(clean_fcq, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for i in data:
			writer.writerow(i)



class Command(BaseCommand):
    print(
        "Cleaning fcq data from original csv file..."
    )
    def handle(self, *args, **kwargs):
        # Return values are for tests. test kwarg flag will be set if used with test
        in_test = kwargs.pop("test", False)
        if in_test:
            if readWriteCSV():
                return True
            else:
                return False
        else:
            readWriteCSV()