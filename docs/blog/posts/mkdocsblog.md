---
date: 2024-12-20
author:
 - me
---

# Personal blog with mkdocs and github.io

Capture your client's attention with a spiffy personal blog based on mkdocs and a material theme. We'll walk through forking & modifying Jason Liu's consulting-blog-template for a **free** github.io hosted website.

<!-- more -->

## Get Jason Liu's consulting blog template

- **Assumptions**
These specific walkthrough steps are based on: 
	- Win11 
	- Anaconda for Python environments and command terminals
	- Git Bash or similar installed 
	- local repos in ```%USERPROFILE%\github\``` directory
	- a Github account
	- the repo is named blog

- **Get the repo**
	- Fork: https://github.com/jxnl/consulting-blog-template to your own github account, renaming it to the shorter 'blog'
	- Clone local copy to ```%USERPROFILE%\github\blog```

- **Setup a website**
	- Create a username.github.io account (using your username): https://pages.github.com/
	- Clone local copy to ```%USERPROFILE%\github\username.github.io``` 

- **Create a Python environment**
	
	```
	cd %USERPROFILE%\github\blog
	conda create blog
	conda activate blog
	pip install -r requirements-doc.txt
	mkdocs build
	```
	If it all works, you can skip the next subsection.

- **Fix the mkdocs-material environment**
	- If mkdocs-material[imaging] fails (e.g. on build), you may have to:
	- Read: https://squidfunk.github.io/mkdocs-material/plugins/requirements/image-processing/#cairo-graphics-windows
	- Install MSYS2: https://www.msys2.org/
	- Install Cairo Graphics:
	
	```
	pacman -S mingw-w64-ucrt-x86_64-cairo
	```

	- Check path variables 
	- Ensure that the mkdocs build step works before proceeding

## Content Updates to make to go-live: 
- mkdocs.yml
	- update the following fields:
	- [x] site_name: 'your name' 
	- [x] site_author: 'your name' 
	- [x] site_description: 'your name +/- desc'
	- [x] repo_name: 'the github repo name (that holds your blog) - "blog" recommended'
	- [x] repo_url: 'the github repo name (that holds your blog) - "blog" recommended'
	- [x] site_url: 'e.g. https://yourname.github.io/'
	- [x] copyright:
	- social:
		- [x] optionally add LinkedIn (or other socials)
			- icon: 'fontawesome/brands/linkedin'
			- link: 'update your LinkedIn link'
		- [x] link: 'update your twitter link'
		- [x] link: 'update your github link'
- docs/index.md
	- [x] update 'challenges' bullet points
	- [x] add your recent 'client success stories' to the table (or provide other proof)
	- [x] update 'help' text and bullet points 
- docs/blog/index.md
	- [x] customize 'insights' bullet points
	- [x] add a featured post with markdown as below, with seperate sections for key posts using markdown ```## New Section```   
		```- [Example Blag Post](./posts/example.md): What's next for Example?```
	- update "Subscribe to Updates" url
		- [ ] Setup convertkit account at kit.com (or podia.com for advanced users)
		- [ ] update the url to your subscribe link
		- [x] add ```{ .md-button .md-button--primary }``` directly after (url), no space, to make link into primary button
- docs/blog/.authors.yml 
	- [x] update "name" with your name
	- [x] update "avatar" with your github picture - find your github profile pic, right click & select 'copy image address' to get url
	- [x] update "url" with your twitter handle
- docs/blog/posts/
	- [x] add at least one post (then link it as a featured post)
	- [ ] delete example.md post (it is useful as an example)
- docs/
	- [ ] delete writing-samples.md (it is useful as an example)

## Blog Publishing 

- **Run Locally**: Start a local server to preview your site.
   ```
   conda activate blog
   cd %USERPROFILE%\github\blog
   mkdocs serve -w .
   ```

- **Iterate Content**
	- edit files in the blog repo under 'docs' folder (and mkdoc.yml)
	- serve locally 
		```
		mkdocs serve -w .
		``` 
	- view on local browser e.g. http://127.0.0.1:8000/
	- often saving a .md file will auto-refresh the site
	- on error: 
		- hit CTRL-C in the Anaconda prompt window, then
		- serve locally again 
		```
		mkdocs serve -w .
		``` 

- **Save Blog**
	- Check changes & add new files per usual ```git status```, ```git add -all``` etc.
	- Commit changes to your local blog repo ```git commit -m "my blog updates"```
	- Optional: Push blog markdown to github: ```git push origin```

- **Publish Blog**
	- Reference: https://www.mkdocs.org/user-guide/deploying-your-docs/#organization-and-user-pages
	- Go to your username.github.io local repo: 

		```
		cd %USERPROFILE%\github\username.github.io
		```

	- Deploy (targeting main branch): 

		```
		mkdocs gh-deploy --config-file ..\blog\mkdocs.yml --remote-branch main
		```
	- Review, iterate as needed

## Custom URL

- **Custom URL Setup (one time)**
	- By default, your blog/website will be at https://username.github.io, but you can easily give it a custom URL
	- Buy a domain of your choice: e.g. username.com
	- Review!: https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site
		- Configure DNS, Verify the Domain, and Enable the Custom domain on your github.io site
		- No wildcards 

## Conclusion

