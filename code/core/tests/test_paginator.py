from django.test import TestCase
from core.paginator import Paginator, page_range_short


class PaginatorTestCase(TestCase):

    def test_pagination_default(self):
        pass

    def test_pagination_first_page(self):
        meta_dict = {"skip": 0, "limit": 10, "total": 100}
        p = Paginator(meta_dict)
        self.assertEquals(p.total, 100)
        self.assertEquals(p.pages, 10)
        self.assertEquals(p.has_previous(), False)
        self.assertEquals(p.has_next(), True)
        self.assertEquals(p.page(), 1)
        self.assertEquals(p.page_display(), "1 to 10 of 100")
        self.assertEquals(p.prev(), 1)
        self.assertEquals(p.next(), 2)

    def test_pagination_last_page_even(self):
        meta_dict = {"skip": 90, "limit": 10, "total": 100}
        p = Paginator(meta_dict)
        self.assertEquals(p.total, 100)
        self.assertEquals(p.pages, 10)
        self.assertEquals(p.has_previous(), True)
        self.assertEquals(p.has_next(), False)
        self.assertEquals(p.page(), 10)
        self.assertEquals(p.page_display(), "91 to 100 of 100")
        self.assertEquals(p.prev(), 9)
        self.assertEquals(p.next(), 10)

    def test_pagination_last_page_mod1(self):
        meta_dict = {"skip": 100, "limit": 10, "total": 101}
        p = Paginator(meta_dict)
        self.assertEquals(p.total, 101)
        self.assertEquals(p.pages, 11)
        self.assertEquals(p.has_previous(), True)
        self.assertEquals(p.has_next(), False)
        self.assertEquals(p.page(), 11)
        self.assertEquals(p.page_display(), "101 to 101 of 101")
        self.assertEquals(p.prev(), 10)
        self.assertEquals(p.next(), 11)

    def test_pagination_gt_5000(self):
        meta_dict = {"skip": 4999, "limit": 10, "total": 5001}
        p = Paginator(meta_dict)
        self.assertEquals(p.total, 5000)
        self.assertEquals(p.pages, 500)
        self.assertEquals(p.has_previous(), True)
        self.assertEquals(p.has_next(), False)
        self.assertEquals(p.page(), 500)
        self.assertEquals(p.page_display(), "5000 to 5000 of 5000")
        self.assertEquals(p.prev(), 499)
        self.assertEquals(p.next(), 500)

    def test_page_range_short(self):
        meta_dict = {"skip": 0, "limit": 10, "total": 100}
        p = Paginator(meta_dict)
        page_range = list(page_range_short(p))
        self.assertEquals(page_range, [1, 2, 3, '...', 8, 9, 10])
