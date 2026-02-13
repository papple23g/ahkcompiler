from django.test import TestCase, RequestFactory
from django.http import HttpResponse, HttpResponseRedirect
from myapp.views import homepage, ahk_webpage, version_uuid, rm, dl


class HomepageViewTest(TestCase):
    """測試首頁 view"""

    def setUp(self):
        self.factory = RequestFactory()

    def test_homepage_returns_200(self):
        """測試首頁回傳 HTTP 200"""
        request = self.factory.get('/')
        response = homepage(request)
        self.assertEqual(response.status_code, 200)

    def test_homepage_content(self):
        """測試首頁內容包含 'home page.'"""
        request = self.factory.get('/')
        response = homepage(request)
        self.assertIn(b'home page.', response.content)


class AhkWebpageViewTest(TestCase):
    """測試 AHK 網頁 view"""

    def setUp(self):
        self.factory = RequestFactory()

    def test_ahkblockly_returns_200(self):
        """測試 ahkblockly 頁面回傳 HTTP 200"""
        request = self.factory.get('/ahkblockly')
        response = ahk_webpage(request, subpage='ahkblockly')
        self.assertEqual(response.status_code, 200)

    def test_ahktool_returns_200(self):
        """測試 ahktool 頁面回傳 HTTP 200"""
        request = self.factory.get('/ahktool')
        response = ahk_webpage(request, subpage='ahktool')
        self.assertEqual(response.status_code, 200)

    def test_about_returns_200(self):
        """測試 about 頁面回傳 HTTP 200"""
        request = self.factory.get('/about')
        response = ahk_webpage(request, subpage='about')
        self.assertEqual(response.status_code, 200)

    def test_faq_returns_200(self):
        """測試 faq 頁面回傳 HTTP 200"""
        request = self.factory.get('/faq')
        response = ahk_webpage(request, subpage='faq')
        self.assertEqual(response.status_code, 200)

    def test_updateDiary_returns_200(self):
        """測試 updateDiary 頁面回傳 HTTP 200"""
        request = self.factory.get('/updateDiary')
        response = ahk_webpage(request, subpage='updateDiary')
        self.assertEqual(response.status_code, 200)


class VersionUuidTest(TestCase):
    """測試 version_uuid 輔助函數"""

    def test_valid_uuid4(self):
        """測試有效的 UUID v4 字串"""
        valid_uuid = 'a8098c1a-f86e-11da-bd1a-00112444be1e'
        result = version_uuid(valid_uuid)
        self.assertIsNotNone(result)

    def test_valid_uuid4_version(self):
        """測試 UUID v4 的版本號為 4"""
        import uuid
        test_uuid = str(uuid.uuid4())
        result = version_uuid(test_uuid)
        self.assertEqual(result, 4)

    def test_invalid_uuid_returns_none(self):
        """測試無效的 UUID 字串回傳 None"""
        result = version_uuid('not-a-valid-uuid')
        self.assertIsNone(result)

    def test_empty_string_returns_none(self):
        """測試空字串回傳 None"""
        result = version_uuid('')
        self.assertIsNone(result)

    def test_malicious_uuid_returns_none(self):
        """測試惡意字串回傳 None（安全性測試）"""
        result = version_uuid('../../../etc/passwd')
        self.assertIsNone(result)

    def test_sql_injection_returns_none(self):
        """測試 SQL 注入字串回傳 None（安全性測試）"""
        result = version_uuid("'; DROP TABLE users; --")
        self.assertIsNone(result)


class DlViewSecurityTest(TestCase):
    """測試下載 API 的安全性"""

    def setUp(self):
        self.factory = RequestFactory()

    def test_dl_invalid_uuid_redirects(self):
        """測試無效 UUID 的下載請求會被重導向"""
        request = self.factory.get('/dl', {'filename_key': 'invalid-uuid'})
        response = dl(request)
        self.assertIsInstance(response, HttpResponseRedirect)

    def test_dl_path_traversal_redirects(self):
        """測試路徑遍歷攻擊會被重導向"""
        request = self.factory.get('/dl', {'filename_key': '../../../etc/passwd'})
        response = dl(request)
        self.assertIsInstance(response, HttpResponseRedirect)


class RmViewSecurityTest(TestCase):
    """測試移除 API 的安全性"""

    def setUp(self):
        self.factory = RequestFactory()

    def test_rm_invalid_uuid_redirects(self):
        """測試無效 UUID 的移除請求會被重導向"""
        request = self.factory.get('/rm', {'filename_key': 'invalid-uuid'})
        response = rm(request)
        self.assertIsInstance(response, HttpResponseRedirect)

    def test_rm_path_traversal_redirects(self):
        """測試路徑遍歷攻擊會被重導向"""
        request = self.factory.get('/rm', {'filename_key': '../../../etc/passwd'})
        response = rm(request)
        self.assertIsInstance(response, HttpResponseRedirect)


class UrlRoutingTest(TestCase):
    """測試 URL 路由"""

    def test_homepage_url(self):
        """測試首頁 URL 可正常存取"""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_ahkblockly_url(self):
        """測試 ahkblockly URL 可正常存取"""
        response = self.client.get('/ahkblockly')
        self.assertEqual(response.status_code, 200)

    def test_ahktool_url(self):
        """測試 ahktool URL 可正常存取"""
        response = self.client.get('/ahktool')
        self.assertEqual(response.status_code, 200)

    def test_nonexistent_url_returns_404(self):
        """測試不存在的 URL 回傳 404"""
        response = self.client.get('/nonexistent-page-12345/')
        self.assertEqual(response.status_code, 404)
