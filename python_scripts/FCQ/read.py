import csv


def readWriteCSV():
	lineCount = 0
	data = []
	with open('inst_summary_download_0.csv') as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			rowData = []
			index = 0
			add = True
			if lineCount > 6:
				for col in row:
					if index == 13 and col == '':
						rowData.append('N')
					else:
						rowData.append(col)
					if col == '' and index != 13:
						add = False
						break
					index += 1
				if add == True:
					data.append(rowData)
			lineCount += 1
	with open('clean_fcq.csv', mode='w', newline = '') as clean_fcq:
		writer = csv.writer(clean_fcq, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

		for i in data:
			writer.writerow(i)


def main():
	readWriteCSV()


main()