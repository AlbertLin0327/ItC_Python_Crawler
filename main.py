from crawler import Crawler
from args import get_args
import csv

if __name__ == '__main__':
	args = get_args()
	crawler = Crawler()
	contents = crawler.crawl(args.start_date, args.end_date)
	# TODO: write content to file according to spec
	with open(args.output, 'w') as f:
		for date, title, content in contents:
			title = title.replace(' ', '')
			content = content.replace(' ' , '')
			outstr = f'{str(date)}\n\t{title}\n\t{content}\n'
			f.write(outstr)