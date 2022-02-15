# GraphQL Simples com Python

**Cleuton Sampaio**

# Preparação

Você precisa ter o **python 3.8+** instalado. O exemplo foi criado e executado em **Linux** mas pode perfeitamente ser executado em **MS Windows** ou **macOS**.
Baixe um zip ou clone o projeto, entre na pasta e crie um ambiente virtual: 

```
python -m venv .
source bin/activate
```
# GraphQL é baseado em grafos

Você pode solicitar qualquer pedaço do grafo de informação. 

Usamos requests POST para enviar queries ao servidor GraphQL. 

# Esquema

Imagine um esquema como esse: 

```
type Query {
    url(name: String!) : String
}
```

Esta é a linguagem [**SDL - Schema Definition Language**](https://graphql.org/learn/schema/) do GraphQL. Estamos declarando um tipo de dados "Query" que tem um campo "url". Os campos podem ou não ter argumentos. Neste caso, para obter a URL, precisamos passar o NOME do site. O nome não pode ser null (note a exclamação após o tipo de dados).

Se quisermos saber a URL de um site, fazemos uma query assim: 

```
{
    "query" : "{url(name: \"github\")}"
}
```
E enviamos usando POST para a URL do servidor. 

O resultado é algo assim: 

```
{ 
    "data" : {"url":"http://github.com"}
}
```

# Mutations

Se quisermos alterar algo no servidor, então precisamos definir uma mutação (mutation). Por exemplo: 

```
type Mutation {
    addSite(name: String!, url: String!): Boolean!
}
```

A mutação "addSite" recebe dois argumentos e retorna um Boolean (True / False), indicando se foi possível ou não adicionar o site. 

Para executar, basta enviar isso em um POST: 

```
{
    "query" : "mutation  {addSite(name: \"netflix\", url: \"netflix.com\")}"
}
```

A resposta pode ser algo assim: 

```
{
    "data" : {"addSite":true}
}
```

# Código

O código **schema.py** contém as declarações do esquema necessário para nossa demonstração. 
O código **servidor.py** é um servidor que usa **Ariadne** e **uvicorn** (**ASGI**) para subir um servidor GraphQL.

Primeiramente, temos que validar o esquema: 

```
type_defs = gql(main_schema)
```

É muito fácil associar as **queries** e as **mutations** às funções python que as resolvem: 

```
query = ObjectType("Query")

@query.field("url")
def resolve_name(*_, name):
    ...

mutation = MutationType()
@mutation.field("addSite")
def resolve_addSite(_, info, name, url):
    ...
```

E temos que compilar o esquema: 

```
schema = make_executable_schema(type_defs, [query,mutation])
```

E subir um objeto ASGI gerado pelo GraphQL: 

```
app = GraphQL(schema, debug=True)
```

# Testar

A URL padrão do Ariadne é: http://localhost:8000, que abre um **playground** GraphQL. Se você quiser enviar um request com um programa, por exemplo o **cURL**, pode usar: http://localhost:8000/graphql

Há um arquivo **curl.txt** com dois comandos cURL: Um para consultar e outro para adicionar um site. 

```
