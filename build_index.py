import glob
from langchain.text_splitter import RecursiveCharacterTextSplitter
import utils
from dotenv import load_dotenv
import openai
import os
import json

load_dotenv()

openai.api_key = os.environ["OPENAI_API_KEY"]


CHUNK_SIZE = 12000

def fetch_embedding(chunk):
    return openai.Embedding.create(input=chunk, engine="text-embedding-ada-002")


def write_index(index):
    json_string = json.dumps(index)
    with open(f"index.json", "w") as f:
        f.write(json_string)


if __name__ == "__main__":
    files = list()
    names = list()

    for file in glob.glob("input/*.txt"):
        names.append({"name": file.replace("input/", "").replace(".md", "")})
        with open(file, "r") as f:
            files.append(f.read())

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=0)

    chunks = text_splitter.create_documents(files, metadatas=names)

    utils.log_chunks(chunks)

    index = list()
    total_tokens = 0

    for chunk in chunks:
        response = fetch_embedding(chunk.page_content)
        vector = response["data"][0]["embedding"]

        total_tokens += response["usage"]["total_tokens"]

        index.append(
            {
                "content": chunk.page_content,
                "name": chunk.metadata["name"],
                "vector": vector,
            }
        )

    utils.log(
        {"tokens_used": total_tokens, "index": index},
        file_type="json",
        suffix="build-index",
    )

    write_index(index)
