FROM public.ecr.aws/lambda/python:3.11

# Install Python dependencies for function
COPY requirements.txt /tmp/
RUN python3 -m pip install --upgrade pip -q
RUN python3 -m pip install -r /tmp/requirements.txt -q

# Copy all necessary files and folders to the container
COPY . ${LAMBDA_TASK_ROOT}/

WORKDIR ${LAMBDA_TASK_ROOT}

# Lambda 핸들러 설정
CMD ["lambda_function.lambda_handler"]