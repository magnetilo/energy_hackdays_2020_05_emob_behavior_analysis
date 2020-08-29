import pandas as pd
from sklearn.ensemble import RandomForestRegressor

metrics_and_features_df = pd.read_excel('/../...../public_chargers_metrics_and_features.csv').set_index('evseid')

y_df = metrics_and_features_df.loc[:, 'occupied_ratio']     # extract occupied_ratio
X_df = metrics_and_features_df.loc[:, ['power', 'municipal_typologie', 'population_hect']]     # extract power	municipal_typologie	population_hect


rf = RandomForestRegressor()

rf.fit(X_df, y_df)




# feature importance plot

def plot_feature_importances(feature_importances, column_names, color='b'):
    sort_idx = np.argsort(np.abs(feature_importances))
    plt.figure(num=None, figsize=(8, 8))
    plt.barh(np.arange(len(feature_importances)), feature_importances[sort_idx], color=color)
    plt.yticks(np.arange(len(feature_importances)), column_names[sort_idx])
    plt.title('Feature importances')
    plt.show()


plot_feature_importances(rf.feature_importances_, X_df.columns)
    
    

# feature dependence plot

from sklearn.inspection import plot_partial_dependence

plot_partial_dependence(
    rf,
    X_df,
    features=['power', 'municipal_typologie', 'population_hect'])

fig = plt.gcf()
fig.subplots_adjust(hspace=0.8)
plt.show()





