// Local fixture: exercise the Firecrawl dependency overrides without credentials.
const assert = require('node:assert/strict');
const http = require('node:http');
const { Firecrawl } = require('firecrawl');
const { z } = require('zod/v3');
const { zodToJsonSchema } = require('zod-to-json-schema');

async function main() {
  const schema = z.object({ title: z.string(), count: z.number().int() });
  const converted = zodToJsonSchema(schema);
  assert.equal(converted.properties.title.type, 'string');
  assert.equal(converted.properties.count.type, 'integer');
  const requests = [];
  const server = http.createServer(async (request, response) => {
    let body = '';
    for await (const chunk of request) body += chunk;
    requests.push(JSON.parse(body));
    response.writeHead(200, { 'content-type': 'application/json' });
    response.end(JSON.stringify({ success: true, data: {
      markdown: '# Fixture', json: { title: 'Fixture', count: 1 },
      metadata: { statusCode: 200, sourceURL: 'https://example.com' },
    } }));
  });
  await new Promise(resolve => server.listen(0, '127.0.0.1', resolve));
  try {
    const client = new Firecrawl({ apiKey: 'local-fixture-only',
      apiUrl: `http://127.0.0.1:${server.address().port}` });
    // The CLI sends plain JSON Schema; the SDK also accepts Zod v3 schemas.
    for (const input of [converted, schema]) {
      const result = await client.scrape('https://example.com', {
        formats: ['markdown', { type: 'json', schema: input }],
      });
      assert.equal(result.markdown, '# Fixture');
      assert.equal(result.json.count, 1);
      const sent = requests.at(-1).formats.find(format => format.type === 'json').schema;
      assert.equal(sent.properties.title.type, 'string');
      assert.equal(sent.properties.count.type, 'integer');
    }
    console.log('PASS: Firecrawl JSON Schema and Zod v3 compatibility requests/responses');
  } finally {
    await new Promise(resolve => server.close(resolve));
  }
}
main().catch(error => { console.error(error); process.exitCode = 1; });
