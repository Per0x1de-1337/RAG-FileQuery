import logging
import sys
import os
import click
import pathway as pw
import yaml
from dotenv import load_dotenv

from pathway.udfs import DiskCache, ExponentialBackoffRetryStrategy
from pathway.xpacks.llm import embedders, llms, parsers, splitters
from pathway.xpacks.llm.question_answering import BaseRAGQuestionAnswerer
from pathway.xpacks.llm.vector_store import VectorStoreServer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(name)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

load_dotenv()

license_key = os.getenv("PATHWAY_LICENSE_KEY")
if license_key:
    pw.set_license_key(license_key)
    logging.info("Pathway license key set from environment.")
else:
    logging.warning("PATHWAY_LICENSE_KEY not found. Running in Community mode.")

def data_sources(source_configs) -> list[pw.Table]:
    sources = []
    for source_config in source_configs:
        if source_config["kind"] == "local":
            source = pw.io.fs.read(
                **source_config["config"],
                format="binary",
                with_metadata=True,
            )
            sources.append(source)
    return sources

@click.command()
@click.option("--config_file", default="config.yaml", help="Config file to be used.")
def run(config_file: str):
    with open(config_file) as config_f:
        configuration = yaml.safe_load(config_f)

    LLM_MODEL = configuration["llm_config"]["model"]
    embedding_model = "avsolatorio/GIST-small-Embedding-v0"

    embedder = embedders.SentenceTransformerEmbedder(
        embedding_model,
        call_kwargs={"show_progress_bar": False}
    )

    chat = llms.LiteLLMChat(
        model=LLM_MODEL,
        retry_strategy=ExponentialBackoffRetryStrategy(max_retries=6),
        cache_strategy=DiskCache(),
    )

    host_config = configuration["host_config"]
    host, port = host_config["host"], host_config["port"]

    logging.info(f"Starting RAG API server on {host}:{port} with model {LLM_MODEL}")

    doc_store = VectorStoreServer(
        *data_sources(configuration["sources"]),
        embedder=embedder,
        splitter=splitters.TokenCountSplitter(max_tokens=400),
        parser=parsers.UnstructuredParser(),
    )

    rag_app = BaseRAGQuestionAnswerer(llm=chat, indexer=doc_store)
    rag_app.build_server(host=host, port=port)
    rag_app.run_server(with_cache=True, terminate_on_error=False)

if __name__ == "__main__":
    run()