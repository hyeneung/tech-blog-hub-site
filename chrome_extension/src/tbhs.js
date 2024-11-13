class TbhsContent {
  constructor(type, data) {
    this.type = type;
    this.title = data.title;
    this.pubDate = data.pub_date.substr(0, 10);
    this.companyName = data.company_name;
    this.url = data.url;
    this.summarizedText = data.summarized_text.replace(/\n/g, "<br>");
    this.hashtags = data.hashtags;
  }

  createContent() {
    const content = document.createElement("div");
    content.className = "tbhs__main-body__carousel__content";
    content.href = this.url;

    content.innerHTML = `
      <div class="tbhs__main-body__carousel__content__title-and-date">
        <div class="tbhs__main-body__carousel__content__title">
          <h2 class="tbhs__main-body__carousel__content__title-text">${this.type}: ${this.title}</h2>
        </div>
        <div class="tbhs__main-body__carousel__content__date">
          <span class="tbhs__main-body__carousel__content__date-text">${this.pubDate}</span>
        </div>
      </div>
      <div class="tbhs__main-body__carousel__content__author-and-tags">
        <div class="tbhs__main-body__carousel__content__author">
          <img class="tbhs__main-body__carousel__content__author-icon" src="${chrome.runtime.getURL(`assets/company_logo/${this.companyName}.png`)}" />
          <span class="tbhs__main-body__carousel__content__author-name">${this.companyName}</span>
        </div>
        <div class="tbhs__main-body__carousel__content__tags">
          ${this.hashtags.map(tag => `<span class="tbhs__main-body__carousel__content__tag">#${tag}</span>`).join("\n")}
        </div>
      </div>
      <details class="tbhs__main-body__carousel__content__summary">
        <summary class="tbhs__main-body__carousel__content__summary-btn">요약된 내용 보기</summary>
        <div class="tbhs__main-body__carousel__content__summary-wrapper">
          <p class="tbhs__main-body__carousel__content__summary-text">${this.summarizedText}</p>
        </div>
      </details>
    `;

    content.addEventListener("click", (event) => {
      if (!event.target.closest(".tbhs__main-body__carousel__content__summary")) {
        window.open(this.url, "_self");
      }
    });

    return content;
  }
}


class TbhsMain {
  constructor(currentData, recommendDatas) {
    this.currentData = currentData;
    this.recommendDatas = recommendDatas;
  }

  createMain() {
    const main = document.createElement("div");
    main.className = "tbhs__main";

    const currentContent = new TbhsContent("현재 글", this.currentData).createContent();

    const recommendContents = this.recommendDatas.map(
      recommendData => new TbhsContent("추천 글", recommendData).createContent()
    );

    main.innerHTML = `
      <div class="tbhs__main-wrapper">
        <div class="tbhs__main-container">
          <div class="tbhs__main-header">
            <a href="https://www.tech-blog-hub.site/" class="tbhs__main-header__logo">
              <img class="tbhs__main-header__logo-icon" src="${chrome.runtime.getURL("assets/tbhs_logo.png")}" />
              <h1 class="tbhs__main-header__logo-title">기술 블로그 허브 사이트</h1>
            </a>
          </div>
          <div class="tbhs__main-body">
            <div class="tbhs__main-body__carousel">
              <button class="tbhs__main-body__carousel__prev-btn">&lt;</button>
              <div class="tbhs__main-body__carousel__contents">
              </div>
              <button class="tbhs__main-body__carousel__next-btn">&gt;</button>
            </div>
            <div class="tbhs__main-body__indicators">
            </div>
          </div>
          <div class="tbhs__main-footer">
            <span class="tbhs__main-footer__announcement">
              Summaries and hashtags are generated using LLM
            </span>
          </div>
        </div>
      </div>
      <div class="tbhs__main-btn">
        <div class="tbhs__main-btn__box">
          <div class="tbhs__main-btn__box-text">&and;</div>
        </div>
      </div>
    `;

    const contents = main.querySelector(".tbhs__main-body__carousel__contents");
    contents.appendChild(currentContent);
    recommendContents.forEach((recommendContent) => {
      contents.appendChild(recommendContent);
    });

    const indicators = main.querySelector(".tbhs__main-body__indicators");
    for (let i = 0; i <= this.recommendDatas.length; i += 1) {
      const indicator = document.createElement("div");
      indicator.className = "tbhs__main-body__indicator";
      indicator.id = `tbhs__indicator-${i}`;
      indicators.appendChild(indicator);
    }

    return main;
  }
}


function updateCarousel(contents, contentItems, indicators, currentIndex) {
  contentItems.forEach((content) => {
    content.querySelector(".tbhs__main-body__carousel__content__summary").open = false;
  });
  contents.scrollTo({
    left: contents.clientWidth * currentIndex,
    behavior: "smooth"
  });
  indicators.forEach((indicator) => {
    indicator.classList.remove("checked");
  });
  indicators[currentIndex].classList.add("checked");
}


function insertMain(data) {
  if (data === null) return;

  const tbhsMain = new TbhsMain(data.current, data.recommend).createMain();
  document.body.insertAdjacentElement("beforebegin", tbhsMain);

  const tbhsWrapper = tbhsMain.querySelector(".tbhs__main-wrapper");
  const tbhsContents = tbhsMain.querySelector(".tbhs__main-body__carousel__contents");
  const tbhsContentItems = tbhsMain.querySelectorAll(".tbhs__main-body__carousel__content");
  const tbhsIndicators = tbhsMain.querySelectorAll(".tbhs__main-body__indicator");
  const tbhsMainBtn = tbhsMain.querySelector(".tbhs__main-btn");
  const tbhsMainBtnArrow = tbhsMain.querySelector(".tbhs__main-btn__box-text");
  const tbhsMainContainerHeight = tbhsMain.querySelector(".tbhs__main-container").clientHeight;
  const tbhsTotalContentItems = tbhsContentItems.length;
  let tbhsCurrentIndex = 0;
  let tbhsIsOpened = true;

  tbhsIndicators[tbhsCurrentIndex].classList.add("checked");

  tbhsMainBtn.style.top = `${tbhsMainContainerHeight}px`;

  tbhsIndicators.forEach((indicator) => {
    indicator.addEventListener("click", (event) => {
      tbhsCurrentIndex = parseInt(event.target.id.split("-")[1]);
      updateCarousel(tbhsContents, tbhsContentItems, tbhsIndicators, tbhsCurrentIndex);
    });
  });

  tbhsMain.querySelector(".tbhs__main-body__carousel__prev-btn").addEventListener("click", () => {
    if (tbhsCurrentIndex > 0) {
      tbhsCurrentIndex -= 1;
    } else tbhsCurrentIndex = tbhsTotalContentItems - 1;
    updateCarousel(tbhsContents, tbhsContentItems, tbhsIndicators, tbhsCurrentIndex);
  });
  
  tbhsMain.querySelector(".tbhs__main-body__carousel__next-btn").addEventListener("click", () => {
    if (tbhsCurrentIndex < tbhsTotalContentItems - 1) {
      tbhsCurrentIndex += 1;
    } else tbhsCurrentIndex = 0;
    updateCarousel(tbhsContents, tbhsContentItems, tbhsIndicators, tbhsCurrentIndex);
  });

  tbhsMain.querySelector(".tbhs__main-btn__box").addEventListener("click", () => {
    if (tbhsIsOpened) {
      tbhsWrapper.style.top = `-${tbhsMainContainerHeight}px`;
      tbhsMainBtn.style.top = "0px"
      tbhsMainBtnArrow.style.transform = "rotate(180deg)";
      tbhsIsOpened = false;
    } else {
      tbhsWrapper.style.top = "0px";
      tbhsMainBtn.style.top = `${tbhsMainContainerHeight}px`;
      tbhsMainBtnArrow.style.transform = "";
      tbhsIsOpened = true;
    }
  });
}

async function fetchData(apiRequestUrl) {
  if (apiRequestUrl === null) return null;

  return await fetch(apiRequestUrl, {
    methos: "GET",
    headers: {
      "Content-type": "application/json"
    }
  }).then(res => {
    if (res.status === 200) {
      return res.json();
    } else return null;
  }).then(res => {
    if (res !== null && res["message"] === "success") {
      return res["body"];
    } else return null;
  });

  // return {
  //   "recommend": [
  //     {
  //       "title": "베네딕트는 왜 이프카카오에서 안성재 성대모사를 했을까?",
  //       "pub_date": "2024-11-08T00:00:00Z",
  //       "company_name": "카카오",
  //       "url": "https://tech.kakao.com/posts/659",
  //       "summarized_text": "베네딕트가 이프카카오 발표 중 안성재 셰프의 성대모사를 한 이유와 발표 준비 과정에 대한 글입니다.\n\n목차:\n1. 발표 배경\n2. 발표 준비 과정\n3. 안성재 셰프의 심사 기준\n4. 코드버디와 PR의 의도\n5. AI 기술의 중요성\n6. 코드버디의 역할",
  //       "hashtags": [
  //         "AICodeReviewer",
  //         "PullRequest",
  //         "Presentation",
  //         "Storytelling",
  //         "KakaoAI",
  //         "SoftwareEngineering"
  //       ]
  //     },
  //     {
  //       "title": "AWS DMS를 활용하여 MySQL 트랜잭셔널 데이터를 Amazon OpenSearch Service로 복제하기",
  //       "pub_date": "2024-11-06T06:27:33Z",
  //       "company_name": "AWS",
  //       "url": "https://aws.amazon.com/ko/blogs/tech/rdb2opensearch-usging-dms/",
  //       "summarized_text": "AWS DMS를 이용해 MySQL 트랜잭셔널 데이터를 Amazon OpenSearch Service로 실시간 복제하는 방법을 설명하는 글입니다.\n\n목차:\n1. 배경\n2. 아키텍처\n3. 사전 작업\n4. DMS 구성 및 태스크 시작\n5. 복제 검증 (Full load)\n6. 테스트 (CDC)\n7. 결론",
  //       "hashtags": [
  //         "Infra",
  //         "AmazonOpenSearch",
  //         "MySQL",
  //         "SemanticSearch",
  //         "AWSDMS"
  //       ]
  //     }
  //   ],
  //   "current": {
  //     "title": "모닥불 | EP.5 토스 개발자는 개발만 잘해도 될까",
  //     "pub_date": "2024-09-25T09:44:00Z",
  //     "company_name": "토스",
  //     "url": "https://toss.tech/article/firesidechat_frontend_5",
  //     "summarized_text": "토스 개발자의 기준과 일 잘하는 개발자란 무엇인지에 대해 이야기하는 블로그 글입니다.\n\n목차:\n1. 토스의 개발자 기준\n2. 좋은 코드는 제품의 성공을 보장하지 않는다\n3. 개발자는 요구사항 정의와 구현이 중요하다\n4. 실제 업무 적용 팁\n5. 개발자가 개발만 잘해야 하는가?",
  //     "hashtags": [
  //       "Toss",
  //       "Developer",
  //       "SoftwareEngineering"
  //     ]
  //   }
  // };
}


function getUrl() {
  const domains = [
    "helloworld.kurly.com", // 컬리
    "techblog.lycorp.co.jp", // 라인
    "toss.tech", // 토스
    "medium.com", // 당근, CJ온스타일, 29CM, 헤이딜러
    "tech.kakao.com", // 카카오
    "tech.kakaopay.com", // 카카오페이
    "aws.amazon.com", // AWS
    "techblog.yogiyo.co.kr", // 요기요
    "techblog.gccompany.co.kr", // 여기어때
    "ebay-korea.tistory.com", // 지마켓
    "techtopic.skplanet.com", // SK플래닛
    "saramin.github.io", // 사람인
    "tech.devsisters.com", // 데브시스터즈
    "tech.hancom.com",  // 한글과컴퓨터
    "blog.banksalad.com", // 뱅크샐러드
    "spoqa.github.io", // 스포카
    "labs.brandi.co.kr" // 브랜디
  ];

  const mediumSites = [
    "daangn", // 당근
    "cj-onstyle", // CJ온스타일
    "29cm", // 29CM
    "prnd" // 헤이딜러
  ];

  let currentProtocol = window.location.protocol;
  let currentDomain = window.location.hostname;
  let currentPath = encodeURI(window.location.pathname);
  const currentQuery = encodeURI(window.location.search);

  if (!domains.includes(currentDomain)) return null;
  if (currentDomain === "medium.com" && !mediumSites.includes(currentPath.split("/")[1])) return null;

  if (currentDomain === "helloworld.kurly.com") {
    currentProtocol = "http:"
    currentDomain = "thefarmersfront.github.io";
  }
  if (currentDomain === "tech.devsisters.com") {
    currentPath = currentPath.substring(0, currentPath.length - 1);
  }
  if (currentDomain === "labs.brandi.co.kr") {
    currentProtocol = "http:"
  }

  const requestUrl = `${currentProtocol}//${currentDomain}${currentPath}${currentQuery}`;
  // console.log(`https://www.tech-blog-hub.site/api/v1/recommend?url=${requestUrl}`);
  console.log(requestUrl);
  return `https://www.tech-blog-hub.site/api/v1/recommend?url=${requestUrl}`;
}

// brandi -> no extension (추가 확인)


function init() {
  fetchData(getUrl()).then(fetchedData => insertMain(fetchedData));
}


init();

// 버튼을 기존의 영역에서 튀어나오도록 해서 처리하면 못 클릭하는 영역이 없지 않을까?
// -----------------------------
// |           |   |           |
// |           |   |           |
// -----------------------------
//             |btn|
//             -----