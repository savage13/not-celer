
function lss_segment(name) {
    return `   <Segment><Name>${name}</Name><Icon/></Segment>`
}

export function lss_splits(title, category, names) {
    const xml_header = '<?xml version="1.0" encoding="UTF-8"?>'
    const run = '<Run version="1.7.0">'
    const run_end = '</Run>'
    const icon = `<GameIcon/>`
    const name = `<GameName>${title}</GameName>`
    const cat = `<CategoryName>${category}</CategoryName>`
    const meta = `<Metadata><Run id=""/><Platform usesEmulator="False"/><Region/><Variables><Variable name="Patch">1.2.3.4</Variable></Variables></Metadata>`
    const offset = `<Offset>00:00:00</Offset>`
    const count = `<AttemptCount>0</AttemptCount>`
    const history = `<AttemptHistory/>`
    let segments = [`<Segments>`]
    for(const name of names) {
        segments.push(lss_segment(name))
    }
    segments.push(`</Segments>`)
    segments = segments.join("\n")
    let out = `${xml_header}
${run}
${icon}
${name}
${cat}
${meta}
${offset}
${count}
${history}
${segments}
${run_end}
`
    return out
}
