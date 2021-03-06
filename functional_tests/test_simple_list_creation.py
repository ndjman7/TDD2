import time
from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class NewVisitorTest(FunctionalTest):

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Pando는 멋진 To-Do List 온라인 앱이 나왔다는 소식을 듣고
        # 해당 웹사이트를 확인하러 간다
        self.browser.get(self.live_server_url)

        # 웹 페이지 타이틀과 헤더가 'To-Do'를 표시하고 있다
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # Pando는 바로 To-Do를 추가하기로 한다
        inputbox = self.get_item_input_box()
        self.assertEqual(
                inputbox.get_attribute('placeholder'),
                'Enter a to-do item'
        )

        # "운동 하기"라고 텍스트 상자에 입력한다
        # (Pando의 일과는 운동을 하는 것이다)
        inputbox.send_keys('운동 하기')

        # 엔터키를 치면 페이지가 갱신되고 작업 목록에
        # "1: 운동 하기" 아이템이 추가된다
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        self.wait_for_row_in_list_table('1: 운동 하기')

        # 추가 아이템을 입력할 수 있는 여분의 텍스트 상자가 존재한다
        # 다시 "운동 후 단백질 섭취하기"라고 입력한다
        inputbox = self.get_item_input_box()
        inputbox.send_keys('운동 후 단백질 섭취하기')
        inputbox.send_keys(Keys.ENTER)

        # 페이지는 다시 갱신되고, 두 개 아이템이 목록에 보인다
        self.wait_for_row_in_list_table('2: 운동 후 단백질 섭취하기')
        self.wait_for_row_in_list_table('1: 운동 하기')

        # Pando는 사이트가 입력한 목록을 저장하고 있는지 궁금하다
        # 사이트는 Pando를 위한 특정 URL을 생성해준다
        # 이때 URL에 대한 설명도 함께 제공된다

        # 만족하고 잠자리에 든다

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # Pando는 새로운 To-Do 리스트를 시작한다.
        self. browser.get(self.live_server_url)
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy peacock feathers')

        # Pando는 고유의 URL을 가지고 있다
        pando_list_url = self.browser.current_url
        self.assertRegex(pando_list_url, '/lists/.+')

        # 이제 새로운 유저, Ra가 사이트로 온다
        ## 우리는 정보가 없는 새로운 브라우저 세션을 사용한다
        ##  Pando의 쿠키가 없어야 한다
        self.browser.quit()
        self.browser = webdriver.Chrome()

        # Ra가 사이트에 방문한다. Pando의 리스트가 없다
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)

        # Ra는 새로운 아이템을 리스트에 추가한다
        # 그는 Pando보다 노잼
        inputbox = self.get_item_input_box()
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: Buy milk')

        # Ra는 고유 URL을 가진다
        ra_list_url = self.browser.current_url
        self.assertRegex(ra_list_url, '/lists/.+')
        self.assertNotEqual(ra_list_url, pando_list_url)

        # 다시 Pando의 흔적은 없다
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)

        # 만족하고 같이 자러간다

