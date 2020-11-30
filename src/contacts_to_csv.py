import pandas as pd
import mongo



def main():
    mongo.connect_mongo()
    mongo.connect_coll('gal_part_proj', 'ATX_tech_rec')
    cursor = mongo.coll.find({{}, {'_id':0}})

    df = pd.DataFrame(cursor)
    df = df.T


if __name__ == '__main__':
