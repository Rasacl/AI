import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException

def get_pharmacy_data():
    driver = None
    try:
        print('正在初始化浏览器...')
        # 设置Chrome选项
        chrome_options = Options()
        chrome_options.add_argument('--start-maximized')  # 最大化窗口
        chrome_options.add_argument('--disable-gpu')  # 禁用GPU加速
        chrome_options.add_argument('--no-sandbox')  # 禁用沙箱模式
        chrome_options.add_argument('--disable-dev-shm-usage')  # 禁用/dev/shm使用
        chrome_options.add_argument('--disable-extensions')  # 禁用扩展
        chrome_options.add_argument('--disable-software-rasterizer')  # 禁用软件光栅化
        chrome_options.page_load_strategy = 'eager'  # 设置页面加载策略
        
        print('正在创建Chrome实例...')
        # 创建Chrome浏览器实例，设置超时和性能优化
        driver = webdriver.Chrome(options=chrome_options)
        driver.set_page_load_timeout(60)  # 增加页面加载超时时间
        driver.set_script_timeout(60)  # 增加脚本执行超时时间
        driver.implicitly_wait(10)  # 设置隐式等待时间
        
        # 设置窗口大小为最大化
        driver.maximize_window()
        
        print('正在访问网页...')
        # 访问网页
        driver.get('https://fuwu.nhsa.gov.cn/nationalHallSt/#/search/pharmacies')
        
        print('等待页面加载并点击定点零售药店查询...')
        # 等待并点击定点零售药店查询链接
        try:
            pharmacy_link = WebDriverWait(driver, 30).until(
                EC.element_to_be_clickable((By.XPATH, "//div[contains(@class, 'menu-wrapper')]//span[contains(text(), '定点零售药店查询')]"))
            )
            driver.execute_script("arguments[0].click();", pharmacy_link)
            print('已点击定点零售药店查询')
            time.sleep(2)  # 等待页面跳转
        except TimeoutException:
            print('错误：未找到定点零售药店查询链接，请检查网页结构')
            return []
        except Exception as e:
            print(f'点击定点零售药店查询链接时出错: {str(e)}')
            return []
            
        print('等待页面加载...')
        # 等待页面加载
        try:
            # 等待页面完全加载
            WebDriverWait(driver, 30).until(
                lambda d: d.execute_script('return document.readyState') == 'complete'
            )
            # 等待输入框出现
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'el-input__inner'))
            )
            print('页面加载完成')
        except TimeoutException:
            print('错误：页面加载超时，请检查网络连接')
            return []
        except Exception as e:
            print(f'页面加载出错: {str(e)}')
            return []
        
        print('选择所在地：浙江省...')
        # 点击所在地下拉框
        try:
            # 等待并点击所在地下拉框
            location_dropdown = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.CLASS_NAME, 'el-input__inner'))
            )
            driver.execute_script("arguments[0].click();", location_dropdown)
            print('已点击所在地下拉框')
            time.sleep(2)  # 等待下拉框展开
            
            # 选择浙江省
            print('正在选择浙江省...')
            zhejiang_xpath = "//span[contains(text(),'浙江省')]"
            zhejiang = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, zhejiang_xpath))
            )
            # 先hover浙江省以显示城市列表
            actions = webdriver.ActionChains(driver)
            actions.move_to_element(zhejiang).perform()
            print('已hover浙江省')
            time.sleep(1)  # 等待城市列表显示
            
            # 点击浙江省
            # driver.execute_script("arguments[0].click();", zhejiang)
            print('已选择浙江省')
            time.sleep(1)  # 等待选择生效
            
            # 选择杭州市
            print('正在选择杭州市...')
            hangzhou_xpath = "//span[contains(text(),'杭州市')]"
            hangzhou = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, hangzhou_xpath))
            )
            driver.execute_script("arguments[0].click();", hangzhou)
            print('已选择杭州市')
            time.sleep(1)  # 等待选择生效

            # 选择每页显示100条数据
            print('正在设置每页显示100条数据...')
            try:
                # 点击页码选择框中的span元素
                page_size_span = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//span[contains(@class, 'el-pagination__sizes')]//span"))
                )
                driver.execute_script("arguments[0].click();", page_size_span)
                print('已点击页码选择框')
                time.sleep(1)  # 等待下拉框展开

                # 选择100条/页
                page_size_100 = WebDriverWait(driver, 20).until(
                    EC.element_to_be_clickable((By.XPATH, "//li[contains(@class, 'el-select-dropdown__item')]//span[text()='100条/页']"))
                )
                driver.execute_script("arguments[0].click();", page_size_100)
                print('已选择每页显示100条')
                time.sleep(1)  # 等待选择生效
            except TimeoutException as e:
                print(f'错误：设置每页显示条数超时: {str(e)}')
                return []
            except Exception as e:
                print(f'错误：设置每页显示条数失败: {str(e)}')
                return []

        except TimeoutException as e:
            print(f'错误：选择地区超时: {str(e)}')
            return []
        except Exception as e:
            print(f'错误：选择地区失败: {str(e)}')
            return []
            
        print('点击查询按钮...')
        # 点击查询按钮
        try:
            search_button = WebDriverWait(driver, 20).until(
                EC.element_to_be_clickable((By.XPATH, "//button//span[contains(text(),'查询')]")))
            driver.execute_script("arguments[0].click();", search_button)
            print('已点击查询按钮')

            # 等待数据加载
            print('等待数据加载...')
            try:
                # 等待表格加载完成
                WebDriverWait(driver, 30).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'el-table'))
                )
                print('表格已加载')
                time.sleep(3)  # 等待数据填充
            except TimeoutException:
                print('错误：数据加载超时')
                return []
            except Exception as e:
                print(f'错误：数据加载失败: {str(e)}')
                return []
            
            # 存储所有药店数据
            pharmacy_data = []
            page_num = 1
            retry_count = 0
            max_retries = 3
            
            while True:
                print(f'正在获取第 {page_num} 页数据...')
                try:
                    # 等待表格行加载完成
                    rows = WebDriverWait(driver, 20).until(
                        EC.presence_of_all_elements_located((By.CLASS_NAME, 'el-table__row'))
                    )
                    time.sleep(2)  # 等待数据稳定
                    
                    if not rows:
                        if retry_count < max_retries:
                            print(f'警告：当前页面未找到数据，第 {retry_count + 1} 次重试...')
                            retry_count += 1
                            time.sleep(3)
                            continue
                        else:
                            print('警告：多次重试后仍未找到数据，停止获取')
                            break
                    
                    retry_count = 0  # 重置重试计数
                    
                    # 获取当前页面的药店信息
                    page_data = []
                    for element in rows:
                        try:
                            # 首先点击箭头展开详细信息
                            try:
                                arrow = element.find_element(By.CSS_SELECTOR, '.el-table__expand-icon')
                                driver.execute_script("arguments[0].click();", arrow)
                                time.sleep(1)  # 等待详细信息加载
                            except Exception as e:
                                print(f'点击展开箭头时出错: {str(e)}')
                                continue

                            # 获取基本信息
                            name = element.find_element(By.CSS_SELECTOR, 'td:nth-child(3)').text.strip()
                            address = element.find_element(By.CSS_SELECTOR, 'td:nth-child(4)').text.strip()

                            # 获取展开后的详细信息
                            try:
                                expanded_row = WebDriverWait(driver, 10).until(
                                    EC.presence_of_element_located((By.CSS_SELECTOR, '.el-table__expanded-cell'))
                                )
                                
                                # 获取医保便民服务状态
                                medical_services = []
                                form = expanded_row.find_element(By.CSS_SELECTOR, '.el-form.table-expand')
                                service_elements = form.find_elements(By.CSS_SELECTOR, '.el-form-item__content div')
                                for element in service_elements:
                                    service_name = element.text.strip()
                                    service_status = ''
                                    class_attr = element.get_attribute('class')
                                    if 'round-gray' in class_attr:
                                        service_status = '未开通'
                                    elif 'round-green' in class_attr:
                                        service_status = '已开通'
                                    elif 'round-red' in class_attr:
                                        service_status = '业务开通但近7天未产生业务数据'
                                    if service_name and service_status:
                                        medical_services.append(f'{service_name}_{service_status}')
                                
                                # 获取机构编码
                                try:
                                    form_items = form.find_elements(By.CSS_SELECTOR, '.el-form-item')
                                    institution_code = form_items[2].find_element(By.CSS_SELECTOR, '.el-form-item__content span').text.strip()
                                except:
                                    institution_code = '未找到机构编码'
                                
                                # 获取经营范围
                                try:
                                    business_scope = form_items[3].find_element(By.CSS_SELECTOR, '.el-form-item__content span').text.strip()
                                except:
                                    business_scope = '未找到经营范围'
                                
                                # 获取异地就医服务
                                try:
                                    remote_medical = form_items[4].find_element(By.CSS_SELECTOR, '.el-form-item__content span').text.strip()
                                except:
                                    remote_medical = '未找到异地就医服务信息'
                                
                                # 组合所有详细信息
                                details = {
                                    '医保便民服务': medical_services,
                                    '机构编码': institution_code,
                                    '经营范围': business_scope,
                                    '异地就医服务': remote_medical
                                }
                                
                                # 再次点击箭头关闭详细信息
                                driver.execute_script("arguments[0].click();", arrow)
                                time.sleep(0.5)  # 等待关闭动画完成
                            except Exception as e:
                                print(f'获取详细信息时出错: {str(e)}')
                                details = ''

                            if name and address:  # 只添加非空数据
                                page_data.append({
                                    '药店名称': name,
                                    '详细地址': address,
                                    '医保便民服务': '\n'.join(details['医保便民服务']),
                                    '机构编码': details['机构编码'],
                                    '经营范围': details['经营范围'],
                                    '异地就医服务': details['异地就医服务']
                                })
                        except Exception as e:
                            print(f'获取药店信息时出错: {str(e)}')
                            continue
                    
                    if page_data:
                        pharmacy_data.extend(page_data)
                        print(f'第 {page_num} 页成功获取 {len(page_data)} 条数据，总计 {len(pharmacy_data)} 条')
                    else:
                        print(f'警告：第 {page_num} 页未获取到有效数据')
                    
                    # 检查当前页码和是否有下一页
                    try:
                        # 获取当前页码
                        current_page = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, '.el-pager li.active'))
                        ).text
                        print(f'当前页码：{current_page}')
                        
                        # 如果已经到达第44页，停止获取
                        if int(current_page) >= 44:
                            print('已到达最后一页(第44页)')
                            break
                            
                        next_button = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'btn-next'))
                        )
                        if 'disabled' in next_button.get_attribute('class'):
                            print('已到达最后一页')
                            break
                        
                        # 使用JavaScript点击下一页按钮
                        driver.execute_script("arguments[0].click();", next_button)
                        print('正在加载下一页...')
                        time.sleep(3)  # 等待页面切换
                        page_num += 1
                    except TimeoutException:
                        print('警告：未找到下一页按钮，可能已是最后一页')
                        break
                    except Exception as e:
                        print(f'翻页时出错: {str(e)}')
                        if retry_count < max_retries:
                            print(f'第 {retry_count + 1} 次重试翻页...')
                            retry_count += 1
                            time.sleep(3)
                            continue
                        else:
                            print('多次重试翻页失败，停止获取')
                            break
                except TimeoutException:
                    print(f'错误：第 {page_num} 页数据加载超时')
                    if retry_count < max_retries:
                        print(f'第 {retry_count + 1} 次重试加载...')
                        retry_count += 1
                        time.sleep(3)
                        continue
                    else:
                        print('多次重试后仍然超时，停止获取')
                        break
                except Exception as e:
                    print(f'获取第 {page_num} 页数据时出错: {str(e)}')
                    if retry_count < max_retries:
                        print(f'第 {retry_count + 1} 次重试...')
                        retry_count += 1
                        time.sleep(3)
                        continue
                    else:
                        print('多次重试失败，停止获取')
                        break

        except WebDriverException as e:
            print('='*50)
            print('浏览器驱动错误:')
            print(f'错误信息: {str(e)}')
            print('可能的原因:')
            print('1. Chrome浏览器未安装')
            print('2. ChromeDriver未安装或版本与Chrome不匹配')
            print('3. ChromeDriver未添加到系统环境变量')
            print('解决方案:')
            print('1. 安装最新版Chrome浏览器')
            print('2. 下载对应版本的ChromeDriver并添加到环境变量')
            print('3. 重启电脑后重试')
            print('='*50)
            return []
    except Exception as e:
        print('='*50)
        print('发生未知错误:')
        print(f'错误信息: {str(e)}')
        print('建议:')
        print('1. 检查网络连接')
        print('2. 确保系统资源充足')
        print('3. 稍后重试')
        print('='*50)
        return []
    
    finally:
        if driver:
            print('正在关闭浏览器...')
            try:
                driver.quit()
                print('浏览器已关闭')
            except Exception as e:
                print('关闭浏览器时出错:')
                print(f'错误信息: {str(e)}')
                print('请手动关闭浏览器窗口')
        return pharmacy_data

def main():
    try:
        print('='*50)
        print('开始获取药店数据...')
        print('注意事项:')
        print('1. 请确保网络连接稳定')
        print('2. 请勿关闭或最小化浏览器窗口')
        print('3. 程序运行期间请勿操作浏览器')
        print('='*50)
        
        # 获取药店数据
        pharmacy_data = get_pharmacy_data()
        if not pharmacy_data:
            print('='*50)
            print('未获取到任何数据')
            print('建议:')
            print('1. 检查网络连接后重试')
            print('2. 确认网站是否正常访问')
            print('='*50)
            return
        
        print('='*50)
        print('正在保存数据到Excel...')
        # 创建DataFrame
        df = pd.DataFrame(pharmacy_data)
        
        # 保存为Excel文件
        output_file = 'd:/project/self/AI/杭州市定点零售药店.xlsx'
        df.to_excel(output_file, index=False)
        print('数据保存成功!')
        print(f'保存位置: {output_file}')
        print(f'数据总量: {len(pharmacy_data)} 条')
        print('='*50)
        
    except Exception as e:
        print('='*50)
        print('保存数据时出错:')
        print(f'错误信息: {str(e)}')
        print('建议:')
        print('1. 确保Excel文件未被其他程序占用')
        print('2. 检查磁盘空间是否充足')
        print('3. 确保有写入权限')
        print('='*50)

if __name__ == '__main__':
    main()