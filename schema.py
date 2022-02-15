main_schema = """
type Query {
    url(name: String!) : String
}

type Mutation {
    addSite(name: String!, url: String!): Boolean!
}
"""