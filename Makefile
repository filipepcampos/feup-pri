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

# Flag identifying if the language of each quote should be identifed and analysed
# This is a computationally expensive step, therefore is presented as an option
# 1 = Active, 0 = Inactive
IDENTIFY_QUOTE_LANGUAGE := 1

# Crawler output folder
DATA_OUTPUT_FOLDER := data

# Output folder for process stage
PROCESS_OUTPUT_FOLDER := solr/data

# Output folder for analyze stage
ANALYSIS_OUTPUT_FOLDER := data/analysis

#################
# Rules section #
#################
all: clean process analyze

# Cleans everything, including the original data
# Since crawling takes a considerable amount of time a separate rule was created
clean_all:
	rm -rf data $(PROCESS_OUTPUT_FOLDER) $(ANALYSIS_OUTPUT_FOLDER)

clean:
	rm -rf $(PROCESS_OUTPUT_FOLDER) $(ANALYSIS_OUTPUT_FOLDER)

.PHONY: collect process analyze adhoc
collect $(DATA_OUTPUT_FOLDER)/goodreads.json:
	# This target will execute our webcrawler and export the resulting data to $(DATA_OUTPUT_FOLDER)/goodreads.json
	# An python virtual environment is used to keep the project pip dependencies contained
	
	mkdir -p $(DATA_OUTPUT_FOLDER)
	cd crawler; \
		python3 -m venv venv; \
		source venv/bin/activate; \
		pip install -r requirements.txt; \
		scrapy crawl goodreads \
			-a base_url=$(BASE_URL) -a books_page_count=$(N_BOOK_PAGES) -a quotes_page_count=$(N_QUOTE_PAGES) \
			-o ../$(DATA_OUTPUT_FOLDER)/goodreads.json; \
		deactivate

process: $(DATA_OUTPUT_FOLDER)/goodreads.json data-processing/convert_isbn.py data-processing/format_pages.py data-processing/format_quote_likes.py data-processing/remove_quoteless_books.py data-processing/strip_quotes.py data-processing/fill_missing_fields.py data-processing/count_authors.py data-processing/count_quotes.py data-processing/get_first_genres.py
	# Apply data processing steps using some small python scripts
	
	mkdir -p $(PROCESS_OUTPUT_FOLDER)

	cat $(DATA_OUTPUT_FOLDER)/goodreads.json | \
		python3 data-processing/convert_isbn.py | \
		python3 data-processing/format_pages.py | \
		python3 data-processing/format_quote_likes.py | \
		python3 data-processing/remove_quoteless_books.py | \
		python3 data-processing/strip_quotes.py | \
		python3 data-processing/fill_missing_fields.py | \
		python3 data-processing/count_authors.py | \
		python3 data-processing/count_quotes.py | \
		python3 data-processing/get_first_genres.py \
		> $(PROCESS_OUTPUT_FOLDER)/goodreads.json

	# The language identification step is time consuming, due to the large amount of quotes that need to be considered
	# This step is optional for now to save time
	
ifeq ($(IDENTIFY_QUOTE_LANGUAGE), 1)
	mv $(PROCESS_OUTPUT_FOLDER)/goodreads.json $(PROCESS_OUTPUT_FOLDER)/goodreads_nolanguage.json
	python3 -m venv data-processing/venv
	source data-processing/venv/bin/activate; \
		pip install -r data-processing/requirements.txt --quiet; \
		cat $(PROCESS_OUTPUT_FOLDER)/goodreads_nolanguage.json | \
		python3 data-processing/identify_language.py \
		> $(PROCESS_OUTPUT_FOLDER)/goodreads.json
	rm $(PROCESS_OUTPUT_FOLDER)/goodreads_nolanguage.json
endif

analyze:
	# Analyse the data that was obtained from the process step

	mkdir -p $(ANALYSIS_OUTPUT_FOLDER)

	python3 -m venv data-characterization/venv

ifeq ($(IDENTIFY_QUOTE_LANGUAGE), 1)
	source data-characterization/venv/bin/activate; \
		pip install -r data-characterization/requirements.txt --quiet; \
		python3 data-characterization/analyze.py -i $(PROCESS_OUTPUT_FOLDER)/goodreads.json -o $(ANALYSIS_OUTPUT_FOLDER);  \
		python3 data-characterization/language.py -i $(PROCESS_OUTPUT_FOLDER)/goodreads.json -o $(ANALYSIS_OUTPUT_FOLDER)
else
	source data-characterization/venv/bin/activate; \
		pip install -r data-characterization/requirements.txt --quiet; \
		python3 data-characterization/analyze.py -i $(PROCESS_OUTPUT_FOLDER)/goodreads.json -o $(ANALYSIS_OUTPUT_FOLDER)
endif

adhoc:
	# This target is not part of the overall automation, but it can be useful to have something similar
	# to automate some less frequent operation that you might want to run only when strictly necessary
	# (e.g., organize all produced data/analysis and run a notebook for an easier visual verification of obtained results)
	
	echo "Not implemented"
