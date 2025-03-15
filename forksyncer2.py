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
import pdb

# https://gitpython.readthedocs.io/en/stable/index.html
# https://pygithub.readthedocs.io/en/latest/index.html

class MyProgressPrinter(git.RemoteProgress):
	def update(self, op_code, cur_count, max_count=None, message=''):
		print(op_code, cur_count, max_count, cur_count / (max_count or 100.0), message or "NO MESSAGE")

def handle_remote(repo, remote):
	# check if valid remote...

	for fetch_info in remote.fetch(): #progress=MyProgressPrinter()):
		print("Updated %s to %s" % (fetch_info.ref, fetch_info.commit))

	"""
	if not repo.name.endswith(".wiki"):
		ghrepo = gh.get_repo()
		scrape_issues(repo, ghrepo)
		scrape_releases(repo, ghrepo)
	"""

	"""
	commits_behind = repo.iter_commits('master..origin/master')
	commits_ahead = repo.iter_commits('origin/master..master')
	count = sum(1 for c in commits_ahead)
	"""

	"""
	commits_diff = repo.git.rev_list('--left-right', '--count', f'{branch}...{branch}@{{u}}')
	num_ahead, num_behind = commits_diff.split('\t')
	"""

def scrape_issues(localrepo, ghrepo):
	lastscrapedate = None
	issues = ghrepo.get_issues(
		state='all',
		since=lastscrapedate,
		sort='updated'
	)

def main():
	GH_ACCESS_TOKEN = os.environ["GH_ACCESS_TOKEN"]
	ARK_META_REPO = os.environ["ARK_META_REPO"]
	ARK_STORAGE_DIR = os.environ["ARK_STORAGE_DIR"]
	GITHUB_HOST = os.environ["GITHUB_HOST"]

	Path(ARK_STORAGE_DIR).mkdir(parents=True, exist_ok=True)
	Path(ARK_META_REPO + "/meta").mkdir(parents=True, exist_ok=True)

	gh = github.Github(GH_ACCESS_TOKEN)
	username = gh.get_user().login
	storage = Path(ARK_STORAGE_DIR)

	for ghrepo in gh.get_user().get_repos():
		folder = storage / ghrepo.name
		if folder.exists():
			continue

		print(f"cloning {username}/{ghrepo.name}")
		arkrepo = git.Repo.clone_from(
			f"git@{GITHUB_HOST}:{username}/{ghrepo.name}.git",
			folder,
			multi_options=[],
			no_single_branch=True,
			#progress=MyProgressPrinter(), # print spam
			mirror=True
		)

		if ghrepo.fork:
			print(f"  adding remote {ghrepo.parent.owner.login}_{ghrepo.parent.name}")
			arkrepo.create_remote(f"{ghrepo.parent.owner.login}_{ghrepo.parent.name}", ghrepo.parent.clone_url)
			if ghrepo.source != ghrepo.parent:
				print(f"  adding remote {ghrepo.source.owner.login}_{ghrepo.source.name}")
				arkrepo.create_remote(f"{ghrepo.source.owner.login}_{ghrepo.source.name}", ghrepo.source.clone_url)

	#pdb.set_trace()

	for f in storage.iterdir():
		if not f.is_dir():
			continue
		repo = git.Repo(f) # need to catch git.exc.InvalidGitRepositoryError
		for remote in repo.remotes:
			handle_remote(repo, remote)


if __name__ == "__main__":
	main()
