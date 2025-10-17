import json
import os
import logging
from elasticsearch import Elasticsearch

# ----------------------------------------------------
#                      설정값
# ----------------------------------------------------
ES_HOST = "localhost"
ES_PORT = 9200
ES_USER = "elastic" # curl에서 성공한 'elastic' 사용자로 설정
ES_PASSWORD = "1234"
CA_CERTS_PATH = os.path.expanduser("~/dev/certs/ca.crt")
TARGET_INDEX = "article_infos"
OUTPUT_FILENAME = f"backup_{TARGET_INDEX}.jsonl"
SCROLL_SIZE = 1000
# ----------------------------------------------------

def backup_index_to_jsonl(es_client, index_name, filename):
    """Scroll API를 사용해 인덱스의 모든 문서를 .jsonl 파일로 저장합니다."""
    print(f"\n[INFO] 인덱스 '{index_name}' 백업 시작...")
    scroll_id = None
    try:
        resp = es_client.search(
            index=index_name,
            scroll="2m",
            size=SCROLL_SIZE,
            body={"query": {"match_all": {}}}
        )
        scroll_id = resp.get('_scroll_id')
        hits = resp['hits']['hits']
        
        if scroll_id is None or not hits:
            print("[WARNING] 데이터가 없거나 스크롤을 시작할 수 없습니다.")
            return

        total_docs = resp['hits']['total']['value']
        processed_docs = 0

        with open(filename, 'w', encoding='utf-8') as f:
            for doc in hits:
                f.write(json.dumps(doc['_source'], ensure_ascii=False) + '\n')
            processed_docs += len(hits)
            print(f"[INFO] 진행: {processed_docs} / {total_docs} 문서 처리됨")

            while scroll_id and hits:
                resp = es_client.scroll(scroll_id=scroll_id, scroll="2m")
                scroll_id = resp.get('_scroll_id')
                hits = resp['hits']['hits']
                if not hits: break
                for doc in hits:
                    f.write(json.dumps(doc['_source'], ensure_ascii=False) + '\n')
                processed_docs += len(hits)
                print(f"[INFO] 진행: {processed_docs} / {total_docs} 문서 처리됨")
        
        print(f"\n[SUCCESS] 백업 완료! 총 {processed_docs}개의 문서가 '{filename}' 파일에 저장되었습니다.")

    except Exception as e:
        logging.error("[ERROR] 백업 중 오류 발생", exc_info=True)
    finally:
        if scroll_id:
            try:
                es_client.clear_scroll(scroll_id=scroll_id)
                print("[INFO] 스크롤 ID를 성공적으로 정리했습니다.")
            except Exception as ce:
                logging.error("[ERROR] 스크롤 ID 정리 중 오류 발생", exc_info=True)


if __name__ == "__main__":
    try:
        print("[INFO] Elasticsearch 클라이언트 연결 시도...")
        
        # 구버전(7.x) 라이브러리에 맞는 방식으로 수정
        es = Elasticsearch(
            [ES_HOST],
            scheme="https",
            port=ES_PORT,
            http_auth=(ES_USER, ES_PASSWORD),
            ca_certs=CA_CERTS_PATH
        )
        
        info = es.info()
        print(f"\n[SUCCESS] Elasticsearch 정보 확인 성공. 버전: {info['version']['number']}")
        
        backup_index_to_jsonl(es, TARGET_INDEX, OUTPUT_FILENAME)

    except FileNotFoundError:
        print(f"[ERROR] CA 인증서 파일을 찾을 수 없습니다. 경로를 확인하세요: {CA_CERTS_PATH}")
    except ConnectionError as e:
        print(f"[ERROR] 연결 오류: {e}")
    except Exception as e:
        logging.error("[ERROR] 알 수 없는 오류 발생", exc_info=True)

