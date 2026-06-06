import json, time, urllib.parse, urllib.request

MAX_TO_PROCESS = 20  # limit for quick test

def search_europepmc(query):
    url = f"https://www.ebi.ac.uk/europepmc/webservices/rest/search?query={urllib.parse.quote(query)}&format=json&resulttype=lite"
    try:
        with urllib.request.urlopen(url, timeout=10) as resp:
            data = json.load(resp)
            results = data.get('resultList', {}).get('result', [])
            if results:
                return results[0]
    except Exception as e:
        print('Error querying', query, e)
    return None

def main():
    with open('tools_data.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    found = 0
    processed = 0
    for tool in data.get('tools', []):
        if processed >= MAX_TO_PROCESS:
            break
        if not tool.get('preprint_doi') and not tool.get('preprint_link') and tool.get('publication_type') != 'preprint':
            name = tool.get('name')
            if not name or len(name) < 5:
                continue
            query = f'"{name}" AND SRC:PPR'
            result = search_europepmc(query)
            if result and result.get('doi'):
                tool['preprint_doi'] = result['doi']
                tool['preprint_link'] = f"https://doi.org/{result['doi']}"
                found += 1
                print(f"Found preprint for {name}: {tool['preprint_doi']}")
            processed += 1
            time.sleep(0.2)
    print('Total preprints found in subset:', found)
    with open('tools_data_updated_subset.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    print('Saved subset updated file')

if __name__ == '__main__':
    main()
