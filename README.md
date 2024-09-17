# 🌐 Tech Blog Hub Site

<p align="center">
  <img src="path_to_your_logo.png" alt="Tech Blog Hub Logo" width="200"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="version"/>
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="license"/>
</p>

> A platform to aggregate, analyze, and recommend tech blog posts from various companies(3-2 data analysis capstone design)
## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [License](#license)

## 🔎 Overview

Tech Blog Hub Site is a capstone design project for the 3-2 Data Analysis course, aimed at creating a platform to aggregate, analyze, and recommend tech blog posts from various companies. This academic project leverages natural language processing techniques to extract and analyze hashtags from blog posts, enabling content discovery through related hashtags and topics.

Key aspects of our project include:
- Aggregation of tech blog posts from multiple company sources
- Automated hashtag extraction and analysis from blog content
- Content recommendation based on hashtag similarity
- Enhanced search functionality using hashtag-based indexing
- Trend analysis of popular topics in the tech industry through hashtag frequency

[Detailed Project Presentation](https://gamma.app/docs/-5i75coxbxfpndyl?mode=doc)
## ✨ Features

- Automated RSS feed scraping from various tech company blogs
- Natural Language Processing for text analysis and hashtag extraction
- Hashtag-based content recommendation system
- Advanced search functionality using hashtag filters
- Trend analysis and visualization of popular tech topics based on hashtag usage

## 📁 Project Structure

```
tech-blog-hub-site/
├── crawler/
│   ├── config/
│   ├── generated/
│   ├── internal/
│   │   ├── crawler/
│   │   ├── db/
│   │   ├── types/
│   │   └── utils/
│   └── main.go
├── text_handler/
│   ├── generated/
│   ├── model/
│   └── utils/
├── front/
├── api/
└── proto_config/
```

1. crawler/
   - 크롤러 관련 코드와 설정을 포함하는 메인 디렉토리
   - config/: 크롤러 설정 파일을 저장하는 폴더
   - generated/: grpc protobuf로 생성된 Go 코드
   - internal/
     - crawler/: 실제 크롤링 로직이 구현된 패키지
     - db/: 데이터베이스 관련 코드가 있는 패키지
     - types/: 공통으로 사용되는 타입 정의가 있는 패키지
     - utils/: 유틸리티 함수들이 모여있는 패키지
   - main.go: 크롤러 애플리케이션의 진입점

2. text_handler/
   - 텍스트 처리 관련 코드
   - generated/: grpc protobuf로 생성된 Python 코드
   - model/: 텍스트 데이터 모델 관련 코드
   - utils/: 텍스트 처리에 필요한 유틸리티 함수들

3. front/
   - 프론트엔드 관련 코드가 위치하는 디렉토리

4. api/
   - API 관련 코드나 정의가 포함된 디렉토리

5. proto_config/
   - 프로토콜 버퍼 정의 파일들이 저장되는 디렉토리
   - 서비스 간 통신을 위한 인터페이스를 정의

## 📄 License
This project is distributed under the MIT License. See the LICENSE file for more information.
