const coffee_file = process.argv[2]
const fs = require('fs')
const coffeescript = require('coffeescript')
const src = fs.readFileSync(coffee_file, 'utf8')
process.stdout.write(coffeescript.compile(src, {
    bare: true
}))
