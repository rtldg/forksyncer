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

# /// script
# dependencies = [
#   "PyGithub",
# ]
# ///

# Github fork syncer thing...

import github
import datetime
import os

def create_branch(repo, branch_name, sha):
	repo.create_git_ref("refs/heads/"+branch_name, sha)

def timey():
	return datetime.datetime.now().strftime("_%Y%m%d_%H%M%S")

def sync_branch(repo, branch_name):
	try:
		comparison = repo.compare(f"{repo.parent.owner.login}:{branch_name}", branch_name)
	except github.GithubException as ex:
		print(repo.name)
		if ex.status != 404:
			raise ex
		# "No common ancestor between parentrepo:branch and repo:branch..."
		old_branch_name = branch_name + timey()
		sha = repo.parent.get_branch(branch_name).commit.sha
		print(f"{repo.name} syncing {branch_name}. comparison 404, moving to {old_branch_name}. {branch_name} at {sha}")
		create_branch(repo, branch_name+timey(), repo.get_branch(branch_name).commit.sha)
		ref = repo.get_git_ref(f"heads/{branch_name}")
		ref.edit(sha, force=True)
		return

	if comparison.ahead_by > 0:
		if True:
			print(f"we're ahead by {comparison.ahead_by} in {repo.name}/{branch_name} so maybe the parent was deleted?")
			return
		old_branch_name = branch_name + timey()
		print(f"{repo.name} syncing {branch_name}. commits AHEAD by: {comparison.ahead_by}. moving to {old_branch_name}")
		create_branch(repo, old_branch_name, repo.get_branch(branch_name).commit.sha)

	if comparison.behind_by > 0 or comparison.ahead_by > 0:
		ref = repo.get_git_ref(f"heads/{branch_name}")
		print(f"{repo.name} syncing {branch_name}. behind by: {comparison.behind_by}. ahead by {comparison.ahead_by}")
		ref.edit(comparison.base_commit.sha, force=True)

def iter_repos(g, repos):
	skip = True
	for repo in repos:
		#if repo.name != "BombSiteLimiter": # test repo...
		#	continue

		"""
		if repo.name == "SuppressViewpunch":
			skip = False
		if skip:
			continue
		"""

		try:
			if repo.parent == None:
				continue
		except github.GithubException as ex:
			print(f"failed to fetch repo.parent on {repo.name} (status = {ex.status})")
			continue

		my_branches = {}
		try:
			for branch in repo.get_branches():
				my_branches[branch.name] = branch
		except:
			print(f"branches from {repo.name} are fucked? skipping")
			continue

		parent_branches = []
		try:
			parent_branches = [branch for branch in repo.parent.get_branches()]
		except:
			print(f"parent_branches from {repo.name} are fucked?")
			continue;

		for branch in parent_branches:
			if branch.name in my_branches:
				sync_branch(repo, branch.name)
			else:
				print(f"{repo.name} creating new branch {branch.name} at {branch.commit.sha}")
				create_branch(repo, branch.name, branch.commit.sha)

def main():
	if not "GH_ACCESS_TOKEN" in os.environ:
		with open("../forksyncertoken.secret") as f:
			os.environ["GH_ACCESS_TOKEN"] = f.read().strip()
	g = github.Github(os.environ["GH_ACCESS_TOKEN"])
	iter_repos(g, g.get_organization("eatjelly").get_repos())
	iter_repos(g, g.get_user().get_repos())

if __name__ == "__main__":
	main()
