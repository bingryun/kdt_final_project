from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.hooks.S3_hook import S3Hook
from airflow.hooks.postgres_hook import PostgresHook
from io import StringIO
from psycopg2.extras import execute_values
from common.alert import SlackAlert
import requests
import csv
import pendulum
import logging

slackbot = SlackAlert('#airflow_log')
kst = pendulum.timezone("Asia/Seoul")

default_args = {
    'owner': 'chansu',
    'depends_on_past': True,
    'start_date': pendulum.datetime(2024, 8, 2, tz=kst),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': pendulum.duration(minutes=5),
    'on_failure_callback': slackbot.failure_alert,
    'on_success_callback': slackbot.success_alert,
}

def fetch_api_data(api_url: str, params: dict) -> str:
    response = requests.get(api_url, params=params)
    response_200 = 200
    if response.status_code != response_200:
        logging.error(f"ERROR : 응답 코드 오류 {response.status_code}")
        logging.error(f"ERROR : 메세지 : {response.text}")
        raise ValueError(f"ERROR : 응답코드오류 {response.status_code}, 메세지 : {response.text}")
    logging.info(f"API 상태코드: {response.status_code}")
    return response.text

def parse_response_data(response_text: str) -> list:
    if "#START7777" not in response_text or "#7777END" not in response_text:
        logging.error("ERROR : 데이터 수신 실패", response_text)
        raise ValueError(f"ERROR : 데이터 수신 실패 : {response_text}")
    
    lines = response_text.splitlines()
    data = []
    start_index = 0
    
    for i, line in enumerate(lines):
        if line.startswith('# REG_ID'):
            start_index = i + 1
            break

    for line in lines[start_index:]:
        if line.strip() and not line.startswith('#7777END'):
            columns = line.split(',')
            columns = [col.strip() for col in columns if col.strip()]
            data.append(parse_columns(columns))
    
    return data

def parse_columns(columns: list) -> tuple:
    column_len = 12
    if len(columns) < column_len:
        columns += [None] * (column_len - len(columns))
    try:
        reg_id = columns[0]
        tm_fc = pendulum.parse(columns[1], strict=False) if columns[1] else None
        tm_ef = pendulum.parse(columns[2], strict=False) if columns[2] else None
        mod = columns[3]
        stn = columns[4]
        c = columns[5]
        min_val = columns[6]
        max_val = columns[7]
        min_l = columns[8]
        min_h = columns[9]
        max_l = columns[10]
        max_h = columns[11]
        return (reg_id, tm_fc, tm_ef, mod, stn, c, min_val, max_val, min_l, min_h, max_l, max_h)
    except ValueError as e:
        logging.warning(f"행을 파싱하는 중 오류 발생: {e}")
        return None

def save_to_s3(data: list, s3_key: str) -> None:
    csv_buffer = StringIO()
    csv_writer = csv.writer(csv_buffer)
    csv_writer.writerow(['REG_ID','TM_FC','TM_EF','MODE_KEY','STN_ID','CNT_CD','MIN_TA','MAX_TA','MIN_L_TA','MIN_H_TA','MAX_L_TA','MAX_H_TA'])
    csv_writer.writerows(data)
    
    s3_hook = S3Hook(aws_conn_id='AWS_S3')
    bucket_name = 'team-okky-1-bucket'
    
    try:
        s3_hook.load_string(
            csv_buffer.getvalue(),
            key=s3_key,
            bucket_name=bucket_name,
            replace=True
        )
        logging.info(f"데이터를 S3에 저장 성공: {s3_key}")
    except Exception as e:
        logging.error(f"S3 업로드 실패: {e}")
        raise ValueError(f"S3 업로드 실패: {e}")

def fct_afs_wc_to_s3(data_interval_end: pendulum.datetime, **kwargs) -> None:
    api_url = "https://apihub.kma.go.kr/api/typ01/url/fct_afs_wc.php"
    api_key = "HGbLr74hS2qmy6--ITtqog"
    
    data_interval_end_kst = data_interval_end.in_timezone(kst)
    one_hour_before = data_interval_end_kst - pendulum.duration(hours=1)
    tmfc1 = one_hour_before.strftime('%Y%m%d%H')
    tmfc2 = one_hour_before.strftime('%Y%m%d%H')

    params = {
        'stn': '',
        'reg': '',
        'tmfc': '',
        'tmfc1': tmfc1,
        'tmfc2': tmfc2,
        'tmef1': '',
        'tmef2': '',
        'mode': 0,
        'disp': 1,
        'help': 0,
        'authKey': api_key
    }

    response_text = fetch_api_data(api_url, params)
    data = parse_response_data(response_text)

    if data:
        tm_fc = pendulum.parse(data[0][1], strict=False) if data[0][1] else None
        year = tm_fc.strftime('%Y')
        month = tm_fc.strftime('%m')
        day = tm_fc.strftime('%d')
        hour = tm_fc.strftime('%H')
        formatted_date = tm_fc.strftime('%Y_%m_%d_%H')
        s3_key = f'fct_afs_wc/{year}/{month}/{day}/{hour}/{formatted_date}_fct_afs_wc.csv'

        save_to_s3(data, s3_key)
        kwargs['task_instance'].xcom_push(key='s3_key', value=s3_key)
    else:
        logging.error("ERROR : 유효한 데이터가 없어 삽입할 수 없습니다.")
        raise ValueError("ERROR : 유효한 데이터가 없어 삽입할 수 없습니다.")

def fct_afs_wc_to_redshift(data_interval_end: pendulum.datetime, **kwargs) -> None:
    logging.info("redshift 적재 시작")
    s3_key = kwargs['task_instance'].xcom_pull(task_ids='fct_afs_wc_to_s3', key='s3_key')
    s3_path = f's3://team-okky-1-bucket/{s3_key}'
    s3_hook = S3Hook(aws_conn_id='AWS_S3')
    redshift_hook = PostgresHook(postgres_conn_id='AWS_Redshift')
    bucket_name = 'team-okky-1-bucket'
    csv_content = s3_hook.read_key(s3_key, bucket_name)
    logging.info(f"S3 경로: {s3_key}")
    
    csv_reader = csv.reader(StringIO(csv_content))
    next(csv_reader)  # Skip 헤더
    
    data = []
    for row in csv_reader:
        try:
            reg_id, tm_fc, tm_ef, mood_key, stn_id, cnt_cd, min_ta, max_ta, min_l_ta, min_h_ta, max_l_ta, max_h_ta = row
            tm_fc = pendulum.parse(tm_fc, strict=False)
            data_key = data_interval_end + pendulum.duration(hours=9)
            created_at = tm_fc
            updated_at = tm_fc
            data.append((reg_id, tm_fc, tm_ef, mood_key, stn_id, cnt_cd, min_ta, max_ta, min_l_ta, min_h_ta, max_l_ta, max_h_ta, data_key, created_at, updated_at))
        except ValueError as e:
            logging.warning(f"ERROR : 파싱오류: {row}, error: {e}")
            
    if data:
        logging.info(f"{len(data)} rows 데이터를 읽었습니다.")
        conn = redshift_hook.get_conn()
        cursor = conn.cursor()

        insert_query = """
            INSERT INTO raw_data.fct_afs_wc_info (REG_ID, TM_FC, TM_EF, MODE_KEY, STN_ID, CNT_CD, MIN_TA, MAX_TA, MIN_L_TA, MIN_H_TA, MAX_L_TA, MAX_H_TA, DATA_KEY, CREATED_AT, UPDATED_AT)
            VALUES %s;
        """
        
        try:
            execute_values(cursor, insert_query, data)
            affected_rows = cursor.rowcount
            conn.commit()
            logging.info(f"성공적으로 적재된 행 수: {affected_rows}")
            logging.info(f"Redshift 적재 완료: {s3_path}")
        except Exception as e:
            raise ValueError(f"Redshift 로드 실패: {e}")
    else:
        logging.error("ERROR : 적재할 데이터가 없습니다.")
        raise ValueError("ERROR : 적재할 데이터가 없습니다.")

with DAG(
    'fct_afs_wc_to_s3_and_redshift',
    default_args=default_args,
    description='중기기온예보 S3 & redshift 적재',
    schedule_interval='0 7,19 * * *',
    catchup=True,
    dagrun_timeout=pendulum.duration(hours=2),
    tags=['중기', 'Daily', '2 time', 'raw'],
) as dag:
    dag.timezone = kst
    
    fct_afs_wc_to_s3 = PythonOperator(
        task_id='fct_afs_wc_to_s3',
        python_callable=fct_afs_wc_to_s3,
        provide_context=True,
        execution_timeout=pendulum.duration(hours=1),
    )
    
    fct_afs_wc_to_redshift = PythonOperator(
        task_id='fct_afs_wc_to_redshift',
        python_callable=fct_afs_wc_to_redshift,
        provide_context=True,
        execution_timeout=pendulum.duration(hours=1),
    )

    fct_afs_wc_to_s3 >> fct_afs_wc_to_redshift
