from contextlib import nullcontext
from ariadne import ObjectType, QueryType, MutationType, gql, make_executable_schema
from ariadne.asgi import GraphQL
from schema import main_schema

# Database de Sites:

db_sites = {}

db_sites["google"] = "http://google.com"
db_sites["github"] = "http://github.com"

# Criando o esquema a partir da SDL: 

type_defs = gql(main_schema)

# Resolvers para query: 

query = ObjectType("Query")

@query.field("url")
def resolve_name(*_, name):
    if name in db_sites:
        return db_sites[name]
    else:
        return None

# Resolvers para Mutation:

mutation = MutationType()
@mutation.field("addSite")
def resolve_addSite(_, info, name, url):
    if name and url:
        db_sites[name]=url
        return True
    return False

# Compila o esquema: 

schema = make_executable_schema(type_defs, [query,mutation])

app = GraphQL(schema, debug=True)

