# Github fork syncer thing...

# pip3 install PyGithub
# echo accesstoken >> access_token.secret
# python3 forksyncer.py

import github
import datetime

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
		old_branch_name = branch_name + timey()
		print(f"{repo.name} syncing {branch_name}. commits AHEAD by: {comparison.ahead_by}. moving to {old_branch_name}")
		create_branch(repo, old_branch_name, comparison.merge_base_commit.sha)

	if comparison.behind_by > 0:
		ref = repo.get_git_ref(f"heads/{branch_name}")
		print(f"{repo.name} syncing {branch_name}. commits behind by: {comparison.behind_by}")
		ref.edit(comparison.base_commit.sha, force=True)

def main():
	g = None
	with open("access_token.secret", "r") as f:
		g = github.Github(f.read().strip())

	for repo in g.get_user().get_repos():
		#if repo.name != "PKHeX": # test repo...
		#	continue
		if repo.parent == None:
			continue

		my_branches = {}
		for branch in repo.get_branches():
			my_branches[branch.name] = branch

		for branch in repo.parent.get_branches():
			if branch.name in my_branches:
				sync_branch(repo, branch.name)
			else:
				print(f"{repo.name} creating new branch {branch.name} at {branch.commit.sha}")
				create_branch(repo, branch.name, branch.commit.sha)

if __name__ == "__main__":
	main()
