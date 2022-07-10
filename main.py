from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import inspect, os, platform, time


def bot():
    # 필요한 변수 정의
    insta_id = input('인스타그램 아이디 : ')
    insta_pw = input('인스타그램 패스워드 : ')
    insta_tag = input('작업할 해시태그 : ')
    insta_cnt = int(input('작업횟수(숫자만) : '))
    insta_sort = input('0 : 인기게시물, 1 : 최근게시물')



    # 크롬드라이버 로딩
    options = webdriver.ChromeOptions()
    options.add_argument('--disable-gpu')
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36')

    current_folder = os.path.realpath(
        os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0]))

    if platform.system() == 'Windows':
        driver_path = os.path.join(current_folder, 'chromedriver.exe')
    else:
        driver_path = os.path.join(current_folder, 'chromedriver')

    driver = webdriver.Chrome(driver_path, options=options)
    driver.implicitly_wait(10)

    ### 인스타그램 자동 좋아요 작업 ###

    # 1. 인스타그램 로그인 페이지로 이동
    driver.get('https://www.instagram.com/?hl=ko')
    print('로그인중....')
    time.sleep(3)

    # 2. 아이디 입력창을 찾아서 위에서 입력받은 아이디(insta_id)값 입력
    id_input = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[1]/div/label')
    id_input.click()  # 입력창 클릭
    id_input.send_keys(insta_id)  # 아이디 입력

    # 2-1. 패스워드 입력창을 찾아서 위에서 입력받은 패스워드(insta_pw)값 입력
    pw_input = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[2]/div/label')
    pw_input.click()
    pw_input.send_keys(insta_pw)

    # 3. 로그인 버튼 클릭
    login_btn = driver.find_element_by_xpath('//*[@id="loginForm"]/div/div[3]/button')
    login_btn.click()

    # 3.1 백업 코드로 이동
    backup_code = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div[1]/div[2]/form/div[4]/button')
    backup_code.click()

    # 3.2 백업 코드 확인 후 입력
    code_input = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div[1]/div[2]/form/div[1]/div/label/input')
    code_input.click()
    code_input.send_keys(input('백업 코드를 입력하세요 : '))

    # 3.3 인증 완료 버튼 클릭
    ok_btn = driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/div/div[1]/div[2]/form/div[2]/button')
    ok_btn.click()

    time.sleep(10)

    # 4. 작업할 해시태그 검색 결과 페이지로 이동
    driver.get('https://www.instagram.com/explore/tags/{}/'.format(insta_tag))

    time.sleep(5)

    # 5. 인기게시물 혹은 최근게시물 첫번째 피드 선택
    if insta_sort == '0':
        # 인기게시물 첫번째 피트 선택
        hot_first_feed = driver.find_element_by_xpath(
            '//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div/div[2]')
        hot_first_feed.click()
    else:
        # 최근게시물 첫번째 피드 선택
        new_first_feed = driver.find_element_by_xpath(
            '/html/body/div[1]/div/div[1]/div/div[1]/div/div/div/div[1]/div[1]/section/main/article/div[2]/div/div[1]/div[1]')
        new_first_feed.click()

    time.sleep(1)

    # 6. 좋아요, 팔로우 작업 - 입력한 횟수만큼 반복 작업
    for idx in range(insta_cnt):
        xpath = "//article//section/span/button"
        like_btn = driver.find_elements_by_xpath(xpath)

        like_btn[0].click()  # 좋아요 클릭
        print('{}번째 피드 좋아요 작업 완료'.format(idx + 1))

        follow_btn = driver.find_element_by_xpath('//article//header//button')
        follow_btn_txt = driver.find_element_by_xpath('//article//header//button/div/div').text

        if follow_btn_txt == '팔로우':
            time.sleep(2)
            follow_btn.click()

            print('{}번째 피드 팔로우 성공'.format(idx + 1))
            time.sleep(5)  # 빠른 작업 방지를 위한 대기시간 설정
        elif follow_btn_txt == '팔로잉':
            print('이미 팔로우한 계정입니다.')


        # 너무 빠르게 작업을 할 경우 많은 양의 작업을 하게 되어 인스타그램측에서 계정 정지나 경고를 할 수 있으니
        # 작업과 다음 작업 사이의 속도를 조절하기 위해 20초 이상을 설정해주세요.
        time.sleep(5)

        # 7. 다음 피드로 이동
        if idx < insta_cnt:
            try:
                xpath = "//*[name()='svg'][@aria-label='다음']"
                svg_el = driver.find_element_by_xpath(xpath)
                svg_el.find_element_by_xpath("../../..").click()
            except NoSuchElementException as n:
                print('피드 개수 부족으로 작업이 종료됩니다.')
                break

    print('모든 작업 완료')
    driver.quit()


bot()
