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
.
├── crawler/
│   ├── generated/
│   └── utils/
├── text_handler/
│   ├── generated/
│   ├── model/
│   └── utils/
├── front/
├── api/
└── proto_config/
```

- `crawler/`: RSS 피드 스크래핑 관련 코드
  - `generated/`: gRPC protobuf로부터 생성된 코드
  - `utils/`: 크롤러 유틸리티 함수
- `text_handler/`: 텍스트 처리 서비스 관련 코드
  - `generated/`: gRPC protobuf로부터 생성된 코드
  - `model/`: 텍스트 처리 모델
  - `utils/`: 텍스트 처리 유틸리티 함수
- `front/`: 프론트엔드 관련 코드
- `api/`: API 서버 관련 코드
- `proto_config/`: gRPC 프로토콜 버퍼 정의 파일

## 📄 License
This project is distributed under the MIT License. See the LICENSE file for more information.
