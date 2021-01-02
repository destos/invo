const g2j = require("graphql-2-json-schema")
const graphql = require("graphql")

module.exports = {
  plugin: (schema, documents, config, info) => {
    const introSchema = graphql.introspectionFromSchema(schema)
    const result = g2j.fromIntrospectionQuery(introSchema)
    return JSON.stringify(result, null, 2)
  }
}
