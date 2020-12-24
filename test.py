import pandas as pd
df = pd.DataFrame([[1,-1,[5,7]],[2,-1,[3]],[3,2,[4]],[4,3,[]],[5,1,[6]],[6,5,[]],[7,1,[8,9]],[8,7,[10]],[9,7,[]],[10,8,[]]],index=[1,2,3,4,5,6,7,8, 9, 10], columns=['tweet_id', 'tweet_parent', 'tweet_fils'])
print(df)
print(df.shape)
Sr="ab cd\n ce "
