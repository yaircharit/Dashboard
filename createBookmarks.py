import argparse
import yaml

choosen_encoding = "UTF-8"
bookmarks_placeholder = '// %INJECT BOOKMARKS HERE%'
newsfeed_placeholder = '// %INJECT NEWSFEED HERE%'

parser = argparse.ArgumentParser(
    description="Creates a static bookmarks site from a given y(a)ml file and an HTML template."
)
parser.add_argument(
    "-bookmarks_file",
    default="bookmarks.yml",
    help="yaml file containing bookmarks and urls",
)
parser.add_argument(
    "-news_file",
    default="news.yml",
    help="yaml file containing bookmarks and urls",
)
parser.add_argument(
    "-template_file",
    default="temp.html",
    help='html template containing the string "var injected="%INJECTED%"',
)
parser.add_argument(
    "-out_file", 
    default="bookmarks.html"
)

args = parser.parse_args([])

outfile = args.out_file

with open(args.bookmarks_file, "r", encoding=choosen_encoding) as f:
    print(f"Reading {args.bookmarks_file}")
    bookmarks = yaml.full_load(f)
    
with open(args.news_file, "r", encoding=choosen_encoding) as f:
    print(f"Reading {args.news_file}")
    news = yaml.full_load(f)
    print(news)

with open(args.template_file, "r", encoding=choosen_encoding) as f:
    print(f"Reading {args.template_file}")
    template = f.readlines()

for line in range(0, len(template)):
    if template[line].find(bookmarks_placeholder) >= 0:
        print("Inserting bookmarks...")
        template[line] =  f'\t\t\tdocument.staticMarks = {str(bookmarks).strip()}\n'
        
    if template[line].find(newsfeed_placeholder) >= 0:
        print("Inserting news...")
        if news == None:
            template[line] =  f'\t\t\tdocument.newsFeed = {{}}\n'     
        else:
            template[line] =  f'\t\t\tdocument.newsFeed = {str(news).strip()}\n'     
    

with open(outfile, "w", encoding=choosen_encoding, errors="ignore") as f:
    print("Creating HTML webpage")
    for line in template:
        f.write(line)

print(f"A new {outfile} file was created in the root directory")
