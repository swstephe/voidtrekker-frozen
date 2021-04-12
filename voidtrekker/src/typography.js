const config = JSON.parse(process.argv[2])
const Typography = require('typography')
const typography = new Typography(config)
process.stdout.write(typography.toString())
