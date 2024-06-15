# Not Celer
Routing tool for Zelda TotK

You can find it https://restite.org/not-celer

### What is here
- index.html: primary program where most of the code is constain as inline javascript.
    Be warned, its messy and needs attention
- generate_meta_data.py: creates celer_totk_metadata.json from a set of "raw" json files obtained from radar-totk.zeldamods.org.  Most of the input files start with `raw_`
- server.py: runs a local https webserver with an associated key.pem / server.pem.  Clipboard usage requires https
- Assorted Image files and javascript libraries

#### Support for loading routes from external resources
- Github Gist
  - `https://restite.org/notceler-totk/?gist=${gist_id}`
- Github Repo
  - `https://restite.org/notceler-totk/?github=${user}/${repo}/${branch}/${filepath}`
- Codeberg
  - `https://restite.org/notceler-totk/?codeberg=${user}${repo}/raw/{$filepath}` 

### License
BSD 2-Clause License

### Why does the code look so bad
This started as a project to see if the previous celer routes could be parsed within the browser.  It turned into mostly a placeholder / stop-gap for the new version of celer to be finished.  As such I did not want to put too time / effort into something that may disappear.  As such, it will probably turn into a standard that will get out of control ;P


