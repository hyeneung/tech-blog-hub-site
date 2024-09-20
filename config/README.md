# Config

This folder contains configuration files for API specifications and protocol buffers.

## Structure

- `openapi_config/`: OpenAPI specification for the Tech Blog Hub search API
- `proto_config/`: Protocol Buffer definitions for the crawler text handler

## Protocol Buffer Configuration

The `proto_config/crawler_text_handler.proto` file contains Protocol Buffer definitions for the crawler text handler.

### Generate Code

To generate code from the Protocol Buffer definition:

1. For Python:
- Prerequisites:
  ```bash
  pip install grpcio grpcio-tools
  ```
- Generate Python code:
  ```bash
  cd root/config/proto_config
  python -m grpc_tools.protoc -I. --python_out=../../text_handler/generated --grpc_python_out=../../text_handler/generated crawler_text_handler.proto
  ```
2. For Go:
- Prerequisites:
  ```bash
  go install google.golang.org/protobuf/cmd/protoc-gen-go@v1.34.2
  go install google.golang.org/grpc/cmd/protoc-gen-go-grpc@v1.5.1
  ```
- Generate Go code:
  ```bash
  cd root/config/proto_config
  protoc --go_out=. --go-grpc_out=. crawler_text_handler.proto
  ```
> **Important**: Ensure that the target folders (e.g., `root/text_handler/generated`) exist before running these commands. If they don't exist, create them first.

Make sure to run these commands from the appropriate directory to ensure correct file paths.

## OpenAPI Configuration

The `openapi_config/openapi.yaml` file defines the OpenAPI Specification for the Tech Blog Hub search API. 

### Generate Code

To generate server and client code from the OpenAPI specification:

1. Install openapi-generator:
    ```bash
    npm install @openapitools/openapi-generator-cli -g
    ```
2. Generate server code:
  - spring boot server
    ```bash
    cd root/config/openapi_config
    ```
    ```bash
    npx @openapitools/openapi-generator-cli generate -i ./openapi.yaml -g spring -o ../../backend/generated-spring-server --additional-properties=useSpringBoot3=true,springBootVersion=3.1.3,artifactId=backend,artifactVersion=0.0.1-SNAPSHOT,delegatePattern=true,serializableModel=true --api-package=com.openapi.gen.springboot.api --model-package=com.openapi.gen.springboot.dto
    ```
    ```bash
    copy /Y openapi.yaml ..\..\backend\src\main\resources\swagger\openapi.yaml
    cp -f openapi.yaml ../../backend/src/main/resources/swagger/openapi.yaml
    ```

   - go server
        ```bash
        cd root/config/openapi_config
        ```
        ```bash
        npx @openapitools/openapi-generator-cli generate -i ./openapi.yaml -g go-server -o ../../backend/generated-go-server --additional-properties=packageName=generated,generateInterfaces=true,enumClassPrefix=true,structPrefix=true
        ```

3. Generate TypeScript Axios client:
   ```bash
   npx @openapitools/openapi-generator-cli generate -i ./openapi.yaml -g typescript-axios -o ../../front/generated-typescript-client --additional-properties=supportsES6=true,npmName=tech-blog-hub-api-client
   ```