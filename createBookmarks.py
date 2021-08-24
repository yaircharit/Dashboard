import sys, argparse
import yaml

choosen_encoding = "UTF-8"
bookmarks_placeholder = '// %INJECT BOOKMARKS HERE%'
newsfeed_placeholder = '// %INJECT NEWSFEED HERE%'
newsfeed_animation_placeholder = '/* %INJECT NEWSFEED ANIMATION HERE% */'
newsfeed_duration_placeholder = '/* %INJECT NEWSFEED DURATION HERE% */'
newsfeed_animation_duration = 7 #in seconds
newsfeed_font_size = 70 #in pixels

parser = argparse.ArgumentParser(
    description="Creates a static bookmarks site from a given y(a)ml file and an HTML template."
)
parser.add_argument(
    "-yaml_file",
    default="bookmarks.yml",
    help="yaml file containing bookmarks and urls",
)
parser.add_argument(
    "-template_file",
    default="temp.html",
    help='html template containing the string "var injected="%INJECTED%"',
)
parser.add_argument("-out_file", default="bookmarks.html")

args = parser.parse_args([])
# print(args.template_file, args.yaml_file, args.out_file)

# outfile = sys.argv[4] if len(sys.argv) == 5 else "bookmarks.html"
outfile = args.out_file
news = []
with open(args.yaml_file, "r", encoding=choosen_encoding) as f:
    print(f"Reading yml/yaml file {args.yaml_file}")
    yml = yaml.full_load(f)
    bookmarks = yml['Collections'] if 'Collections' in yml else yml
    if 'News Feed' in yml:
        news = yml['News Feed'] 

with open(args.template_file, "r", encoding=choosen_encoding) as f:
    print(f"Reading Template file {args.template_file}")
    template = f.readlines()

for line in range(0, len(template)):
    if template[line].find(bookmarks_placeholder) >= 0:
        print("Inserting bookmarks...")
        template[line] =  f'\t\t\tdocument.staticMarks = {str(bookmarks).strip()}\n'
        
    if template[line].find(newsfeed_placeholder) >= 0 and len(news) > 0:
        print("Inserting news...")
        template[line] =  f'\t\t\tdocument.newsFeed = {str(news).strip()}\n'
        
    if template[line].find(newsfeed_animation_placeholder) >= 0 and len(news) > 0:
        print("Inserting news animation...")
        max_prec = 100
        base_prec = max_prec / len(news)
        res = ''
        for i in range(len(news)):
            res += f'\t\t\t{base_prec*i}% {{bottom: {int(newsfeed_font_size*i)}px}}\n'
        res += f'\t\t\t100% {{bottom: 0px}}\n'
        template[line] = res
        
    if template[line].find(newsfeed_duration_placeholder) >= 0 and len(news) > 0:
        template[line] = f'\t\t\tanimation-duration: {len(news)*newsfeed_animation_duration}s;\n'
        
    

with open(outfile, "w", encoding=choosen_encoding, errors="ignore") as f:
    print("Creating HTML webpage")
    for line in template:
        f.write(line)


print(f"A new {outfile} file was created in the root directory")
