SHELL := /bin/bash

#####################
# Variables section #
#####################

# Base url used for crawling
BASE_URL := "https://www.goodreads.com/list/show/1.Best_Books_Ever?page="
# Number of pages that should be crawled
N_BOOK_PAGES := 100
# Number of quotes pages that should be crawler per book
N_QUOTE_PAGES := 50

#################
# Rules section #
#################
all: clean process analyze

# Cleans everything, including the original data
# Since crawling takes a considerable amount of time a separate rule was created
clean_all:
	rm -rf data processed analysis

clean:
	rm -rf processed analysis

.PHONY: collect process analyze adhoc
collect:
	# This target is usually associated with data collection
	# This can involved scraping websites, downloading files from servers,
	# or other similar operations.
	# As best practice, ensure that all output data goes to a known location (e.g., here, data/)
	
	mkdir -p data
	cd crawler; \
		python3 -m venv venv; \
		source venv/bin/activate; \
		pip install -r requirements.txt; \
		scrapy crawl goodreads \
			-a base_url=$(BASE_URL) -a books_page_count=$(N_BOOK_PAGES) -a quotes_page_count=$(N_QUOTE_PAGES) \
			-o ../data/goodreads.json; \
		deactivate

process: data/goodreads.json data-processing/convert_isbn.py data-processing/format_pages.py data-processing/format_quote_likes.py data-processing/remove_quoteless_books.py data-processing/strip_quotes.py data-processing/fill_missing_fields.py
	# This target is reserved for data processing, which typically includes
	# cleaning and refinement.
	# As best practice, have multiple scripts to perform different (sub)steps
	# You may even opt for several targets for bigger granularity
	# (e.g., a process_cleaning and a process_refinement target)
	# Moreover, ensure that data also goes to a known location for easier analysis
	
	mkdir -p processed
	
	python3 -m venv data-processing/venv

	source data-processing/venv/bin/activate; \
		pip install -r data-processing/requirements.txt --quiet; \
		cat data/goodreads.json | \
		python3 data-processing/convert_isbn.py | \
		python3 data-processing/format_pages.py | \
		python3 data-processing/format_quote_likes.py | \
		python3 data-processing/remove_quoteless_books.py | \
		python3 data-processing/strip_quotes.py | \
		python3 data-processing/fill_missing_fields.py | \
		python3 data-processing/identify_language.py \
		> processed/goodreads.json

analyze:
	# This target is recommended to isolate all data analysis scripts.
	# Once again, it is recommended to separate different types of analysis between scripts,
	# which may span several languages. Diversity is key here so data can be better understood.

	mkdir data-characterization/output -p

	python3 -m venv data-characterization/venv

	source data-characterization/venv/bin/activate; \
		pip install -r data-characterization/requirements.txt --quiet; \
		python3 data-characterization/main.py -i processed/goodreads.json -o data-characterization/output; \ 
		python3 data-characterization/nlp.py -i processed/goodreads.json -o data-characterization/output

adhoc:
	# This target is not part of the overall automation, but it can be useful to have something similar
	# to automate some less frequent operation that you might want to run only when strictly necessary
	# (e.g., organize all produced data/analysis and run a notebook for an easier visual verification of obtained results)
	
	echo "Not implemented"
