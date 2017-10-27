const name = process.argv[2];

const html = String.raw`<html>
<head>
<meta http-equiv="Content-Type" content="text/html;charset=utf-8">
<link rel="stylesheet" type="text/css" href="licenses.css">
</head>
<body>
<h2>${name}</h2>
<table>
<tr>
<th>Package Group</th>
<th>Package Artifact</th>
<th>Package Version</th>
<th>Remote Licenses</th>
<th>Local Licenses</th>
</tr>
</table>
</body>
</html>`;

console.log(html);
