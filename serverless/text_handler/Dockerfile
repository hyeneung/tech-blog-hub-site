# docker build --platform linux/x86_64 -t lambda-selenium-docker -f Dockerfile .
FROM public.ecr.aws/lambda/python:3.9 as stage

RUN yum install -y -q sudo unzip
ENV CHROMIUM_VERSION=1002910

# Install Chromium
COPY install-browser.sh /tmp/
RUN /usr/bin/bash /tmp/install-browser.sh

FROM public.ecr.aws/lambda/python:3.9 as base

COPY chrome-deps.txt /tmp/
RUN yum install -y $(cat /tmp/chrome-deps.txt)

# Install Python dependencies for function
COPY requirements.txt /tmp/
RUN python3 -m pip install --upgrade pip -q
RUN python3 -m pip install -r /tmp/requirements.txt -q

COPY --from=stage /opt/chrome /opt/chrome
COPY --from=stage /opt/chromedriver /opt/chromedriver

# Copy all necessary files and folders to the container
COPY hashtag ${LAMBDA_TASK_ROOT}/hashtag
COPY summarize ${LAMBDA_TASK_ROOT}/summarize
COPY utils ${LAMBDA_TASK_ROOT}/utils
COPY lambda_function.py ${LAMBDA_TASK_ROOT}/lambda_function.py

WORKDIR ${LAMBDA_TASK_ROOT}

CMD [ "lambda_function.lambda_handler" ]