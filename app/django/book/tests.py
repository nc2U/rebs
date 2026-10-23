from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.urls import reverse

from .models import Book, Subject, Image

User = get_user_model()


class BookModelTestCase(TestCase):
    """Book 및 Subject 모델 메서드 단위 테스트"""

    def setUp(self):
        self.user = User.objects.create_user(username='bookuser', email='bookuser@example.com', password='password123')
        self.book = Book.objects.create(
            title='파이썬 코딩의 기술',
            disclosure=True,
            author='브렛 슬라킨',
            publisher='길벗',
            description='파이썬 실력을 키우는 90가지 기술',
            creator=self.user,
        )
        self.subject1 = Subject.objects.create(
            book=self.book,
            seq=1,
            title='제1장 파이썬답게 생각하기',
            level=1,
            content='### 1장 내용 요약',
            creator=self.user,
        )
        self.subject2 = Subject.objects.create(
            book=self.book,
            seq=2,
            title='아이템 1: 사용 중인 파이썬의 버전을 알아두라',
            level=2,
            content='python --version 명령어를 사용하자.',
            creator=self.user,
        )

    def test_book_str_representation(self):
        """도서 문자열 표현이 제목을 정상 반환하는지 검증"""
        self.assertEqual(str(self.book), '파이썬 코딩의 기술')

    def test_subject_str_and_absolute_url(self):
        """단원 문자열 표현 및 절대 URL 반환 검증"""
        self.assertEqual(str(self.subject1), '제1장 파이썬답게 생각하기')
        expected_url = reverse('book:subject_detail', args=[self.book.id, self.subject1.pk])
        self.assertEqual(self.subject1.get_absolute_url(), expected_url)

    def test_subject_prev_and_next_post(self):
        """단원 간 이전/다음 포스트 탐색 검증"""
        self.assertIsNone(self.subject1.get_previous_post())
        self.assertEqual(self.subject1.get_next_post(), self.subject2)

        self.assertEqual(self.subject2.get_previous_post(), self.subject1)
        self.assertIsNone(self.subject2.get_next_post())


class BooksViewTestCase(TestCase):
    """도서 CRUD 뷰 통합 테스트"""

    def setUp(self):
        self.user = User.objects.create_user(username='tester', email='tester@example.com', password='password123')
        self.book = Book.objects.create(
            title='Django 디자인 패턴',
            disclosure=True,
            author='아룬 라빈드란',
            publisher='에이콘',
            description='Django 웹 개발 베스트 프랙티스',
            creator=self.user,
        )

    def test_unauthenticated_user_redirects_to_login(self):
        """비로그인 사용자가 도서 목록 접근 시 로그인 페이지로 리다이렉트되는지 검증"""
        res = self.client.get(reverse('book:index'))
        self.assertEqual(res.status_code, 302)
        self.assertIn('/accounts/login/', res.url)

    def test_books_list_and_search_filter(self):
        """로그인 사용자의 도서 목록 조회 및 q 파라미터 검색 필터링 검증"""
        self.client.force_login(self.user)

        # 1. 전체 목록 조회
        res = self.client.get(reverse('book:index'))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Django 디자인 패턴')

        # 2. 검색어 일치
        res_search = self.client.get(reverse('book:index'), {'q': '디자인'})
        self.assertEqual(res_search.status_code, 200)
        self.assertEqual(len(res_search.context['object_list']), 1)

        # 3. 검색어 불일치
        res_none = self.client.get(reverse('book:index'), {'q': '존재하지않는책'})
        self.assertEqual(res_none.status_code, 200)
        self.assertEqual(len(res_none.context['object_list']), 0)

    def test_books_detail_view(self):
        """도서 상세 페이지 정상 렌더링 검증"""
        self.client.force_login(self.user)
        res = self.client.get(reverse('book:detail', args=[self.book.id]))
        self.assertEqual(res.status_code, 200)
        self.assertContains(res, 'Django 웹 개발 베스트 프랙티스')

    def test_books_create_view(self):
        """새 도서 등록 시 creator가 요청 유저로 자동 저장되는지 검증"""
        self.client.force_login(self.user)
        payload = {
            'title': '클린 아키텍처',
            'disclosure': True,
            'author': '로버트 마틴',
            'publisher': '인사이트',
            'description': '소프트웨어 구조와 설계의 원칙',
        }
        res = self.client.post(reverse('book:add'), payload)
        self.assertEqual(res.status_code, 302)
        new_book = Book.objects.get(title='클린 아키텍처')
        self.assertRedirects(res, reverse('book:detail', args=[new_book.id]))
        self.assertEqual(new_book.creator, self.user)

    def test_books_update_view(self):
        """도서 정보 수정 검증"""
        self.client.force_login(self.user)
        payload = {
            'title': 'Django 디자인 패턴 (개정판)',
            'disclosure': True,
            'author': '아룬 라빈드란',
            'publisher': '에이콘출판',
            'description': '수정된 설명글',
        }
        res = self.client.post(reverse('book:edit', args=[self.book.id]), payload)
        self.assertEqual(res.status_code, 302)
        self.book.refresh_from_db()
        self.assertEqual(self.book.title, 'Django 디자인 패턴 (개정판)')
        self.assertEqual(self.book.description, '수정된 설명글')

    def test_books_delete_view(self):
        """도서 삭제 시 index 페이지로 리다이렉트되고 DB에서 삭제되는지 검증"""
        self.client.force_login(self.user)
        res = self.client.post(reverse('book:delete', args=[self.book.id]))
        self.assertEqual(res.status_code, 302)
        self.assertRedirects(res, reverse('book:index'))
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())


class SubjectsViewTestCase(TestCase):
    """단원(Subject) CRUD, 이미지 폼셋 및 템플릿 연동 테스트"""

    def setUp(self):
        self.user = User.objects.create_user(username='author', email='author@example.com', password='password123')
        self.book = Book.objects.create(
            title='Vue.js 완벽 가이드',
            disclosure=True,
            author='Evan You',
            publisher='길벗',
            creator=self.user,
        )
        self.subject1 = Subject.objects.create(
            book=self.book,
            seq=1,
            title='1장 Vue 핵심 문법',
            level=1,
            content='### Vue 3 Composition API',
            creator=self.user,
        )
        self.subject2 = Subject.objects.create(
            book=self.book,
            seq=2,
            title='2장 반응형 상태 관리',
            level=2,
            content='### ref and reactive',
            creator=self.user,
        )

    def test_subjects_index_and_detail_views(self):
        """단원 인덱스 및 상세 페이지 조회와 브레드크럼 검증"""
        self.client.force_login(self.user)

        # 1. 단원 인덱스 (첫 번째 단원 렌더링)
        res_idx = self.client.get(reverse('book:subject_index', args=[self.book.id]))
        self.assertEqual(res_idx.status_code, 200)
        self.assertContains(res_idx, '1장 Vue 핵심 문법')
        self.assertEqual(res_idx.context['total'], 2)

        # 2. 단원 상세
        res_det = self.client.get(reverse('book:subject_detail', args=[self.book.id, self.subject2.id]))
        self.assertEqual(res_det.status_code, 200)
        self.assertContains(res_det, '2장 반응형 상태 관리')
        # 브레드크럼 생성 검증
        breadcrumb = res_det.context['breadcrumb']
        self.assertTrue(len(breadcrumb) >= 2)
        # 현재 활성 페이지(레벨 2)의 속성 검증
        self.assertIn('aria-current=page', breadcrumb[-1]['cls2'])

    def test_invalid_book_id_returns_404(self):
        """존재하지 않는 도서 ID 접근 시 500이 아닌 404를 반환하는지 검증"""
        self.client.force_login(self.user)
        res = self.client.get(reverse('book:subject_index', args=[99999]))
        self.assertEqual(res.status_code, 404)

        res_det = self.client.get(reverse('book:subject_detail', args=[99999, 1]))
        self.assertEqual(res_det.status_code, 404)

    def test_subjects_create_with_image_formset_and_seq_auto_increment(self):
        """단원 생성 시 Max('seq') + 1 순번 부여 및 ImageFormSet 첨부파일이 정상 저장되는지 검증"""
        self.client.force_login(self.user)

        small_gif = (
            b'\x47\x49\x46\x38\x39\x61\x01\x00\x01\x00\x80\x00\x00'
            b'\xff\xff\xff\x00\x00\x00\x21\xf9\x04\x01\x00\x00\x00'
            b'\x00\x2c\x00\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02'
            b'\x44\x01\x00\x3b'
        )
        img_file = SimpleUploadedFile('test_chart.gif', small_gif, content_type='image/gif')

        payload = {
            'title': '3장 Pinia 스토어',
            'level': 2,
            'content': '### Pinia 스토어 구조 다이어그램',
            # ImageFormSet management form fields
            'image_set-TOTAL_FORMS': '1',
            'image_set-INITIAL_FORMS': '0',
            'image_set-MIN_NUM_FORMS': '0',
            'image_set-MAX_NUM_FORMS': '1000',
            'image_set-0-image': img_file,
        }

        res = self.client.post(reverse('book:subject_add', args=[self.book.id]), payload)
        self.assertEqual(res.status_code, 302)

        new_subject = Subject.objects.get(title='3장 Pinia 스토어')
        # seq가 기존 최대값(2) + 1 = 3 으로 안전하게 채번되었는지 검증
        self.assertEqual(new_subject.seq, 3)
        self.assertEqual(new_subject.creator, self.user)

        # 이미지 폼셋 저장이 정상 동작하여 Image 레코드가 생성되었는지 검증
        images = Image.objects.filter(subject=new_subject)
        self.assertEqual(images.count(), 1)
        self.assertTrue(images.first().image.name.endswith('.gif'))
        self.assertTrue(images.first().image.storage.exists(images.first().image.name))
        images.first().image.delete(save=False)

    def test_subjects_update_preserves_creator_and_saves_image(self):
        """단원 수정 시 기존 creator가 보존되고 이미지 폼셋이 정상 저장되는지 검증"""
        editor = User.objects.create_user(username='editor', email='editor@example.com', password='password123')
        self.client.force_login(editor)

        payload = {
            'title': '1장 Vue 핵심 문법 (수정됨)',
            'level': 1,
            'content': '### 업데이트된 Vue 3 내용',
            'image_set-TOTAL_FORMS': '0',
            'image_set-INITIAL_FORMS': '0',
            'image_set-MIN_NUM_FORMS': '0',
            'image_set-MAX_NUM_FORMS': '1000',
        }
        res = self.client.post(reverse('book:subject_edit', args=[self.book.id, self.subject1.id]), payload)
        self.assertEqual(res.status_code, 302)

        self.subject1.refresh_from_db()
        self.assertEqual(self.subject1.title, '1장 Vue 핵심 문법 (수정됨)')
        # 작성자(creator)가 수정자로 덮어씌워지지 않고 원작성자(author)로 유지되는지 검증
        self.assertEqual(self.subject1.creator, self.user)

    def test_subjects_delete_view_renders_confirm_and_deletes_successfully(self):
        """단원 삭제 확인 화면 정상 렌더링 및 POST 삭제 후 subject_index 리다이렉트 검증"""
        self.client.force_login(self.user)

        # 1. 삭제 확인 GET 요청 시 subject_confirm_delete.html 폼이 노출되는지 검증
        delete_url = reverse('book:subject_delete', args=[self.book.id, self.subject2.id])
        res_get = self.client.get(delete_url)
        self.assertEqual(res_get.status_code, 200)
        self.assertContains(res_get, '단원 삭제 확인')
        self.assertContains(res_get, '2장 반응형 상태 관리')

        # 2. 삭제 POST 요청 시 get_success_url()에 의해 subject_index로 리다이렉트되고 DB 삭제 검증
        res_post = self.client.post(delete_url)
        self.assertEqual(res_post.status_code, 302)
        self.assertRedirects(res_post, reverse('book:subject_index', args=[self.book.id]))
        self.assertFalse(Subject.objects.filter(id=self.subject2.id).exists())
