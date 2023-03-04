import glob
from langchain.text_splitter import MarkdownTextSplitter
import utils

files = list()

for file in glob.glob("input/*.md"):
    with open(file, "r") as f:
        files.append(f.read())

markdown_splitter = MarkdownTextSplitter(chunk_size=12000, chunk_overlap=0)

docs = markdown_splitter.create_documents(files)

utils.log_chunks(docs)
