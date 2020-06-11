# Recommendation_System

### Problem Statement
The dataset contains information on books purchased through amazon. Our objective is to provide recommendations based on the information we have by using a custom scoring mechanism

### Approach
Recommendation systems can be categorized broadly into two categories – Content based filtering and Collaborative filtering. We have information that can be used for both these methods. The CoPurchase graph gives us information on books co-purchased together and hence can be helpful for Collaborative filtering methods. Meanwhile the edge weights on this graph , and also the measures in the dataframe, gives us item information. We use a combination of these to generate our recommendations

### Scoring Mechanism (Higher is better)
`Score= AvgRating* (Log(DegreeCentrality)+1) * (EdgeWeight+1)^2 *Log(Zipf's value)`

The logic behind this scoring mechanism is pretty intuitive.
A better AverageRating obviously means a better product. We multiply this with DegreeCentrality. A higher DC means a more popular book and hence a better recommendation. Since the DC varies quite a lot (having large values), we standardize it using a log function (we add 1 since it gives better results). EdgeWeight is perhaps the most important factor and hence we square the value (Adding 1 since EdgeWeight is always less than 1. 
Finally, a lower value for sales rank means it’s a better product. But we would want to reward better ranked members more than the other books. Hence we try to implement Zipf’s law.

Zipf’s law has its roots in information retrieval techniques and states that the frequency of a word is inversely proportional to rank. In other words the frequency of the 2nd ranked word is ½ of the 1st ranked word, the frequency of the 3rd ranked word in 2/3 the frequency of the 2nd word and so on. We calculate the zipf’s value , where we generate a series using the numpy method np.zipf, divide by maximum value and multiply by 100 and append to dataset.

Zipf’s array for 10 ranks(descending) = [20.0, 20.0, 20.0, 20.0, 20.0, 20.0, 40.0, 40.0, 80.0, 100.0]
This is the value we multiply the whole score with and this gives better recommendations.
