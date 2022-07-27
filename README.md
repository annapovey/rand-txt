python3 -m venv wiki_env
source wiki_env/bin/activate
which pip
pip install apache_beam mwparserfromhell
pip3 install datasets

There is 6,458,670 wikipedia march 2022 articles.
Selected 36K random lines from 6M articles
wikipedia_20220301_en_train
1_sentence_per_line.txt

Wanted 2 sentences per line
paste -d " "  - - < wikipedia_20220301_en_train.txt > 2_sentences_per_line.txt
