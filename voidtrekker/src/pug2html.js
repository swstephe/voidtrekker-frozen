const pug_file = process.argv[2]
const data = JSON.parse(process.argv[3])
const pug = require('pug')
const compiled = pug.compileFile(pug_file, {})
process.stdout.write(compiled(data))
