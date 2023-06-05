import os
import requests
import shutil

#################
# PREPARE FILES #
#################
source_dir = os.path.dirname(os.path.realpath(__file__))
md_file = os.path.join(source_dir, 'project.md')


##################
# PARSE MARKDOWN #
##################
with open(md_file, 'r') as f:
	md = f.read()

#####################
# TRANSFORM TO HTML #
#####################
# documentation https://developer.github.com/v3/markdown/
r = requests.post(
	"https://api.github.com/markdown",
	json={
		"text": md,
		"mode": "markdown",
		"context": "github/gollum"
	}
)

#################
# OUTPUT RESULT #
#################
output = """
<meta name="viewport" content="width=device-width, initial-scale=1">
<link rel="stylesheet" href="github-markdown.css">
<style>
	.markdown-body {
		box-sizing: border-box;
		min-width: 200px;
		max-width: 980px;
		margin: 0 auto;
		padding: 45px;
	}

	@media (max-width: 767px) {
		.markdown-body {
			padding: 15px;
		}
	}
</style>
""" + f"""
<article class="markdown-body">
{r.text}
</article>
"""

output_dir = os.path.join(source_dir, 'output')

html_file = os.path.join(output_dir, 'index.html')
with open(html_file, "w") as f:
	f.write(output)

resources_dir = os.path.join(source_dir, 'apron-doc')
resources_target = os.path.join(output_dir, 'apron-doc')
shutil.rmtree(resources_target, ignore_errors=True)
shutil.copytree(resources_dir, resources_target)