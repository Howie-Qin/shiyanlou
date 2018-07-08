import json

from selenium import webdriver
from scrapy.http import HtmlResponse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#存取爬取的结果
results = []

#使用xpath解析评论数据
def parse(response):
    for comment in response.css('div.comment-list-item'):
        #解析的数据存入字典result，然后将result存入results
        result = dict(
                username=comment.xpath('.//a[@class="username"]/text()').extract_first().strip(),
                content=comment.xpath('.//div[contains(@class,"comment-item-content")]/p/text()').extract_first()
                )
        results.append(result)

#判断是否有下一页（此函数可有可无）
def has_next_page(response):
    classes = response.xpath('//li[contains(@class, "next-page")]/@class').extract_first()
    #classes = response.css('div.comment-box li.disabled.next-page').extract()
    print(classes)
    return 'disabled' not in classes
   # return not classes

#进入到下一页
#使用driver.find_element_by_xpath获得下一页数据
#模拟按钮的click()操作进入到下一页
def goto_next_page(driver):
    next_page_btn = driver.find_element_by_xpath('//li[contains(@class, "next-page")]')
    next_page_btn.click()

#等待页面加载完成
def wait_page_return(driver, page):
    WebDriverWait(driver, 20).until(
            EC.text_to_be_present_in_element(
                (By.XPATH, '//ul[@class="pagination"]/li[@class="active"]'),
                str(page)
            )
        )
#主函数
def spider():
    #创建PhantomJS的 webdriver
    driver = webdriver.PhantomJS()
    #获取第一个页面
    url = 'https://www.shiyanlou.com/courses/427'
    driver.get(url)
    page = 1
    while True:
        #加载评论的第一页
        wait_page_return(driver, page)
        #获取页面源码
        html = driver.page_source
        #构建HtmlResponse对象获取评论数据
        response = HtmlResponse(url=url, body=html.encode('utf8'))
        #解析 HtmlResponse 对象获取评论数据
        parse(response)
        print('--------------', page)
        #如果是最后一页则停止爬取
        if not has_next_page(response):
        #if response.css('div.comment-box li.disabled.next-page'):
            break
        page +=1
        goto_next_page(driver)
    #将results使用json序列化后写入文件
    with open('comments.json', 'w') as f:
        f.write(json.dumps(results))

if __name__ == '__main__':
    spider()



