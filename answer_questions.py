from dotenv import load_dotenv
import openai
import os
import json
import utils
import numpy
import tiktoken

load_dotenv()

openai.api_key = os.environ["OPENAI_API_KEY"]


def similarity(v1, v2):
    return numpy.dot(v1, v2)


def num_tokens_from_messages(messages, model="gpt-3.5-turbo-0301"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    if model == "gpt-3.5-turbo-0301":  # note: future models may deviate from this
        num_tokens = 0
        for message in messages:
            num_tokens += (
                4  # every message follows <im_start>{role/name}\n{content}<im_end>\n
            )
            for key, value in message.items():
                num_tokens += len(encoding.encode(value))
                if key == "name":  # if there's a name, the role is omitted
                    num_tokens += -1  # role is always required and always 1 token
        num_tokens += 2  # every reply is primed with <im_start>assistant
        return num_tokens
    else:
        raise NotImplementedError(
            f"""num_tokens_from_messages() is not presently implemented for model {model}.
See https://github.com/openai/openai-python/blob/main/chatml.md for information on how messages are converted to tokens."""
        )


if __name__ == "__main__":
    with open("index.json", "r") as index:
        index_data = json.load(index)

    while True:
        query = input("Enter your question here: ")

        response = openai.Embedding.create(input=query, engine="text-embedding-ada-002")
        query_vector = response["data"][0]["embedding"]

        query_embedding_usage = response["usage"]["total_tokens"]
        utils.log(
            f"USAGE: {query_embedding_usage}\n\n"
            "QUERY:\n\n"
            f"{query}\n\n"
            "VECTOR:\n\n"
            f"{query_vector}",
            suffix="query-embedding",
        )

        scores = list() 
        for chunk in index_data:
            score = similarity(query_vector, chunk["vector"])
            scores.append(
                {"content": chunk["content"], "score": score, "name": chunk["name"]}
            )

        sorted_scores = sorted(scores, key=lambda d: d["score"], reverse=True)

        most_similar = sorted_scores[0]
        excerpt = most_similar["content"]

        messages = [
            {
                "role": "system",
                "content": (
                    "You are a swashbuckling pirate first and foremost, and a programmer who specializes in web development. You are the digital soul of Jimmy Cleveland, and you have a Youtube channel for which you are currently answering questions. All your answers should be in pirate speak, and try to format your answers in markdown. Give a succinct answer to the question using only the information in excerpt below, as if you have no prior knowledge about the question. Translate any text you use from the excerpt into pirate speak. If there is no information in the excerpt that is relevant to the question, apologize and say there isn't enough information in the blog to answer, and do it all in pirate speak. Never ask the user questions."
                    "\n\nEXCERPT:\n\n"
                    f"{excerpt}"
                ),
            },
            {"role": "user", "content": query},
        ]

        print(num_tokens_from_messages(messages))

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", temperature=0.7, max_tokens=500, messages=messages
        )

        utils.log(response, file_type="json", suffix="chat-completion-response")

        system_message = response["choices"][0]["message"]
        system_message["source"] = "\n\nSource: " + most_similar["name"]
        messages.append(system_message)

        chat_transcript = ""
        for message in messages:
            if message["role"] != "system":
                chat_transcript += (
                    message["role"]
                    + ": "
                    + message["content"]
                    + "\n\n"
                    + (message["source"] + "\n\n")
                    if "source" in message
                    else ""
                )

        print(chat_transcript)
