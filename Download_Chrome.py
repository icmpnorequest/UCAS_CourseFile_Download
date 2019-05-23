# coding=utf8
"""
@author: Yantong Lai
@date: 2019.5.5

MIT License

Copyright (c) 2019 Yantong Lai

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

from bs4 import BeautifulSoup
import os
import shutil
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

index_url = "http://onestop.ucas.edu.cn/"
Download_path = "Download"
Dir_str = "项"


def login():
    """
    It is a function to log in the UCAS onestop system.
    """
    try:
        print("1. Login.\n")
        # Wait for login.
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "neirong")))
        # Send username and password to log in.
        input_user = browser.find_element_by_id("menhuusername")
        input_user.send_keys(username)
        input_pwd = browser.find_element_by_id("menhupassword")
        input_pwd.send_keys(password)
        input_pwd.send_keys(Keys.ENTER)
    except Exception as e:
        print(e)

def gotoCourseWeb():
    """
    It is a function to go to 'Course Website'.
    """
    try:
        print("2. Go to Course Website.\n")
        course_web = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@href='/portal/site/16/801']")))
        course_web.click()

        # 2.1 Go to 'My Course'.
        my_course = wait.until(EC.element_to_be_clickable((By.XPATH,'//*[@id="toolMenu"]/ul/li[4]/a')))
        my_course.click()
    except Exception as e:
        print(e)

def listAllCourse():
    """
    It is a function to list all the courses.
    """
    try:
        print("3. List all the courses.\n")
        # Wait for loading.
        wait.until(EC.presence_of_element_located((By.ID, "worksite")))
        soup = BeautifulSoup(browser.page_source, features="lxml")
        allcourses = soup.find_all("th", {"headers":"worksite"})

        AllCoursesName = []
        AllCoursesUrl = []
        for item in allcourses:
            course_url = item.a.get("href")
            AllCoursesUrl.append(course_url)
            course_name = item.a.text
            AllCoursesName.append(course_name)
        AllCoursesIndex = list(range(len(AllCoursesName)))
        AllCoursesVal = zip(AllCoursesName, AllCoursesUrl)
        AllCoursesDict = dict(zip(AllCoursesIndex, AllCoursesVal))
        return AllCoursesDict
    except Exception as e:
        print(e)

def chooseCourse(CourseIdx):
    """
    It is a function to choose Course and go to that couse..
    :param CourseIdx:
    """
    try:
        print("4. Choose course and go to that course.\n")
        # Open a new tab
        browser.execute_script("window.open('');")
        browser.switch_to.window(window_name=browser.window_handles[1])
        browser.get(AllCourses[CourseIdx][1])
        browser.implicitly_wait(5)

        courseID = AllCourses[CourseIdx][1].split("/")[-1]

        # Click My Resource
        courseSrc = browser.find_element_by_xpath('//*[@id="toolMenu"]/ul/li[5]/a')
        courseSrc.click()
        browser.implicitly_wait(5)

        soup = BeautifulSoup(browser.page_source, features="lxml")
        FileItems = soup.find_all("span", {"class": "hidden-sm hidden-xs"})

        # Create the Course Directory at the Download_path
        course_path = Download_path + "/" + AllCourses[CourseIdx][0]
        if not os.path.exists(course_path):
            os.mkdir(course_path)
            print("Create %s dir successfully.\n" %course_path)

        FileLists = []
        for item in FileItems:
            FileLists.append(item.text)

        FileLists.pop(0)
        FileListsIdx = range(len(FileLists))
        FileDict = dict(zip(FileListsIdx, FileLists))
        print("Sources list is as follow: \n")
        return FileDict

        # If only file in the FileLists, download all the files.
        # If there are some directories in FileLists, input the index of specific directory and download
    except Exception as e:
        print(e)

def checkDir(srcIndex):
    """
    It is a function to check whether it's a directory or file.
    :return: If it's a dir, return 1; else return 0
    """
    soup = BeautifulSoup(browser.page_source, features="lxml")
    allsrc = soup.find_all("td", {"headers": "size"})
    if Dir_str in allsrc[srcIndex].text:
        return 1
    else:
        return 0

def every_downloads_chrome(browser):
    """
    It is a function to check whether downloading task is completed.
    :param driver: Chrome Webdriver
    """
    if not browser.current_url.startswith("chrome://downloads"):
        browser.get("chrome://downloads/")
    return browser.execute_script("""
        var items = downloads.Manager.get().items_;
        if (items.every(e => e.state === "COMPLETE"))
            return items.map(e => e.fileUrl);
        """)

def move_file(dst_path):
    """
    It is a function to put the downloaded file into corresponding directory.
    @:param dst_path: It is the path of destination.
    """
    for file in os.listdir(Download_path):
        if file.endswith(".crdownload"):
            time.sleep(5)
            continue
        elif file.endswith(".pdf") or file.endswith(".pptx") or file.endswith(".ppt") or file.endswith(".docx") or file.endswith(".doc") or file.endswith(".zip") or file.endswith(".xlsx"):
            print("### Move %s ### \n" %file)
            shutil.move(Download_path + "/" + file, dst_path)
        else:
            continue

def downloadCourse(srcIndex, courseIndex):
    """
    It is a function to download course resources.
    @:param srcIndex: It is the index of which resource you want to download at the specific course path.
    @:param courseIndex: It is the index of course you want to download.
    """
    # At most, each course include 2 child directories.
    try:
        if checkDir(srcIndex) == 1:
            chooseDir = CourseResource[srcIndex]
            print("chooseDir = ", chooseDir)

            # It is a directory, go into the directory
            srcDir_path = Download_path + "/" + AllCourses[courseIndex][0] + "/" + chooseDir
            print("(1) os.getcwd() = ", os.getcwd())
            print("srcDir_path = ", srcDir_path)

            if not os.path.exists(srcDir_path):
                os.mkdir(srcDir_path)

            # FileScript = "document.getElementById('sakai_action').value='doExpand_collection';document.getElementById('collectionId').value='/group/" + CourseID + "/" + \
                         # CourseResource[int(srcIndex)] + "/';document.getElementById('navRoot').value='';document.getElementById('showForm').submit();"
            browser.find_element_by_xpath('//*[@id="showForm"]/table/tbody/tr[' + str(3 + srcIndex) + ']/td[3]/a[2]').click()
            # //*[@id="showForm"]/table/tbody/tr[6]/td[3]/a[2]
            browser.implicitly_wait(5)

            soup = BeautifulSoup(browser.page_source, features="lxml")
            items = soup.find_all("span", {"class": "hidden-sm hidden-xs"})

            chooseDirTree = []
            for item in items:
                # print(item.text)
                if item.text == chooseDir:
                    continue
                chooseDirTree.append(item.text)
            print("chooseDirTree = ", chooseDirTree)
            print("len(chooseDirTree) = ", len(chooseDirTree))

            chooseDirType = []
            for idx in range(len(chooseDirTree)):
                # print(checkDir(idx))
                print("chooseDirTree[idx] = ", chooseDirTree[idx])
                chooseDirType.append(checkDir(idx))
                if checkDir(idx) == 1:
                    # @treePath is the param of item  path of the specific source.
                    treePath = srcDir_path + "/" + chooseDirTree[idx]
                    print("Now, treePath = ", treePath)
                    if not os.path.exists(treePath):
                        os.mkdir(treePath)

                    # Get into the tree dir.
                    browser.find_element_by_xpath('//*[@id="showForm"]/table/tbody/tr[' + str(3 + idx) + ']/td[3]/a[2]').click()
                    browser.implicitly_wait(5)

                # os.chdir("..")
                print("(2) os.getcwd() = ", os.getcwd())

                ### Download #####
                soup = BeautifulSoup(browser.page_source, features="lxml")
                src = soup.find_all("td", {"class": "specialLink title"})

                FileLists = []
                FileUrl = []
                print("Start Downloading.\n")
                for item in src:
                    url = item.a.get("href")
                    if url != "#":
                        # Click .pptx/pdf/ppt/docx/doc/xls/csv/zip url
                        file = browser.find_element_by_xpath('//a[@href="' + url + '"]')
                        file.click()

                try:
                    paths = WebDriverWait(browser, 240, 1).until(every_downloads_chrome)
                    print("Save Successfully!\n")

                except Exception as e:
                    print(e)

                print("Move file to Dst path.\n")
                # move_file(Download_path + "/" + AllCourses[courseIndex][0] + "/" + chooseDir + "/" + chooseDirTree[idx])
                move_file(Download_path + "/" + AllCourses[courseIndex][0] + "/" + chooseDir)
                # srcDir_path = Download_path + "/" + AllCourses[courseIndex][0] + "/" + chooseDir
                print("Move Successfully.\n")

                # Go back to specific Source
                browser.back()

                if idx == len(chooseDirTree):
                    browser.find_element_by_xpath('//*[@id="showForm"]/ol/li[2]/a').click()
                else:
                    browser.find_element_by_xpath('//*[@id="showForm"]/ol/li[3]/a').click()
        else:
            ### Download #####
            soup = BeautifulSoup(browser.page_source, features="lxml")
            src = soup.find_all("td", {"class": "specialLink title"})

            print("Start Downloading.\n")
            for item in src:
                url = item.a.get("href")
                if url != "#":
                    # Click .pptx/pdf/ppt/docx/doc/xls/csv/zip file
                    file = browser.find_element_by_xpath('//a[@href="' + url + '"]')
                    file.click()
            try:
                paths = WebDriverWait(browser, 240, 1).until(every_downloads_chrome)
                print("Save Successfully!\n")
            except Exception as e:
                print(e)

            print("Move file to Dst path.\n")
            move_file(Download_path + "/" + AllCourses[courseIndex][0])
            print("Move Successfully.\n")

            browser.back()

    except Exception as e:
        print(e)

def logout():
    """
    It is a function to log out UCAS onestop system.
    """
    try:
        browser.close()
    except Exception as e:
        print(e)


if __name__ == '__main__':

    print("Please input your UCAS onestop username: ")
    username = input()

    print("Please input your password: ")
    password = input()

    # 0. Open a Chrome browser
    options = Options()
    options.add_experimental_option("prefs", {
        "download.default_directory": Download_path,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True,
        "plugins.always_open_pdf_externally": True
    })

    browser = webdriver.Chrome(options=options)
    browser.get(index_url)

    # Define wait for loading
    wait = WebDriverWait(browser, 10)

    # 1. Login
    login()

    # 2. Go to course website.
    gotoCourseWeb()

    # 3. List all the courses.
    AllCourses = listAllCourse()
    print(AllCourses)

    # 4. Choose Course and go to the course you chose.
    # Create a directory under Download_path and name the directory as the course name.
    print("Please input the index of which course you want to choose.\n")
    CourseIndex = int(input())
    CourseID = AllCourses[CourseIndex][1].split("/")[-1]

    CourseResource = chooseCourse(CourseIndex)
    print(CourseResource)

    # 5. If only file in the FileLists, download all the files.
    # If there are some directories in FileLists, input the index of specific directory and download
    print("5. Please input the index of directory/file\n")
    SrcIndex = int(input())
    downloadCourse(SrcIndex, CourseIndex)

    # 6. Logout
    print("6. Logout.\n")
    logout()