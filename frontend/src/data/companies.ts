interface Company {
    name: string;
    logo: () => Promise<typeof import('*.png')>;
}

  
export const companies: Company[] = [
    { name: "라인", logo: () => import('@/assets/company_logos/line.png') },
    { name: "토스", logo: () => import('@/assets/company_logos/toss.png') },
    { name: "당근", logo: () => import('@/assets/company_logos/daangn.png') },
    { name: "카카오", logo: () => import('@/assets/company_logos/kakao.png') },
    { name: "우아한형제들", logo: () => import('@/assets/company_logos/woowahan.png') },
    { name: "카카오페이", logo: () => import('@/assets/company_logos/kakaopay.png') },
    { name: "AWS", logo: () => import('@/assets/company_logos/aws.png') },
    { name: "컬리", logo: () => import('@/assets/company_logos/kurly.png') },
    { name: "요기요", logo: () => import('@/assets/company_logos/yogiyo.png') },
    { name: "여기어때", logo: () => import('@/assets/company_logos/gccompany.png') },
    { name: "지마켓", logo: () => import('@/assets/company_logos/gmarket.png') },
    { name: "SK플래닛", logo: () => import('@/assets/company_logos/skplanet.png') },
    { name: "사람인", logo: () => import('@/assets/company_logos/saramin.png') },
    { name: "데브시스터즈", logo: () => import('@/assets/company_logos/devsisters.png') },
    { name: "한글과컴퓨터", logo: () => import('@/assets/company_logos/hancom.png') },
    { name: "뱅크샐러드", logo: () => import('@/assets/company_logos/banksalad.png') },
    { name: "CJ온스타일", logo: () => import('@/assets/company_logos/cjonstyle.png') },
    { name: "스포카", logo: () => import('@/assets/company_logos/spoqa.png') },
    { name: "29CM", logo: () => import('@/assets/company_logos/29cm.png') },
    { name: "브랜디", logo: () => import('@/assets/company_logos/brandi.png') },
    { name: "헤이딜러", logo: () => import('@/assets/company_logos/heydealer.png') }
];