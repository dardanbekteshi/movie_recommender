import pandas as pd

r_cols = ["user_id", "movie_id", "rating"]
ratings = pd.read_csv("u.data", sep="\t", names=r_cols,
                      usecols=range(3))
m_cols = ["movie_id", "title"]
movies = pd.read_csv("u.item", sep="|", names=m_cols, 
                     usecols=range(2))
ratings = pd.merge(movies, ratings)
user_ratings = ratings.pivot_table(index=["user_id"], columns=["title"], values=["rating"])

corr_matrix = user_ratings.corr(method="pearson", min_periods=100)

my_ratings = user_ratings.loc[999].dropna()  # select the dummy user ratings which I have added
print "The dummy user has made the following ratings:\n", my_ratings

sim_candidates = pd.Series()
for i in range(0, len(my_ratings)):
    sims = corr_matrix[my_ratings.index[i]].dropna()
    sims = sims.map(lambda x: x * my_ratings[i])  # u japim peshe vlerave varesisht nga ratingu i dhene nga user-i
    sim_candidates = sim_candidates.append(sims)

sim_candidates.sort_values(inplace=True, ascending=False)
sim_candidates = sim_candidates.groupby(sim_candidates.index).sum()
sim_candidates.sort_values(inplace=True,ascending=False)

filtered_sims=sim_candidates.drop(my_ratings.index)
print "The recommendations are as follows:"
print filtered_sims.head(10)