import base64
import logging
import urllib.parse
from typing import Any, Dict, List, Optional

import requests
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from django.conf import settings
from django.core.cache import cache

logger = logging.getLogger(__name__)


class CodefException(Exception):
    """CODEF API 통신 및 비즈니스 예외"""
    def __init__(self, code: str, message: str, extra_message: Optional[str] = None):
        super().__init__(f"[{code}] {message}" + (f" ({extra_message})" if extra_message else ""))
        self.code = code
        self.message = message
        self.extra_message = extra_message


class CodefClient:
    """
    CODEF B2B 금융 API 클라이언트
    
    기능:
    - OAuth 2.0 Access Token 발급 및 Redis 캐싱 (기본 7일 유효, 6일 주기로 갱신)
    - RSA 공개키 기반 민감 정보(비밀번호 등) 암호화
    - 계정 등록 (Connected ID 발급)
    - 법인/개인 은행 계좌 거래내역 조회
    """

    OAUTH_URL = "https://oauth.codef.io/oauth/token"
    TOKEN_CACHE_KEY = "codef_access_token_v1"

    def __init__(self, is_sandbox: bool = False):
        self.is_sandbox = is_sandbox
        if is_sandbox:
            self.host = "https://sandbox.codef.io"
            self.client_id = getattr(settings, 'CODEF_SANDBOX_CLIENT_ID', 'ef27cfaa-10c1-4470-adac-60ba476273f9')
            self.client_secret = getattr(settings, 'CODEF_SANDBOX_CLIENT_SECRET', '83160c33-9045-4915-86d8-809473cdf5c3')
        else:
            self.host = getattr(settings, 'CODEF_HOST', 'https://development.codef.io')
            self.client_id = getattr(settings, 'CODEF_CLIENT_ID', '')
            self.client_secret = getattr(settings, 'CODEF_CLIENT_SECRET', '')

        self.public_key_str = getattr(settings, 'CODEF_PUBLIC_KEY', '')

    def get_access_token(self, force_refresh: bool = False) -> str:
        """
        OAuth 2.0 액세스 토큰 취득 (Redis 캐싱 활용)
        """
        cache_key = f"{self.TOKEN_CACHE_KEY}_{'sandbox' if self.is_sandbox else 'demo'}"
        if not force_refresh:
            token = cache.get(cache_key)
            if token:
                return token

        if not self.client_id or not self.client_secret:
            raise ValueError("CODEF client_id 또는 client_secret이 설정되지 않았습니다.")

        auth_str = f"{self.client_id}:{self.client_secret}"
        auth_b64 = base64.b64encode(auth_str.encode("utf-8")).decode("utf-8")

        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Basic {auth_b64}"
        }
        data = {"grant_type": "client_credentials"}

        try:
            resp = requests.post(self.OAUTH_URL, data=data, headers=headers, timeout=10)
            resp.raise_for_status()
            res_json = resp.json()

            access_token = res_json.get("access_token")
            expires_in = res_json.get("expires_in", 604800)  # 기본 7일

            if not access_token:
                raise CodefException("TOKEN_ERROR", "액세스 토큰을 발급받지 못했습니다.", str(res_json))

            # 만료 시간보다 1일 여유 있게 캐시 저장 (약 6일)
            cache_timeout = max(3600, expires_in - 86400)
            cache.set(cache_key, access_token, timeout=cache_timeout)
            logger.info("CODEF Access Token 발급 및 캐싱 완료 (TTL: %d초)", cache_timeout)
            return access_token

        except requests.RequestException as e:
            logger.error("CODEF 토큰 발급 네트워크 오류: %s", str(e))
            raise CodefException("NETWORK_ERROR", "CODEF 토큰 발급 요청 중 네트워크 오류가 발생했습니다.", str(e))

    def encrypt_rsa(self, plain_text: str) -> str:
        """
        CODEF RSA 공개키(PKCS#1 v1.5)를 사용하여 평문(비밀번호 등)을 암호화 후 Base64 반환
        """
        if not self.public_key_str:
            raise ValueError("CODEF_PUBLIC_KEY 설정이 누락되었습니다.")

        # PEM 포맷 정규화
        clean_key = self.public_key_str.strip().replace("-----BEGIN PUBLIC KEY-----", "").replace("-----END PUBLIC KEY-----", "").replace("\n", "").replace(" ", "")
        pem_formatted = f"-----BEGIN PUBLIC KEY-----\n{clean_key}\n-----END PUBLIC KEY-----"

        try:
            public_key = serialization.load_pem_public_key(pem_formatted.encode("utf-8"))
            encrypted_bytes = public_key.encrypt(
                plain_text.encode("utf-8"),
                padding.PKCS1v15()
            )
            return base64.b64encode(encrypted_bytes).decode("utf-8")
        except Exception as e:
            logger.error("RSA 암호화 실패: %s", str(e))
            raise ValueError(f"RSA 암호화 처리 중 오류가 발생했습니다: {str(e)}")

    def _request(self, endpoint: str, body: Dict[str, Any]) -> Dict[str, Any]:
        """
        CODEF API 공통 호출 메서드
        """
        token = self.get_access_token()
        url = f"{self.host}{endpoint}"
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        try:
            resp = requests.post(url, json=body, headers=headers, timeout=30)
            res_json = resp.json()

            # URL 디코딩 처리 (CODEF는 일부 응답 문자열을 URL 인코딩하여 반환할 수 있음)
            result = res_json.get("result", {})
            code = result.get("code", "")
            message = result.get("message", "")
            extra_msg = result.get("extraMessage", "")

            # 성공 코드: CF-00000
            if code == "CF-00000":
                return res_json.get("data", {})
            else:
                logger.warning("CODEF API 응답 오류 [%s]: %s (추가: %s)", code, message, extra_msg)
                raise CodefException(code=code, message=message, extra_message=extra_msg)

        except requests.RequestException as e:
            logger.error("CODEF API 요청 통신 오류: %s", str(e))
            raise CodefException("NETWORK_ERROR", f"CODEF API 호출 실패 ({endpoint})", str(e))

    def create_account(self, account_list: List[Dict[str, Any]]) -> str:
        """
        계정 등록 API (/v1/account/create)
        성공 시 connectedId 반환
        """
        endpoint = "/v1/account/create"
        body = {"accountList": account_list}
        data = self._request(endpoint, body)
        
        connected_id = data.get("connectedId")
        if not connected_id:
            raise CodefException("NO_CONNECTED_ID", "connectedId가 응답에 포함되지 않았습니다.")
        return connected_id

    def fetch_transactions(
        self,
        connected_id: str,
        organization: str,
        account_number: str,
        start_date: str,
        end_date: str,
        order_by: str = "0",
        inquiry_type: str = "0",
        is_business: bool = True
    ) -> List[Dict[str, Any]]:
        """
        수시입출 계좌 거래내역 조회
        
        Args:
            connected_id: 계정 등록 식별자
            organization: 은행 기관코드 (예: '0004' 국민, '0088' 신한 등)
            account_number: 계좌번호 (하이픈 제외 권장)
            start_date: 조회시작일 (YYYYMMDD)
            end_date: 조회종료일 (YYYYMMDD)
            order_by: "0"(최신순), "1"(과거순)
            inquiry_type: "0"(전체), "1"(입금), "2"(출금)
            is_business: True면 법인(/b/), False면 개인(/p/)
        """
        client_type = "b" if is_business else "p"
        endpoint = f"/v1/kr/bank/{client_type}/account/transaction-list"
        body = {
            "connectedId": connected_id,
            "organization": organization,
            "account": account_number,
            "startDate": start_date,
            "endDate": end_date,
            "orderBy": order_by,
            "inquiryType": inquiry_type
        }
        data = self._request(endpoint, body)

        # 응답 데이터 정규화 (기관별/엔드포인트별 거래내역 리스트 키 처리)
        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return (
                data.get("resTrHistoryList")
                or data.get("resTrList")
                or data.get("resAccountTrList")
                or data.get("resList")
                or []
            )
        return []

    def fetch_account_list(
        self,
        connected_id: str,
        organization: str,
        is_business: bool = True
    ) -> List[Dict[str, Any]]:
        """
        보유 은행 계좌 목록 조회 API (/v1/kr/bank/b/account/list 또는 /p/account/list)
        
        Args:
            connected_id: 계정 등록 식별자
            organization: 은행 기관코드 (예: '0004' 국민, '0088' 신한 등)
            is_business: True면 법인(/b/), False면 개인(/p/)
        """
        client_type = "b" if is_business else "p"
        endpoint = f"/v1/kr/bank/{client_type}/account/list"
        body = {
            "connectedId": connected_id,
            "organization": organization
        }
        data = self._request(endpoint, body)

        if isinstance(data, list):
            return data
        elif isinstance(data, dict):
            return (
                data.get("resAccountList")
                or data.get("resList")
                or data.get("resAccountTrList")
                or []
            )
        return []

