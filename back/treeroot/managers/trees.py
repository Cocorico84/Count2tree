from treeroot.models.tree import Tree
from treeroot.models.user import User
from treeroot.models.favorite import Favorite
import requests
import csv




def load_data():
    r = requests.get('https://opendata.paris.fr/api/records/1.0/search/?dataset=les-arbres&facet=typeemplacement&facet=domanialite&facet=arrondissement&facet=libellefrancais&facet=genre&facet=espece')
    data = r.json()
    print(data)


def get_tree_by_genus(self):
    genus = []
    for genus_tree in self.genus:
        genus.append(genus_tree.specie)
    return genus

#df = pd.read_csv('les-arbres.csv',sep=';')
#df.drop(['COMPLEMENTADRESSE','TYPEEMPLACEMENT','DOMANIALITE','CIRCONFERENCEENCM','NUMERO','LIEU / ADRESSE','IDEMPLACEMENT','LIBELLEFRANCAIS','REMARQUABLE','geo_point_2d'],axis=1,inplace=True)
#print(list(df.columns.values.tolist()))
#df['IDBASE'] = df['IDBASE'].astype(int)
#df.to_csv("les-arbres2.csv")


def data_csv_in_class():
    with open('les-arbres2.csv','r') as f:
        reader = csv.DictReader(f,delimiter=',')
        results = []
        for row in reader:
            results.append(dict(row))

    for i in results:
        tree = Tree.get_or_none(id=i['IDBASE'])
        if tree is None:
            tree = Tree.create(id=i['IDBASE'],localisation=i['ARRONDISSEMENT'],genus=i['GENRE'],specie=i['ESPECE'],variety=i['VARIETEOUCULTIVAR'],height=i['HAUTEUR (m)'])
    return tree


def create_tree(variety,height):
    caracteristics = {"variety":variety,"height":height}
    tree = Tree.get_or_none(caracteristics=caracteristics)
    if tree is None:
        tree = Tree.create(**caracteristics)
    else:
        tree.update(**caracteristics).execute()
    return tree


def search_trees(localisation):
    trees = Tree.select().where(Tree.localisation == localisation).limit(10).execute()
    return trees


def get_locations():
    query = Tree.select(Tree.localisation).distinct().order_by(Tree.localisation).execute()
    locations = []
    for element in query:
        locations.append(element.localisation)
    return locations


def get_height():
    query = Tree.select(Tree.height).distinct().where(Tree.height < 10).execute()
    height = []
    for element in query:
        height.append(element.height)
    return height


def create_user(username,password):
    data = {'username' : username, 'password' : password}
    user = User.get_or_none(data=data)

    if user is None:
        user = User.create(**data)
    else:
        user = User.update(**data).execute()
    return user

def get_user(username,password):
    query = User.select().where(username=username,password=password)

    if query is not None:
        return query
    else:
        print("Your username or password doesn't exist !")
    return query


def get_tree_height_by_locations(localisation):
    height = []
    trees = search_trees(localisation)
    for tree in trees:
        height.append(tree.height)
    return height


def add_favorite(genus, specie, variety):
    data = {'genus':genus,'specie':specie,'variety':variety}
    favorite = Favorite.get_or_none(data=data)
    if favorite is None:
        favorite = Favorite.create(**data)
    else:
        favorite = Favorite.update(**data).execute()
    return favorite