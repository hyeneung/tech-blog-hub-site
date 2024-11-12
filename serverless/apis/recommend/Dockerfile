FROM public.ecr.aws/lambda/python:3.11

# Install Python dependencies for function
COPY requirements.txt /tmp/
RUN python3 -m pip install --upgrade pip -q
RUN python3 -m pip install -r /tmp/requirements.txt -q

# Copy all necessary files and folders to the container
COPY bigquery ${LAMBDA_TASK_ROOT}/bigquery
COPY opensearch ${LAMBDA_TASK_ROOT}/opensearch
COPY lambda_function.py ${LAMBDA_TASK_ROOT}/lambda_function.py
COPY recommend.py ${LAMBDA_TASK_ROOT}/recommend.py

WORKDIR ${LAMBDA_TASK_ROOT}

# Lambda 핸들러 설정
CMD ["lambda_function.lambda_handler"]