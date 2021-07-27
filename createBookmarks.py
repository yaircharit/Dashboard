import sys, argparse
import yaml

choosen_encoding = "UTF-8"
placeholder = '// %INJECT HERE%'

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
with open(args.yaml_file, "r", encoding=choosen_encoding) as f:
    print(f"Reading yml/yaml file {args.yaml_file}")
    bookmarks = yaml.full_load(f)

with open(args.template_file, "r", encoding=choosen_encoding) as f:
    print(f"Reading Template file {args.template_file}")
    template = f.readlines()

for line in range(0, len(template)):
    if template[line].find(placeholder) >= 0:
        print("Inserting bookmarks...")
        template[line] =  f'\t\t\tdocument.staticMarks = {template[line].replace(placeholder, str(bookmarks)).strip()}\n'
        template[line] = template[line]
        break

with open(outfile, "w", encoding=choosen_encoding, errors="ignore") as f:
    print("Creating HTML webpage")
    for line in template:
        f.write(line)


print(f"A new {outfile} file was created in the root directory")
