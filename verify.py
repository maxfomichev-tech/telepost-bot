import json, urllib.request, sys

sys.stdout.reconfigure(encoding='utf-8')

API = 'https://n8n-service-f9co.onrender.com/api/v1'
KEY = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiI2NTEzNzM2My0wYTUzLTQyYjctYjA3YS03MjFkNTFiY2JkZmEiLCJpc3MiOiJuOG4iLCJhdWQiOiJwdWJsaWMtYXBpIiwianRpIjoiYTM4NjUyOGItODI2ZC00MjNkLWFhYjUtMWViZTA5ZGYzYmExIiwiaWF0IjoxNzgwMTczNzMzLCJleHAiOjE3ODI3MDU2MDB9.XENIuusMbVQJmDqzjnGm6fRS7SAco6n6KjrvAafdk8M'
headers = {'X-N8N-API-KEY': KEY}

# Check last execution
req = urllib.request.Request(f'{API}/executions?limit=1&workflowId=olY5LFhYz2NIBCAC', headers=headers)
resp = urllib.request.urlopen(req)
data = json.loads(resp.read().decode())

for ex in data.get('data', []):
    eid = ex['id']
    print(f"Execution {eid} | Status: {ex.get('status')} | Started: {ex.get('startedAt')}")

    req2 = urllib.request.Request(f'{API}/executions/{eid}?includeData=true', headers=headers)
    resp2 = urllib.request.urlopen(req2)
    full = json.loads(resp2.read().decode())

    rd = full.get('data', {}).get('resultData', {})
    err = rd.get('error')
    if err:
        print(f"Error: {json.dumps(err, ensure_ascii=False)[:300]}")

    for node_name, node_data in rd.get('runData', {}).items():
        for run in node_data:
            status = run.get('executionStatus', 'unknown')
            main = run.get('data', {}).get('main', [])
            output = main[0] if main else []
            print(f"  [{node_name}] {status}, {len(output)} items")
            for item in output[:2]:
                j = item.get('json', {})
                print(f"    {json.dumps(j, ensure_ascii=False)[:250]}")
            if not output:
                print(f"    (empty)")
