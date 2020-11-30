import pandas as pd
import mongo



def main():
    mongo.connect_mongo()
    mongo.connect_coll('gal_part_proj', 'ATX_tech_rec')
    cursor = mongo.coll.find({}, {'_id':0})

    df = pd.DataFrame(cursor)
    df = df.T

    index = list()
    results = list()

    for idx, row in df.iterrows():
        index.append(idx)
        results.append(row[row.notnull()].values[0])

    clean_df = pd.DataFrame(results, index=index)
    clean_df.rename({0: 'Scrape Results'}, axis=1, inplace=True)
    clean_df.head()


if __name__ == '__main__':
    main()