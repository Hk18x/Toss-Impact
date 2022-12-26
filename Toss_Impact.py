#!/usr/bin/env python
# coding: utf-8

# # IMPACT OF TOSS ON OUTCOME OF A MATCH
# 
# <br>In this notebook, we will be analysing the impact of toss on the outcome of a match. and the steps we will be following are as follows-<br><br><br>
# <b> 1) Defining the context: </b>
# For any analysis, we will first need to develop an idea of the data that is required and also how are we going to breakdown the analysis into different categories. After finalising the structure of data to be used, the next task is to shortlist the parameters which we'll be using for performing the analysis.<br><br>
# <b> 2) Getting the data: </b>
# Now, the next task is to get the data in the required format discussed in previous step.<br><br>
# <b> 3) Pre-Processing the data: </b>
# After we get the data, the next step is to remove the extra information and clean the dataset to create a new one having the information which can be used for calculating parameters.<br><br>
# <b> 4) Calculating the parameters: </b>
# Now, we need to get the mathematical value of the parameters which we have shortlisted in the first step. So, in this step, we will use the preprocessed data to calculate the required parameters.<br><br>
# <b> 5) Conclusion: </b>
# Then using the calculated parameters, we try to find a trend from them and using this trend, we make a conclusion of our analysis.
# 
# Now, let's look at each of these 5 steps one by one for our analysis on impact of toss on outcome of a match.
# 
# ### Defining the context
# 
# For sake of simplicity, we will only be considering the test matches, but the same analysis can be extrapolated to ODIs and T20Is as well. In this analysis, we will be loking at the impact of toss on the outcome of a match, so the data that we require should have the list of all the test matches that are played, their result, and the toss result. So, the necessary columns are team name, match result and toss result, for each test match happened. Also, for this analysis, we will be considering the recent generation's matches only, i.e. from 2016-present. This period is also selected because of the sudden increase in the of the use data from 2016. Now, since we are looking at test matches, there are 3 results possible for a match (win, lose, or draw), so the parameter that we should look for analysis should not be only focused on winning matches, but also on drawn test matches. So, for this analysis, we will consider lose percentage of a team, after they have one the toss and lost the toss. To summarize, <b>the data we will require is the scorecard data of each match, having result of the match and toss result, and the parameter we will be using for analysing the impact of toss will be the losing percentage of the team after they have won/lost the toss.</b>
# 
# ### Getting the data
# 
# The data required for this analysis in the above mentioned format can be found on statsguru website (by ESPNCricinfo) by applying concerned filters. The procedure to go to the required page is:<br>
# 1) Go to https://stats.espncricinfo.com/ci/engine/stats/index.html and click on team tab. <br>
# 2) Select "Home Venue" in Home or Away row and "Match Results" in View Format row. <br>
# 3) Give the Starting date from 01 Jan 2016 and click Submit Query.<br>
# 4) Go to page number 2 and copy the url. We have copied the url of page number 2 because when the first page is loaded, there is no mention of page number in the URL, but in the URL of page 2, there is a part as "page=2" which will be useful for us in automating the scraping for all pages in one go.<br><br>
# After we have the URL of the webpage, now we will create a web-scraper to scrape all the pages of the query that we gave. First we will create a scaper to scrape one page, and then we will repeat the same steps for all the pages to scrape all the pages.

# In[ ]:


import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen


# In[ ]:


url = 'https://stats.espncricinfo.com/ci/engine/stats/index.html?class=1;home_or_away=1;orderby=start;orderbyad=reverse;page=1;spanmin1=01+Jan+2016;spanval1=span;template=results;type=team;view=results' # URL of page number 1


# To open the webpage in the python notebook, we will use "urlopen" function. It will create a HTTP Response between python notebook and the webpage.

# In[ ]:


text = urlopen(url) # opening the webpage in python


# In[ ]:


print(text)


# Using the link that is being created, we will get the HTML of the webpage using BeautifulSoup library

# In[ ]:


soup = BeautifulSoup(text, "lxml") # getting the HTML of the webpage using BeautifulSoup(_HTTP_Response_, "lxml")


# In[ ]:


print(soup)


# Now, we will analyse the webpage and try to find tags and attributes which makes our desired table different from all other elements on webpage. So, after analysing the webpage, it is found that the table of our interest is different from other elements with tag as table and class as engineTable. Also amongst all the tables with class engineTable, it is the only table having caption tag in it. So now, in the HTML of the webpage, we need to find all the tables with class engineTable, and amongst all those tables, we need to find the table having a caption tag inside it.

# In[ ]:


table = soup.findAll('table', attrs = {'class' : 'engineTable'}) # finding all the tables with class as engineTable in the HTML of webpage
int_table = 0 # defining a variable which will store the HTML of the table of our interest
for temp_table in table: # running a loop over all the tables with class engineTable
    caption_tag = temp_table.findAll('caption') # Looking for caption tag in each table's HTML
    if(len(caption_tag) > 0): # checking if there is any captio tag in the table
        int_table = temp_table # if a caption tag is found then save this table as the table of our interest


# In[ ]:


print(int_table)


# After getting the HTML code of the required table, now we will look for all the rows inside the table and then scrape the data row-wise

# In[ ]:


tr_list = int_table.findAll('tr', attrs = {'class': 'data1'}) # getting all the rows in the table


# In[ ]:


print(len(tr_list))


# As it can be seen that now we have the HTML of all the 50 rows stored in tr_list variable with each element in tr_list as HTML of one row. Now, we will get column data of each row separately and save that into a list. So, for each row, we will look for all td tags and then for each td tag, we will clear all HTML tags from the code to get only the cleantext or the data that is written in that particular cell. Then we will append this cleantext into the row data and then we will append the entire ro data to the master data, i.e. the data for all the matches.

# In[ ]:


master_data = [] # list to contain all the rows in our table
for tr in tr_list:
    td_list = tr.findAll('td') # finding all the td tags in a row
    row_data = [] # list to save the data of each row
    for td in td_list:
        td_str = str(td) # converting HTML of the td tag from BeautifulSoup HTML code to string datatype
        cleantext = BeautifulSoup(td_str, "lxml").get_text() # removing all the unecssary tags from the HTML of td to get only the text written in that tag on webpage
        row_data.append(cleantext) # appendng that data to row data
    master_data.append(row_data) # appending the entire row data to our master data (contaiing all rows)


# In[ ]:


master_data


# The above process is to get the data from 1 webpage, but in our query, we have total 5 webpages. Each of the webpage are same, only the data is different. So now we need to repeat the above process exactly for page 2, 3, 4, and 5. For doing so, we will use a for loop where our variable 'k' will vary from 1 to 5, and repeat the same lines of code for each page. The only difference in URL of these pages is "page=1" (for page 1), "page=2" (for page 2), "page=3" (for page 3) and so on till page=5. So, we will vary our k from 1 to 5 and edit the URL with page=k for each iteration, and run the above blocks of code for each page.

# In[ ]:


master_data = [] # list to contain all the rows in our tables of all the pages of the query
for k in range(1,6): # varying value of k from 1 to 5
    url = 'https://stats.espncricinfo.com/ci/engine/stats/index.html?class=1;home_or_away=1;orderby=start;orderbyad=reverse;page=' + str(k) + ';spanmin1=01+Jan+2016;spanval1=span;template=results;type=team;view=results' # URL of page number 'k'
    text = urlopen(url) # opening the webpage in python
    soup = BeautifulSoup(text, "lxml") # getting the HTML of the webpage using BeautifulSoup(_HTTP_Response_, "lxml")
    table = soup.findAll('table', attrs = {'class' : 'engineTable'}) # finding all the tables with class as engineTable in the HTML of webpage
    int_table = 0 # defining a variable which will store the HTML of the table of our interest
    for temp_table in table: # running a loop over all the tables with class engineTable
        caption_tag = temp_table.findAll('caption') # Looking for caption tag in each table's HTML
        if(len(caption_tag) > 0): # checking if there is any captio tag in the table
            int_table = temp_table # if a caption tag is found then save this table as the table of our interest
    tr_list = int_table.findAll('tr', attrs = {'class': 'data1'}) # getting all the rows in the table
    for tr in tr_list:
        td_list = tr.findAll('td') # finding all the td tags in a row
        row_data = [] # list to save the data of each row
        for td in td_list:
            td_str = str(td) # converting HTML of the td tag from BeautifulSoup HTML code to string datatype
            cleantext = BeautifulSoup(td_str, "lxml").get_text() # removing all the unecssary tags from the HTML of td to get only the text written in that tag on webpage
            row_data.append(cleantext) # appendng that data to row data
        master_data.append(row_data) # appending the entire row data to our master data (contaiing all rows)


# In[ ]:


print(len(master_data))


# There were total 210 matches between 01 Jan 2016 and 25 Feb 2021, and we are also getting the same number of rows in our master_data. Hence our scraper has scraped the complete data from statsguru required for this analysis, now lets convert this master_data to a dataframe, so that we can use pandas then for working with the dataset.

# In[ ]:


master_data_df = pd.DataFrame(master_data)


# In[ ]:


master_data_df


# In[ ]:


# renaming the columns
master_data_df.columns = ["Home", "Result", "Margin", "Toss", "Bat", "None1", "Opposition" , "Ground", "Date", "None2"]


# In[ ]:


master_data_df


# In[ ]:


#saving the data scraped
master_data_df.to_csv('toss_data_2016_2021.csv')


# ## Pre-processing the data
# 
# Now, we have the data of all the matches from 2016-present, the next step is to pre process the data so as to make it easier for calculating parameter which in our case is losing percentage. To calculate losing percentage of each team, we need to have a column in our dataset which should show whether the team who won the toss lost the match (0:if the team winning the toss does not lose the match, 1: if the team winning the toss, lose the match). Now, to create this column, we will need to columns, one is the name of the team who won the toss, and second name of the team who lost the match (in case of draw, the column value will be draw). So let us now create these 2 columns first.<br><br><br>
# Before we create these columns, let us first remove the unecessary columns from the table. Column "None1" and "None2" are empty columns, so we need to drop both of these columns. Also, in opposition column, before the name of oppositiion team, "v " is written, so we need to remove that "v " from the opposition column.

# In[ ]:


#dropping the columns
master_data_df = master_data_df.drop(['None1', 'None2'], axis = 1) # .drop(list_of_columns_to_be_dropped)
# axis=0, if we have to remove rows and axis=1, if we have to remove columns


# In[ ]:


master_data_df


# In[ ]:


# removing "v " from opposition column
master_data_df["Opposition"] = master_data_df["Opposition"].str.replace("v ", "")
# we have replaced "v " with empty string so that we now have only the name of the team in Opposition column


# In[ ]:


master_data_df


# Now, let us create the two columns, the first column will be the name of the team who won the toss, because in our table, we only have won and lost in the toss column, it does not have the name of the team who won the toss. To create this column, we will run a for loop on the entire dataframe and then for each row we will see if the Toss is won, then the team who won the toss is Home team, else it is the opposition team.

# In[ ]:


toss_team = [] # a list to contain each row's value of new column
for index, row in master_data_df.iterrows(): # for loop on the dataframe
    if(row["Toss"] == "won"): # if the toss value is won, then the team who won the toss is Home team
        toss_team.append(row["Home"])
    else: # if the toss value is lost, then the team who won the toss is opposition
        toss_team.append(row["Opposition"])


# In[ ]:


toss_team


# In[ ]:


# Adding this column to dataframe
master_data_df["toss_team"] = toss_team


# In[ ]:


master_data_df


# Now we will add the next column as the name of the team who lost the match (Draw in case of a draw). To add this column, we will again look at each row separately. For each row, if the Result is won, then the team lost the match is opposition, if the Result is lost, then the team lost the match is home, or if the Result is draw, then the match was drawn.

# In[ ]:


team_lost = [] # a list to contain the name of the team who lost the match for each row
for index, row in master_data_df.iterrows(): # for loop for the entire dataframe
    if(row["Result"] == "won"): # if the Result is won, then the team lost the match is opposition
        team_lost.append(row["Opposition"])
    elif(row["Result"] == "lost"): # if the Result is lost, then the team lost the match is Home
        team_lost.append(row["Home"])
    else: # if the Result is draw, then the match is draw
        team_lost.append("draw")


# In[ ]:


team_lost


# In[ ]:


# Adding this column to dataframe
master_data_df["team_lost"] = team_lost


# In[ ]:


master_data_df


# Now we will add the final column i.e. whether the team who won the toss, has lost the match or not.<br>
# 0: if the team who won the toss, didn't lose the match<br>
# 1: if the team who won the toss, lost the match

# In[ ]:


won_toss_lost_match = [] # defing a list that will contain the 0/1 values for each row in the dataframe
for index, row in master_data_df.iterrows(): # for loop over the entire dataframe
    if(row["toss_team"] == row["team_lost"]): # if the team who lost the toss, has also lost the match, then the value will be 1
        won_toss_lost_match.append(1)
    else: # if the team who lost the toss, has not lost the match, then the value will be 0
        won_toss_lost_match.append(0)


# In[ ]:


won_toss_lost_match


# In[ ]:


# Adding the column to dataframe
master_data_df["toss_data"] = won_toss_lost_match


# In[ ]:


master_data_df


# ## Calculating the parameters
# 
# Now, we have the data in the desired format, we need to calculate the lose percentage for each team after they have won the toss. To do so, first of all we will need to find all the unique teams in our dataset and after that, for each team, we will see the total number of instances where the team has won the toss, and then we will look at the the total number of instances where the value of "toss_data" is 1 for that team. Using these 2 values we will get the losing percentage of the team ((total instances of "toss_data = 1")/(total instances where team has won the toss))
# 
# Let us now first find the unique teams in our dataset:

# In[ ]:


teams = master_data_df["toss_team"].unique().tolist() # first we use the unique() function to find all the unique values in
# the "toss_team" column and then converted that output array into a list using tolist() function because we are more
# comfortable working with lists.


# In[ ]:


teams


# After finding the unique list of teams, now we will look at each team separately and calculate losing percentage of each team. For each team, first we will filter the dataset to contain only the rows where toss_team is the team we are considering, and then we will find the total number of occurances of 1 in toss_data column in this filtered dataframe. After that we will divide this number by the total number of rows for that team to calculate lose percentage.

# In[ ]:


loss_percentage = [] # loss percentage list for each team
for team in teams: # running a for loop on teams list, taking one team per iteration
    filtered_df = master_data_df[master_data_df["toss_team"] == team] # filtering the data where toss_team is equal to the name of our concerened team
    num_of_matches = len(filtered_df) # calculating total number of matches where the team has won the toss
    lost_df = filtered_df[filtered_df["toss_data"] == 1] # filtering only the rows where team has lost the match after winning the toss
    lost_count = len(lost_df) # calculating number of times the team has lost the match after winning the toss
    loss_percent = lost_count/num_of_matches*100 # calculating loss percentage
    temp = [] # creating an empty list to store losing percentage and team name
    temp.append(team) # adding team name in temp list
    temp.append(loss_percent) # adding loss_percent in temp list
    loss_percentage.append(temp) # adding temp list to the main loss percentage list


# In[ ]:


loss_percentage


# ## Conclusion
# 
# We will not be considering Afghanistan and Ireland as the sample size is less for them. For India, Australia, New Zealand and South Africa, losing percentage is at max 20% after winning the toss, which indicate that these teams uses the toss for their benefit and toss plays an important role in the outcome of the match. Also, for India it is only 5% which indicates that team India knows how to use the toss to their benefit very well. Teams like England, Bangladesh, West Indies and Pakistan are yet to figure out how to use the toss for their benefit as their losing percentages are high even after winning the toss. So, to conclude, it can be said that in test matches, toss plays an important role for top teams as they have less losing percentages whereas other teams are yet to take advantage of toss in tests.
