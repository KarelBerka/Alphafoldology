const fs = require('fs');

async function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

async function searchEuropePMC(query) {
    const url = `https://www.ebi.ac.uk/europepmc/webservices/rest/search?query=${encodeURIComponent(query)}&format=json&resultType=lite`;
    try {
        const response = await fetch(url);
        if (!response.ok) return null;
        const data = await response.json();
        if (data.resultList && data.resultList.result && data.resultList.result.length > 0) {
            return data.resultList.result[0];
        }
    } catch (e) {
        console.error(`Error querying ${query}:`, e.message);
    }
    return null;
}

async function main() {
    console.log("Loading tools_data.json...");
    const rawData = fs.readFileSync('tools_data.json', 'utf8');
    const data = JSON.parse(rawData);
    
    let foundCount = 0;
    
    for (let i = 0; i < data.tools.length; i++) {
        const tool = data.tools[i];
        
        if (!tool.preprint_doi && !tool.preprint_link && tool.publication_type !== 'preprint') {
            // Search Europe PMC for a preprint with a matching title/name
            // We search for the exact phrase if it's long, else just the keywords
            let query = `"${tool.name}" AND SRC:PPR`;
            if (tool.name.length < 5) continue; // skip very short generic names

            console.log(`[${i+1}/${data.tools.length}] Searching for: ${tool.name}`);
            const result = await searchEuropePMC(query);
            
            if (result && result.doi) {
                console.log(`  -> Found preprint: ${result.title} (${result.doi})`);
                tool.preprint_doi = result.doi;
                tool.preprint_link = `https://doi.org/${result.doi}`;
                foundCount++;
            } else {
                // If it has a paper_doi, we could theoretically look it up, but text search usually covers it
            }
            
            await sleep(200); // 5 requests per second
        }
    }
    
    console.log(`Finished. Found preprints for ${foundCount} tools.`);
    data.metadata.total_preprints = (data.metadata.total_preprints || 0) + foundCount;
    
    fs.writeFileSync('tools_data_updated.json', JSON.stringify(data, null, 2), 'utf8');
    console.log("Saved to tools_data_updated.json.");
}

main().catch(console.error);
