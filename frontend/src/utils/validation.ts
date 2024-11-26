/**
 * 해시태그 유효성 검사
 * @param hashtag 검사할 해시태그
 * @returns 유효하면 true, 그렇지 않으면 false
 */
function isValidHashtag(hashtag: string): boolean {
  return /^[a-zA-Z/]{1,15}$/.test(hashtag);
}

/**
 * 회사 이름 유효성 검사
 * @param company 검사할 회사 이름
 * @returns 유효하면 true, 그렇지 않으면 false
 */
function isValidCompany(company: string): boolean {
  return /^[a-zA-Z가-힣0-9]{0,10}$/.test(company);
}

/**
 * 검색어 유효성 검사
 * @param query 검사할 검색어
 * @returns 유효하면 true, 그렇지 않으면 false
 */
function isValidQuery(query: string): boolean {
  return /^[가-힣a-zA-Z0-9\s/,&+]{0,15}$/.test(query);
}

/**
 * 검색 파라미터 유효성 검사
 * @param params 검사할 검색 파라미터
 * @returns 오류 메시지 문자열 또는 null (검증 통과 시)
 */
export function validateSearchParams(params: {
  hashtags?: string[];
  company?: string;
  query?: string;
  page?: number;
  size?: number;
}): string | null {
  const { hashtags, company, query, page, size } = params;

  if (hashtags) {
    if (hashtags.length > 10) {
      return "해시태그는 최대 10개까지만 허용됩니다.";
    }
    if (hashtags.some(tag => !isValidHashtag(tag))) {
      return "유효하지 않은 해시태그가 포함되어 있습니다. (최대 15자, 알파벳과 / 만 허용)";
    }
  }

  if (company && !isValidCompany(company)) {
    return "유효하지 않은 회사 이름입니다. (최대 10자, 알파벳, 완성형 한글, 숫자만 허용)";
  }

  if (query && !isValidQuery(query)) {
    return "유효하지 않은 검색어입니다. (최대 15자, 완성형 한글, 알파벳, 숫자, 띄어쓰기, /, ,, &, + 만 허용)";
  }

  if (page !== undefined && (page < 0 || !Number.isInteger(page))) {
    return "유효하지 않은 페이지 번호입니다. (0 이상의 정수)";
  }

  if (size !== undefined && (size < 1 || size > 30 || !Number.isInteger(size))) {
    return "유효하지 않은 페이지 크기입니다. (1에서 30 사이의 정수)";
  }

  return null; // 유효한 경우
}