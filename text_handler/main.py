import grpc
from concurrent import futures
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
import os
import concurrent.futures

from generated import crawler_text_handler_pb2_grpc, crawler_text_handler_pb2
from model.hashtag import HashtaggingModule
from model.summarize import SummarizeModule
from utils.preprocess import get_preprocessed_text

class CrawlerTextHandlerServicer(crawler_text_handler_pb2_grpc.CrawlerTextHandlerServicer):
    def __init__(self):
        self.summarize_module = SummarizeModule()
        self.hashtagging_module = HashtaggingModule()
        self.executor = ThreadPoolExecutor(max_workers=10)

    def StreamUrlSummaries(self, request_iterator, context):
        for request in request_iterator:
            try:
                url = request.url
                print(f"Processing URL: {url}")
                preprocessed_text = get_preprocessed_text(url)
                summarized_text, hashtags = asyncio.run(self.process_text(preprocessed_text))
                
                yield crawler_text_handler_pb2.SummarizedDataResponse(
                    content=preprocessed_text,
                    summarized_text=summarized_text,
                    hashtags=hashtags
                )
            except grpc.RpcError as e:
                print(f"gRPC Error: {e.code()}, {e.details()}")
                context.abort(e.code(), f"gRPC Error: {e.details()}")
            except Exception as e:
                print(f"Error in StreamUrlSummaries: {e}")
                context.abort(grpc.StatusCode.INTERNAL, f"Internal Error: {str(e)}")

    async def process_text(self, preprocessed_text):
        summarize_task = asyncio.create_task(self.summarize_url(preprocessed_text))
        hashtag_task = asyncio.create_task(self.generate_hashtags(preprocessed_text))

        summarized_text = await summarize_task
        hashtags = await hashtag_task

        return summarized_text, hashtags

    async def summarize_url(self, url):
        loop = asyncio.get_running_loop()
        with concurrent.futures.ThreadPoolExecutor() as pool:
            return await loop.run_in_executor(pool, self.summarize_module.summarize, url)

    async def generate_hashtags(self, url):
        loop = asyncio.get_running_loop()
        with concurrent.futures.ThreadPoolExecutor() as pool:
            return await loop.run_in_executor(pool, self.hashtagging_module.generate_hashtags, url)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=20))
    crawler_text_handler_pb2_grpc.add_CrawlerTextHandlerServicer_to_server(CrawlerTextHandlerServicer(), server)

    # server_address = os.getenv('SERVER_ADDRESS')
    server_address = "[::]:50051"
    server.add_insecure_port(server_address)
    server.start()
    
    print("Server started on port 50051")
    try:
        server.wait_for_termination()
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()