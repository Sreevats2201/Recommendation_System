# -*- coding: utf-8 -*-
"""
@author: Sreevatsan
"""
print ()

import networkx
from operator import itemgetter
import matplotlib.pyplot
import pandas as pd
import numpy as np

# Reading the .csv file containing book informatin onto a dataframe
amazonBooks = pd.read_csv('./amazon-books.csv', index_col=0)

# Reading the weighted edge graph containing information on co-purchases and 
# category similarity

# Edge between two nodes exist if the two books have been co-purchased

# Weight on edge -> Number of similar tags / Total number of distinct tags
fhr=open("amazon-books-copurchase.edgelist", 'rb')
copurchaseGraph=networkx.read_weighted_edgelist(fhr)
fhr.close()

# Now let's assume a person is considering buying the following book;
# what else can we recommend to them based on copurchase behavior 
# we've seen from other users?
print ("Looking for Recommendations for Customer Purchasing this Book:")
print ("--------------------------------------------------------------")
purchasedAsin = '0841914060'

# Let's first get some metadata associated with this book
print ("ASIN = ", purchasedAsin) 
print ("Title = ", amazonBooks.loc[purchasedAsin,'Title'])
print ("SalesRank = ", amazonBooks.loc[purchasedAsin,'SalesRank'])
print ("TotalReviews = ", amazonBooks.loc[purchasedAsin,'TotalReviews'])
print ("AvgRating = ", amazonBooks.loc[purchasedAsin,'AvgRating'])
print ("DegreeCentrality = ", amazonBooks.loc[purchasedAsin,'DegreeCentrality'])
print ("ClusteringCoeff = ", amazonBooks.loc[purchasedAsin,'ClusteringCoeff'])
    

# Now let's look at the ego network associated with purchasedAsin in the
# copurchaseGraph - which is esentially comprised of all the books 
# that have been copurchased with this book in the past


# Our first step would be to get the ego graph at depth 1 for the book 
purchasedAsinEgoGraph = networkx.ego_graph(copurchaseGraph,purchasedAsin,radius=1)

# We identify it's neighbors
egoneighbors = [i for i in purchasedAsinEgoGraph.neighbors(purchasedAsin)] 


        
# Next, recall that the edge weights in the copurchaseGraph is a measure of
# the similarity between the books connected by the edge. So we can use the 
# island method to only retain those books that are highly simialr to the 
# purchasedAsin
threshold = 0.5
purchasedAsinEgoTrimGraph = networkx.Graph()
for f, t, e in purchasedAsinEgoGraph.edges(data=True):
    if e['weight'] >= threshold:
        purchasedAsinEgoTrimGraph.add_edge(f,t,weight=e['weight'])


# We now obtain the neighbors of these neighbors (ie) nodes 1 hop away 
purchasedAsinNeighbors = [i for i in purchasedAsinEgoTrimGraph.neighbors(purchasedAsin)] 

########################### Recommendation algorithm ##########################

#Reading the dataframe

books_data = pd.read_csv('amazon-books.csv',index_col = 'Unnamed: 0')

#Creating a new dataframe for the books that are neigbors in the 
#purchasedAsinTrimGraph
neighbors_data = books_data.loc[purchasedAsinNeighbors]

#Reading infomration on edge weights to or from purchasedAsin to neighbors to
#a list
lst = list()
for f, t, e in purchasedAsinEgoTrimGraph.edges(data=True):
    if f == purchasedAsin:
        lst.append([t,e['weight']])
    if t == purchasedAsin:
        lst.append([f,e['weight']])

#Appending the list to the neighbors dataframe
weight_data = pd.DataFrame(data=lst,columns=['PurchasedAsin','Weight'])
weight_data = weight_data.set_index('PurchasedAsin')
new_data = pd.merge(neighbors_data,weight_data,left_index=True,right_index=True)

#Calculating Zipf's value
a=2
s= np.random.zipf(a,len(purchasedAsinNeighbors))
result = (s/float(max(s)))*100
new_data.sort_values(by=['SalesRank'],ascending=False,inplace=True)
new_data['Zipf value'] = result


#Custom Scoring Mechanism
new_data['Score']= new_data['AvgRating']*(np.log(new_data['DegreeCentrality'])+1)\
       *pow((new_data['Weight']+1),2)*np.log(new_data['Zipf value'])

#Sorting the dataframe accoring to Score and picking top 5
new_data.sort_values(by=['Score'],ascending=False,inplace=True)
reco_books = new_data[:5].index

# Top 5 recommendations

print ("\n\nIf you liked that book, you would love these :\n\n")
    
for book in reco_books:
    print ("ASIN = ", book) 
    print ("Title = ", amazonBooks.loc[book,'Title'])
    print ("SalesRank = ", amazonBooks.loc[book,'SalesRank'])
    print ("TotalReviews = ", amazonBooks.loc[book,'TotalReviews'])
    print ("AvgRating = ", amazonBooks.loc[book,'AvgRating'])
    print ("DegreeCentrality = ", amazonBooks.loc[book,'DegreeCentrality'])
    print ("ClusteringCoeff = ", amazonBooks.loc[book,'ClusteringCoeff'])
    print ("SimilarityScore (Higher is better) = ",new_data.loc[book,'Score'])
    print ("-----------------------------------------------------------------")
    print ()

