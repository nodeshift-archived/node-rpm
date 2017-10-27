const name = process.argv[2];
const version = process.argv[3];

const xml = String.raw`<?xml version='1.0'?>
<licenseSummary>
    <project>${name}</project>
    <version>${version}</version>
</licenseSummary>`;

console.log(xml);
