"""
MIT License

Copyright (c) 2022 rtldg

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

# Github fork syncer thing...

import os
import io
import datetime
from pathlib import Path
import git
import github

class MyProgressPrinter(git.RemoteProgress):
	def update(self, op_code, cur_count, max_count=None, message=''):
		print(op_code, cur_count, max_count, cur_count / (max_count or 100.0), message or "NO MESSAGE")

def handle_remote(meta, repo, remote):
	# check if valid remote...

	"""
	for fetch_info in remote.fetch(progress=MyProgressPrinter()):
		print("Updated %s to %s" % (fetch_info.ref, fetch_info.commit))
	"""

	"""
	if not repo.name.endswith(".wiki.git"):
		ghrepo = gh.get_repo()
		scrape_issues(meta, repo, ghrepo)
		scrape_releases(meta, repo, ghrepo)
	"""

def scrape_issues(meta, localrepo, ghrepo):
	lastscrapedate = None
	issues = ghrepo.get_issues(
		state='all',
		since=lastscrapedate,
		sort='updated'
	)

def main():
	#GH_ACCESS_TOKEN = os.environ["GH_ACCESS_TOKEN"]
	ARK_META_REPO = os.environ["ARK_META_REPO"]
	ARK_STORAGE_DIR = os.environ["ARK_STORAGE_DIR"]

	Path(ARK_STORAGE_DIR).mkdir(parents=True, exist_ok=True)
	Path(ARK_META_REPO + "/meta").mkdir(parents=True, exist_ok=True)

	#gh = github.Github(GH_ACCESS_TOKEN)

	for f in Path(ARK_STORAGE_DIR).iterdir():
		if not f.is_dir():
			continue
		repo = git.Repo(f) # need to catch git.exc.InvalidGitRepositoryError
		print(repo)
		for remote in repo.remotes:
			handle_remote(meta, repo, remote)


if __name__ == "__main__":
	main()
