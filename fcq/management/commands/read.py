import os
import csv


def readWriteCSV():
	count = 0
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
				rowData.append(count)
				if add == True:
					count += 1
					data.append(rowData)
			lineCount += 1
	filename = os.path.join(directory, 'clean_fcq.csv')
	with open(filename, mode='w', newline = '') as clean_fcq:
		writer = csv.writer(clean_fcq, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		for i in data:
			writer.writerow(i)



def main():
	readWriteCSV()



main()