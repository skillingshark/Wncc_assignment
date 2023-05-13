import requests
import pandas as pd
from bs4 import BeautifulSoup


#----------------------------------------------------------------------------------------------------------------------------------------------------------
#1st Part : creating main url and soup

url ="https://itc.gymkhana.iitb.ac.in/wncc/soc/"
page = requests.get(url)
soup = BeautifulSoup(page.text,'html.parser')


#-----------------------------------------------------------------------------------------------------------------------------------------------------------
#2th Part : Creating list of projects

project_name = [] # List of Projects
for i in soup.find_all('p',class_='lead text-center font-weight-bold text-dark'):
    project_temp = i.text
    project_name.append(project_temp)



#---------------------------------------------------------------------------------------------------------------------------------
#3rd part : Creating list of Anchor Tags and links of all projects

anchors = [] #List containing link of all projects
count =0 

all_elements = soup.find_all('div',class_='rounded hover-wrapper pr-3 pl-3 pt-3 pb-3 bg-white')


for i in all_elements:
    temp = str(i.get('href'))
    anchors.append(temp)
    # print(anchors[count])
    count = count +1
    
# print(count)


#--------------------------------------------------------------------------------------------------------------------------------------------------------
#4th part : Creating Urls and Soup for each project using the Anchors list and for loop iteration
# Making list of all MENTOR NAMES
# Making list of NUMBER OF MENTEES in each project
# Making list of NUMBER OF MENTORS in each project
# Making list of PROJECT IMG LINKS
# Making list of PROJECT LINKS


mentor_name = [] # list of all MENTOR NAMES
mentee_num = [] # list of NUMBER OF MENTEES in each project
num_mentor = [] # list of NUMBER OF MENTORS in each project
img_link = [] # list of PROJECT IMG LINKS
project_links =[] # list of PROJECT LINKS
prereq = []
c=0
for i in all_elements:
    url2 = "https://itc.gymkhana.iitb.ac.in/" + anchors[c]
    page2 = requests.get(url2)
    soup2 = BeautifulSoup(page2.text , 'html.parser')
    mentor_temp = soup2.find('h4',class_='display3').next_sibling.next_sibling
    mentor_name.append(mentor_temp.text)
    # print(mentor_name[c])
    project_links.append(url2)
    mentee_temp = soup2.find('h4',class_='display3').next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.next_sibling.text
    mentee_num.append(mentee_temp)
    img_temp =soup2.find('img' , class_='image-1')
    img_link.append( "https://itc.gymkhana.iitb.ac.in/" + str(img_temp.get('src')))
    # print(mentee_num[c])
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
# 5th part :  MAKING A LIST OF PREREQUISITES

    temp = soup2.find('div' , class_='mobile-img-soc').next_sibling.next_sibling.next_sibling.next_sibling.text
    # list = [temp]
    # print(temp)
    index = 0
    check = 0
    index = temp.find("Prerequisites") + 16
    if(temp.find("Prerequisites")>0):
        check = check + 1
    if(check == 0):
        index = temp.find('Prerequisite')+16
        if(temp.find("Prerequisite")>0):
            check = check + 1
    if(check == 0):
        index = temp.find('Prereqs')+10
        if(temp.find("Prereqs")>0):
            check = check + 1
    if(check == 0):
        index = temp.find('Prequisites:')+14
        if(temp.find("Prequisites:")>0):
            check = check + 1
    if(check == 0):
        index = temp.find('Pre-resuisites')+17
        if(temp.find("Pre-resuisites")>0):
            check = check + 1
    if(check == 0):
        index = temp.find('Pre-requisites')+17
        if(temp.find("Pre-requisites")>0):
            check = check + 1
    if(check == 0):
        index = temp.find('PreReqs:')+10
        if(temp.find("PreReqs:")>0):
            check = check + 1
    temp = temp.replace('\n','^')
    index2 = 0
    for i in range(index,len(temp)):
        if(temp[i]=='^'):
            index2 = i
            break
    # print(index)
    # print(index2)
    temp = temp.replace('^','|')
    temp = temp.replace('-',' ')
    if(check!=0):
        prereq.append(temp[index-1:index2])
    else:
        prereq.append("Enthusiasm")
#-------------------------------------------------------------------------------------------------------------------------------------------------------------
    c=c+1

#------------------------------------------------------------------------------------------------------------------------------------------------------------
#6th part : Data cleaning and Preprocessing on the data
#For removing \n from mentor names , number of mentees
#For counting no. of mentors

length = len(mentor_name)
for i in range(length):
    # mentor_name[i] = mentor_name[i].replace("\n" , "/n")
    mentor_name[i] = mentor_name[i].replace("\n" , "/")
    a = 0
    for j in range(len(mentor_name[i])):
        if (mentor_name[i][j]=='/') :
            a = a+1
    
    num_mentor.append(a-1)      
    # mentor_name[i] = mentor_name[i].replace("/n" , "   ")

    #To replace \n by / then adding comma at right position
    if(num_mentor[i]==1):
        mentor_name[i] = mentor_name[i].replace("/" , "")
    else:
        for j in range(len(mentor_name[i])):
            if(j==0 or j==len(mentor_name[i])-1):
                mentor_name[i] = mentor_name[i][:j] + ' ' + mentor_name[i][j+1:]
                
            elif(mentor_name[i][j]=='/'):
                mentor_name[i] = mentor_name[i][:j] + ',' + mentor_name[i][j+1:]

    
    mentor_name[i] = mentor_name[i].replace("," , " , ")
    mentee_num[i] = mentee_num[i].replace("\n","")
    for j in range(len(mentee_num)):
        if(len(mentee_num[i])<=2):
            mentee_num[i] = 'upto ' + mentee_num[i]
    mentee_num[i] = mentee_num[i].replace("-"," to ")
    # print(num_mentor[i])   



#-------------------------------------------------------------------------------------------------------------------------------------------------------------------
#7th part : Creating final dataFrame and exporting to csv file


# print(project_name[0])
df2 = pd.DataFrame([project_name,mentor_name,num_mentor,mentee_num , project_links, img_link ,prereq])
df2.index = ['PROJECTS','MENTORS      ','NUMBER OF MENTORS','   MENTEES     ' , 'PROJECT LINKS              ' ,'PROJECT IMAGE LINK        ','PREREQUISITES        ']
df2 = df2.T
# df2 = pd.DataFrame(df2.T,columns=('Projects','Mentors','Mentees'))
print(df2)


df2.to_csv('Tabulated_data.csv', index=False)











