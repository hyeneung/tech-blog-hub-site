import pandas as pd
from datetime import datetime, timedelta

class GA4LogPreprocessor:
    def __init__(self, logs:pd.DataFrame):
        self.logs = logs
        self.users = None
        self.article_urls = None
        self.current_type = type(logs)
        self.preprocess()

    def preprocess(self):
        # 특정 이벤트만 남기기
        filtered_df = self.logs[self.logs['event_name'].isin(['post_click', 'summary_toggle_click', 'article_search'])]
        self.logs = filtered_df

        # 디버그 모드 제거
        self.logs = self.logs[
            ~self.logs['event_params'].apply(
                lambda params: any(param['key'] == 'debug_mode' and param['value'].get('int_value') == 1 for param in params)
        )]

        # engagement_time_msec < 1000인 항목 제거
        self.logs = self.logs[
            ~((self.logs['event_name'].isin(['post_click', 'summary_toggle_click'])) & 
              (self.logs['event_params'].apply(
                  lambda params: any(param['key'] == 'engagement_time_msec' and param['value'].get('int_value', 0) < 1000 for param in params)
                )
            )
        )]

        filtered_data = []
        user_event_clicks = {}
        user_search_counts = {}

        # DataFrame을 순회하며 하루 3회 제한 로직 및 article_search 제한 로직 적용
        for _, row in self.logs.iterrows():
            user_id = row['user_pseudo_id']
            event_name = row['event_name']
            event_params = row['event_params']
            
            # event_timestamp를 적절한 단위로 변환 (마이크로초 단위로 간주하여 변환)
            event_timestamp = row['event_timestamp']
            event_time = datetime.fromtimestamp(int(event_timestamp) / 1_000_000)  # 마이크로초 단위로 나누어 datetime으로 변환

            # 사이트 정보를 추출하기 위해 event_params에서 post_url 값 가져오기
            post_url = next((param['value'].get('string_value') for param in event_params if param['key'] == 'post_url'), None)
            
            # post_click과 summary_toggle_click 이벤트에 대한 하루 3회 제한 로직
            if event_name in ["post_click", "summary_toggle_click"] and post_url:
                # 사용자 ID와 이벤트명을 기준으로 클릭 기록 추적
                if user_id not in user_event_clicks:
                    user_event_clicks[user_id] = {}
                if post_url not in user_event_clicks[user_id]:
                    user_event_clicks[user_id][post_url] = {}
                if event_name not in user_event_clicks[user_id][post_url]:
                    user_event_clicks[user_id][post_url][event_name] = []
                
                # 하루 3회 이하 조건 확인
                click_times = user_event_clicks[user_id][post_url][event_name]
                click_times = [t for t in click_times if event_time - t < timedelta(days=1)]
                
                if len(click_times) < 3:
                    click_times.append(event_time)
                    user_event_clicks[user_id][post_url][event_name] = click_times
                    filtered_data.append(row)
            
            # article_search 이벤트에 대한 하루 10회 제한 로직
            elif event_name == "article_search":
                search_key = None
                # search_company나 search_hashtags 키를 가진 값을 찾아서 해당 값으로 제한 로직 적용
                for param in event_params:
                    if param['key'] in ['search_company', 'search_hashtags']:
                        search_key = param['value'].get('string_value')
                        break
                
                if search_key:
                    # 사용자 ID와 검색 키워드를 기준으로 검색 기록 추적
                    if user_id not in user_search_counts:
                        user_search_counts[user_id] = {}
                    if search_key not in user_search_counts[user_id]:
                        user_search_counts[user_id][search_key] = []
                    
                    # 하루 10회 이하 조건 확인
                    search_times = user_search_counts[user_id][search_key]
                    search_times = [t for t in search_times if event_time - t < timedelta(days=1)]
                    
                    if len(search_times) < 10:
                        search_times.append(event_time)
                        user_search_counts[user_id][search_key] = search_times
                        filtered_data.append(row)
                else:
                    # search_company나 search_hashtags가 없는 경우, 그대로 유지
                    filtered_data.append(row)
            
            else:
                # 다른 이벤트는 그대로 유지
                filtered_data.append(row)

        # 최종적으로 필터링된 데이터를 새로운 DataFrame으로 변환
        self.logs = pd.DataFrame(filtered_data)




