import argparse
parser = argparse.ArgumentParser(description="Generate code")
parser.add_argument("--language", choices=[
                    "objc"], help="The language to generate", required=True)
parser.add_argument("-o", "--output", help="Output directory", default=".")
parser.add_argument("--url", help="URL for the schema", required=True)


def codegen(args):
	
    pass
