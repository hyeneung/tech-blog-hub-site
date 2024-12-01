# 🌐 Tech Blog Hub Site

<p align="center">
  <img src="https://www.tech-blog-hub.site/assets/logo-KTly0f2B.png" alt="Tech Blog Hub Logo" width="200"/>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/version-1.0.0-blue.svg" alt="version"/>
  <img src="https://img.shields.io/badge/license-MIT-green.svg" alt="license"/>
</p>

> Explore, analyze, and discover tech blog posts from various companies all in one place!

**🚀 [Visit Tech Blog Hub](https://www.tech-blog-hub.site)**

## 🔎 Overview

Tech Blog Hub Site is a capstone design project for the KHU 3-2 Data Analysis course. It aims to create a cutting-edge platform that aggregates, analyzes, and recommends tech blog posts from diverse companies. This academic endeavor harnesses advanced natural language processing techniques to extract and analyze hashtags from blog content, facilitating content discovery through related hashtags and topics.

### Key aspects of our project include:
- Aggregation of tech blog posts from multiple company sources
- Automated hashtag extraction and analysis from blog content
- Personalized content recommendations derived from user logs.
  - With our Chrome extension program, users can access a technology blog recommendation service in conjunction with our website Tech Blog Hub Site. By visiting specific company tech blogs and running the extension program, users receive summary information of the posts, hashtags, and recommendations of other tech blog posts.
  - This extension allows users to read other tech blog posts on similar topics without returning to our site.
https://chromewebstore.google.com/detail/tech-blog-hub-site-extens/jkccccofndhnikmhcfmgcelhbmbpncmh
## ✨ Features

- Automated RSS feed scraping from various tech company blogs
- Natural Language Processing for text analysis and hashtag extraction
- Advanced search functionality using hashtag filters
- Personalized content recommendations based on user activity logs

[Detailed Project Presentation](https://docs.google.com/presentation/d/1dQycfTnDb-gflfqTdEr3cU8wBd9EVCDA9jUdFHy9PpY/edit?usp=sharing)

## 📹 Demonstration Video

[Watch the Demonstration Video](https://drive.google.com/file/d/1Tp3tB6NE2iWXGJYb2OTA_AnpTMgWLzhZ/view?usp=sharing)

## ⚙️ AWS Architecture
![image](https://github.com/user-attachments/assets/6898ae53-c5e3-4db4-9ee5-4bfdeb167e01)

## 👥 Team

| <img src="https://github.com/hyeneung.png" width="100px;"/><br />[hyeneung](https://github.com/hyeneung) | <img src="https://github.com/chanhy-lee.png" width="100px;"/><br />[chanhy-lee](https://github.com/chanhy-lee) | <img src="https://github.com/MintChoco0706.png" width="100px;"/><br />[MintChoco0706](https://github.com/MintChoco0706) |
|:---:|:---:|:---:|
| Project Lead & Full-Stack Developer | Data Scientist | Data Scientist |
| Project Manager & frontend, backend, and infrastructure development | Content Summarization Specialist & Chrome Extension Developer | Hashtag Extraction Specialist & Log Analysis for Recommendation Systems |


## 📁 Project Structure

Our project is organized into several key directories, each serving a specific purpose in our serverless architecture:

`backend` (Deprecated): Originally for EC2 deployment, implements OpenAPI Specification(OAS) using a delegate pattern. Inspired by [Daangn's Community Room team blog post](https://medium.com/daangn/%EC%BB%A4%EB%AE%A4%EB%8B%88%ED%8B%B0%EC%8B%A4-api-design-first-%EC%A0%91%EA%B7%BC%EB%B0%A9%EC%8B%9D-%EC%A0%95%EC%B0%A9%EA%B8%B0-cecca0a37c05). Deprecated after serverless transition. ([issue #6](https://github.com/hyeneung/tech-blog-hub-site/issues/6))

`chrome_extension`: Chrome extension code for recommendation system functionality.

`config` (Deprecated): Previously for ELK stack configuration([issue #18](https://github.com/hyeneung/tech-blog-hub-site/issues/18)), gRPC protobuf files, and OAS YAML files ([issue #13](https://github.com/hyeneung/tech-blog-hub-site/issues/13)). Deprecated after serverless transition.

`crawler` (Deprecated): Houses the crawler code, which originally used gRPC to call the text_handler. This has been updated to invoke the text_handler Lambda function in our serverless architecture. ([issue #1](https://github.com/hyeneung/tech-blog-hub-site/issues/1))

`frontend`: Frontend code using TypeScript and Axios generated from OpenAPI spec YAML. ([issue #7](https://github.com/hyeneung/tech-blog-hub-site/issues/7))

`log_analysis`: Recommendation system-related code.

`opensearch-util`: Utility scripts for OpenSearch database management. These scripts are executed via a NAT instance in the public subnet.

`serverless`: Lambda function code, core of our serverless architecture. ([issue #22](https://github.com/hyeneung/tech-blog-hub-site/issues/22))

`text_handler` (Deprecated): Former gRPC server code for LLM API usage, deprecated after serverless transition.

## 📄 License
This project is distributed under the MIT License. See the LICENSE file for more information.
