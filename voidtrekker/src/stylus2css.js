const stylus_file = process.argv[2]
const fs = require('fs')
const stylus = require('stylus')
const src = fs.readFileSync(stylus_file, 'utf8')
stylus(src)
  .set('filename', stylus_file)
  .render(function(err, css) {{
    if (err) throw err;
    process.stdout.write(css);
  }})
