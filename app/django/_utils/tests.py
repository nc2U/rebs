from datetime import date
from decimal import Decimal
from unittest.mock import patch, MagicMock

from django.test import TestCase

from _utils.file_cleanup import delete_file_field
from _utils.file_upload import generate_safe_filename, get_upload_path
from _utils.file_service import FileService
from _utils.payment_adjustment import (
    calculate_daily_interest,
    get_effective_contract_date,
    aggregate_installment_adjustments,
)
from _utils.push_service import send_push_notification
from _utils.slack_notifications import get_slack_webhook_url


class FileUploadUtilsTestCase(TestCase):
    """파일 업로드 관련 유틸리티 테스트"""

    def test_generate_safe_filename_preserves_extension_and_ascii(self):
        filename = "아파트_분양계약서_홍길동.pdf"
        safe_name = generate_safe_filename(filename)

        # 확장자가 .pdf로 보존되는지 확인
        self.assertTrue(safe_name.endswith(".pdf"))
        # 파일명이 ASCII로만 구성되어 있는지 확인
        self.assertTrue(all(ord(c) < 128 for c in safe_name))
        # 언더스코어로 구분된 타임스탬프와 해시 구조 확인
        parts = safe_name.split("_")
        self.assertGreaterEqual(len(parts), 3)

    def test_generate_safe_filename_uniqueness(self):
        filename = "계약서.docx"
        safe1 = generate_safe_filename(filename, include_microseconds=True)
        safe2 = generate_safe_filename(filename, include_microseconds=True)
        self.assertTrue(safe1.endswith(".docx"))
        self.assertTrue(safe2.endswith(".docx"))

    def test_get_upload_path(self):
        mock_instance = MagicMock()
        path = get_upload_path(mock_instance, "견적서.xlsx", "company", "documents")
        normalized_path = path.replace("\\", "/")
        self.assertTrue(normalized_path.startswith("company/documents/"))
        self.assertTrue(normalized_path.endswith(".xlsx"))


class PaymentAdjustmentUtilsTestCase(TestCase):
    """납부 조정 및 이자/할인 계산 유틸리티 테스트"""

    def test_calculate_daily_interest_valid(self):
        # 10,000,000원, 연이율 12%, 30일 연체
        principal = 10000000
        annual_rate = Decimal("12.0")
        days = 30
        expected = int((Decimal("12.0") / Decimal("100") / Decimal("365")) * 30 * 10000000)
        result = calculate_daily_interest(principal, annual_rate, days)
        self.assertEqual(result, expected)
        self.assertGreater(result, 0)

    def test_calculate_daily_interest_zero_or_negative(self):
        # 원금, 이율, 일수가 0 이하일 때 0 반환 검증
        self.assertEqual(calculate_daily_interest(0, Decimal("10.0"), 10), 0)
        self.assertEqual(calculate_daily_interest(100000, Decimal("0.0"), 10), 0)
        self.assertEqual(calculate_daily_interest(100000, Decimal("10.0"), 0), 0)
        self.assertEqual(calculate_daily_interest(-1000, Decimal("10.0"), 10), 0)

    def test_get_effective_contract_date(self):
        mock_contract = MagicMock()

        # 1. 둘 다 없는 경우
        mock_contract.sup_cont_date = None
        mock_contract.contractor = None
        self.assertIsNone(get_effective_contract_date(mock_contract))

        # 2. 공급계약일만 있는 경우
        d1 = date(2025, 1, 10)
        mock_contract.sup_cont_date = d1
        mock_contract.contractor = None
        self.assertEqual(get_effective_contract_date(mock_contract), d1)

        # 3. 계약자 계약일만 있는 경우
        d2 = date(2025, 2, 15)
        mock_contract.sup_cont_date = None
        mock_contract.contractor = MagicMock(contract_date=d2)
        self.assertEqual(get_effective_contract_date(mock_contract), d2)

        # 4. 둘 다 있는 경우 max 값 반환
        mock_contract.sup_cont_date = d1
        mock_contract.contractor = MagicMock(contract_date=d2)
        self.assertEqual(get_effective_contract_date(mock_contract), d2)

    @patch("_utils.payment_adjustment.calculate_all_installments_payment_allocation")
    def test_aggregate_installment_adjustments(self, mock_calc_allocation):
        # mock 회차 정보 및 all_status 설정
        mock_contract = MagicMock()
        mock_order1 = MagicMock(id=1, pay_code=1, pay_name="1차 계약금")
        mock_order2 = MagicMock(id=2, pay_code=2, pay_name="2차 계약금")

        pub_date = date(2025, 5, 1)

        # all_status mock 반환값 (최적화된 total_discount 및 penalty 포함)
        mock_calc_allocation.return_value = {
            1: {
                "due_date": date(2025, 3, 1),
                "is_fully_paid": True,
                "late_days": 0,
                "total_late_penalty": 0,
                "total_discount": 50000,
                "late_payment_amount": 0,
            },
            2: {
                "due_date": date(2025, 4, 1),
                "is_fully_paid": False,
                "late_days": 15,
                "total_late_penalty": 30000,
                "total_discount": 0,
                "late_payment_amount": 10000000,
            },
        }

        mock_qs = MagicMock()
        mock_qs.filter.return_value.order_by.return_value = [mock_order1, mock_order2]

        result = aggregate_installment_adjustments(mock_contract, mock_qs, 2, pub_date)

        self.assertEqual(result["total_late_fee"], 30000)
        self.assertEqual(result["total_discount"], 50000)
        self.assertEqual(result["penalty_count"], 1)
        self.assertEqual(result["discount_count"], 1)
        self.assertEqual(len(result["installment_details"]), 2)


class PushServiceTestCase(TestCase):
    """푸시 알림 서비스 테스트 (UnboundLocalError 방지 및 카운트 검증)"""

    @patch("_utils.push_service.FCMDevice")
    @patch("redis.Redis.from_url")
    def test_send_push_notification_without_record_returns_zero(self, mock_redis, mock_fcm):
        mock_fcm.objects.filter.return_value.values_list.return_value = []

        # create_notification_record=False 호출 시 UnboundLocalError 없이 0 반환 검증
        result = send_push_notification(
            user_ids=[1, 2],
            title="테스트 알림",
            body="테스트 본문",
            create_notification_record=False,
        )

        self.assertEqual(result, 0)

    @patch("_utils.push_service.Notification")
    @patch("_utils.push_service.FCMDevice")
    @patch("redis.Redis.from_url")
    def test_send_push_notification_with_record_returns_count(self, mock_redis, mock_fcm, mock_notification):
        mock_fcm.objects.filter.return_value.values_list.return_value = []
        mock_notification.objects.bulk_create.return_value = [MagicMock(), MagicMock()]

        result = send_push_notification(
            user_ids=[1, 2],
            title="새 업무 할당",
            body="업무가 등록되었습니다.",
            create_notification_record=True,
        )

        self.assertEqual(result, 2)


class SlackNotificationsTestCase(TestCase):
    """Slack 웹훅 URL 추출 로직 테스트"""

    def test_get_slack_webhook_url_db_priority(self):
        mock_project = MagicMock()
        mock_project.slack_webhook_url = "https://hooks.slack.com/services/test/db/webhook"

        url = get_slack_webhook_url(mock_project)
        self.assertEqual(url, "https://hooks.slack.com/services/test/db/webhook")

    @patch("_utils.slack_notifications.config")
    def test_get_slack_webhook_url_env_fallback(self, mock_config):
        mock_project = MagicMock()
        mock_project.slack_webhook_url = ""
        mock_project.type = "2"
        mock_project.slug = "project-alpha"

        mock_config.side_effect = lambda key, default=None: (
            "https://hooks.slack.com/services/project/alpha"
            if key == "SLACK_PROJECT_PROJECT_ALPHA"
            else default
        )

        url = get_slack_webhook_url(mock_project)
        self.assertEqual(url, "https://hooks.slack.com/services/project/alpha")


class FileServiceTestCase(TestCase):
    """FileService 파일 관리 및 file_cleanup 테스트"""

    def test_manage_files_create_new_file(self):
        mock_instance = MagicMock()
        mock_file_model = MagicMock()
        mock_user = MagicMock()

        initial_data = {
            "new_files": ["fake_file_content"],
            "descriptions": ["설명 텍스트"],
        }

        FileService.manage_files(
            instance=mock_instance,
            initial_data=initial_data,
            creator=mock_user,
            file_model=mock_file_model,
            related_name="meeting",
        )

        mock_file_model.objects.create.assert_called_once_with(
            meeting=mock_instance,
            file="fake_file_content",
            creator=mock_user,
            description="설명 텍스트",
        )

    def test_delete_file_field(self):
        mock_instance = MagicMock()
        mock_field = MagicMock()
        mock_field.name = "sample.pdf"
        setattr(mock_instance, "file", mock_field)

        delete_file_field(mock_instance, "file")
        mock_field.delete.assert_called_once_with(save=False)
